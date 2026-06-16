import os
import uuid
import threading
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.schema import ResearchResult, ComparisonResult
from backend.pipeline import (
    run_research_pipeline, 
    run_comparison, 
    ACTIVE_RUNS_LOGS, 
    ACTIVE_RUNS_STATUS, 
    API_KEYS,
    add_log
)

app = FastAPI(
    title="Competitive Intelligence Research Agent API",
    description="Backend API for autonomous competitive intelligence research on loyalty programs.",
    version="1.0.0"
)

# Enable CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Competitive Intelligence Research Agent Backend API is running.",
        "frontend_dashboard": "http://localhost:5173",
        "api_documentation": "http://127.0.0.1:8000/docs"
    }

# Global results database in-memory
RESEARCH_RESULTS_DB: Dict[str, ResearchResult] = {}
COMPARISON_RESULTS_DB: Dict[str, ComparisonResult] = {}

class ResearchRequest(BaseModel):
    program_name: str
    compare_with: Optional[str] = None
    force_live: bool = False

class SettingsRequest(BaseModel):
    tavily_key: Optional[str] = None
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    gemini_key: Optional[str] = None

# Background task runner
def execute_research_task(run_id: str, program_name: str, compare_with: Optional[str], force_live: bool):
    try:
        if compare_with:
            # Dual research mode
            add_log(run_id, f"Initializing DUAL COMPARISON Mode: '{program_name}' vs '{compare_with}'")
            
            # Create sub run IDs
            run_id_a = f"{run_id}_a"
            run_id_b = f"{run_id}_b"
            
            add_log(run_id, f"Launching parallel sub-agents for Program A: '{program_name}'")
            res_a = run_research_pipeline(run_id_a, program_name, force_live)
            RESEARCH_RESULTS_DB[run_id_a] = res_a
            
            # Simulate separation of logs
            for log in ACTIVE_RUNS_LOGS.get(run_id_a, []):
                add_log(run_id, f"[PROGRAM A] {log.split(']', 1)[-1].strip()}")
                
            add_log(run_id, f"Launching parallel sub-agents for Program B: '{compare_with}'")
            res_b = run_research_pipeline(run_id_b, compare_with, force_live)
            RESEARCH_RESULTS_DB[run_id_b] = res_b
            
            for log in ACTIVE_RUNS_LOGS.get(run_id_b, []):
                add_log(run_id, f"[PROGRAM B] {log.split(']', 1)[-1].strip()}")
                
            ACTIVE_RUNS_STATUS[run_id]["current_component"] = "Comparator"
            add_log(run_id, "Comparator started: Generating side-by-side schema diff and strategic positioning brief.")
            time_delay = 1.5
            threading.Event().wait(time_delay)
            
            comparison = run_comparison(res_a, res_b)
            COMPARISON_RESULTS_DB[run_id] = comparison
            
            ACTIVE_RUNS_STATUS[run_id]["components_done"].append("Comparator")
            ACTIVE_RUNS_STATUS[run_id]["status"] = "complete"
            add_log(run_id, f"Dual comparison pipeline finished for '{program_name}' vs '{compare_with}'!")
        else:
            # Single research mode
            add_log(run_id, f"Initializing SINGLE PROGRAM Mode: '{program_name}'")
            res = run_research_pipeline(run_id, program_name, force_live)
            RESEARCH_RESULTS_DB[run_id] = res
            ACTIVE_RUNS_STATUS[run_id]["status"] = "complete"
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        add_log(run_id, f"CRITICAL ERROR in pipeline execution: {str(e)}")
        print(error_trace)
        ACTIVE_RUNS_STATUS[run_id]["status"] = "failed"
        ACTIVE_RUNS_STATUS[run_id]["error"] = str(e)


@app.post("/api/research")
def start_research(req: ResearchRequest, background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())
    
    ACTIVE_RUNS_STATUS[run_id] = {
        "status": "queued",
        "current_component": "Queued",
        "components_done": [],
        "program_name": req.program_name,
        "compare_with": req.compare_with
    }
    ACTIVE_RUNS_LOGS[run_id] = []
    
    background_tasks.add_task(
        execute_research_task,
        run_id,
        req.program_name,
        req.compare_with,
        req.force_live
    )
    
    return {"run_id": run_id}


@app.get("/api/research/{run_id}/status")
def get_research_status(run_id: str):
    if run_id not in ACTIVE_RUNS_STATUS:
        raise HTTPException(status_code=404, detail="Research run ID not found")
        
    status_info = ACTIVE_RUNS_STATUS[run_id]
    logs = ACTIVE_RUNS_LOGS.get(run_id, [])
    
    return {
        "status": status_info.get("status"),
        "current_component": status_info.get("current_component"),
        "components_done": status_info.get("components_done"),
        "logs": logs,
        "program_name": status_info.get("program_name"),
        "compare_with": status_info.get("compare_with"),
        "error": status_info.get("error")
    }


@app.get("/api/research/{run_id}/result")
def get_research_result(run_id: str):
    status_info = ACTIVE_RUNS_STATUS.get(run_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Research run ID not found")
        
    if status_info["status"] != "complete":
        raise HTTPException(status_code=400, detail="Research run is not complete yet")
        
    compare_with = status_info.get("compare_with")
    
    if compare_with:
        comparison_res = COMPARISON_RESULTS_DB.get(run_id)
        if not comparison_res:
            raise HTTPException(status_code=500, detail="Comparison result missing")
        return {
            "mode": "comparison",
            "comparison": comparison_res
        }
    else:
        res = RESEARCH_RESULTS_DB.get(run_id)
        if not res:
            raise HTTPException(status_code=500, detail="Research result missing")
        return {
            "mode": "single",
            "schema_data": res.schema_data,
            "narrative": res.narrative,
            "sources": res.sources,
            "completeness": res.completeness,
            "confidence_summary": res.confidence_summary
        }


@app.get("/api/research/{run_id}/sources")
def get_research_sources(run_id: str):
    status_info = ACTIVE_RUNS_STATUS.get(run_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Research run ID not found")
        
    compare_with = status_info.get("compare_with")
    if compare_with:
        # Return merged sources
        sources_a = RESEARCH_RESULTS_DB.get(f"{run_id}_a")
        sources_b = RESEARCH_RESULTS_DB.get(f"{run_id}_b")
        return {
            "program_a_sources": sources_a.sources if sources_a else [],
            "program_b_sources": sources_b.sources if sources_b else []
        }
    else:
        res = RESEARCH_RESULTS_DB.get(run_id)
        return {"sources": res.sources if res else []}


@app.post("/api/settings")
def save_settings(req: SettingsRequest):
    if req.tavily_key is not None:
        API_KEYS["TAVILY_API_KEY"] = req.tavily_key
        os.environ["TAVILY_API_KEY"] = req.tavily_key
    if req.openai_key is not None:
        API_KEYS["OPENAI_API_KEY"] = req.openai_key
        os.environ["OPENAI_API_KEY"] = req.openai_key
    if req.anthropic_key is not None:
        API_KEYS["ANTHROPIC_API_KEY"] = req.anthropic_key
        os.environ["ANTHROPIC_API_KEY"] = req.anthropic_key
    if req.gemini_key is not None:
        API_KEYS["GEMINI_API_KEY"] = req.gemini_key
        os.environ["GEMINI_API_KEY"] = req.gemini_key
        
    return {"status": "success", "keys_configured": {k: bool(v) for k, v in API_KEYS.items()}}


@app.get("/api/settings")
def get_settings():
    return {"keys_configured": {k: bool(v) for k, v in API_KEYS.items()}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
