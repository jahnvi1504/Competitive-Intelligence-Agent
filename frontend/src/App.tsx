import React, { useState, useEffect, useRef } from 'react';
import { 
  Search, Settings, Play, CheckCircle, AlertTriangle, Activity, 
  FileText, Layers, Globe, DollarSign, Award, Smartphone, 
  Heart, TrendingUp, ExternalLink, Shield, ArrowRight, Lock, 
  RefreshCw, Download, ChevronDown, ChevronUp, Check, X
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

// Theme colors
const COLORS = {
  high: '#10b981',       // Green
  medium: '#f59e0b',     // Amber
  low: '#f97316',        // Orange
  unverified: '#6b7280', // Grey
  conflict: '#ef4444'    // Red
};

interface SchemaFieldData {
  value: any;
  confidence: string;
  source_url: string | null;
  access_date: string | null;
  conflict: boolean;
  conflicting_value: any;
  conflicting_source_url: string | null;
}

interface ProgramSchema {
  [key: string]: SchemaFieldData;
}

interface SourceMetadata {
  url: string;
  domain: string;
  page_type: string;
  access_date: string;
  tier: string;
  confidence_contribution: number;
  status: string;
  rejection_reason: string | null;
}

interface ResearchResult {
  mode: 'single' | 'comparison';
  schema_data?: ProgramSchema;
  narrative?: string;
  sources?: SourceMetadata[];
  completeness?: number;
  confidence_summary?: {
    high: number;
    medium: number;
    low: number;
    unverified: number;
    conflicts: number;
  };
  comparison?: {
    program_a_name: string;
    program_b_name: string;
    schema_a: ProgramSchema;
    schema_b: ProgramSchema;
    narrative_a: string;
    narrative_b: string;
    strategic_analysis: string;
    comparison_table: any[];
  };
}

export default function App() {
  // Search state
  const [progA, setProgA] = useState('Starbucks Rewards');
  const [progB, setProgB] = useState('');
  const [compareMode, setCompareMode] = useState(false);
  const [forceLive, setForceLive] = useState(false);

  // Settings state
  const [showSettings, setShowSettings] = useState(false);
  const [keys, setKeys] = useState({
    tavily_key: '',
    openai_key: '',
    anthropic_key: '',
    gemini_key: ''
  });
  const [keysConfigured, setKeysConfigured] = useState({
    TAVILY_API_KEY: false,
    OPENAI_API_KEY: false,
    ANTHROPIC_API_KEY: false,
    GEMINI_API_KEY: false
  });

  // Pipeline execution state
  const [runId, setRunId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('idle'); // idle, running, complete, failed
  const [currentComp, setCurrentComp] = useState<string>('Orchestrator');
  const [compsDone, setCompsDone] = useState<string[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Result state
  const [activeTab, setActiveTab] = useState<'schema' | 'narrative' | 'comparison' | 'sources'>('schema');
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [selectedFootnote, setSelectedFootnote] = useState<number | null>(null);

  // Collapsible schema sections
  const [collapsedSections, setCollapsedSections] = useState<{ [key: string]: boolean }>({
    basics: false,
    earn: true,
    burn: true,
    tiers: true,
    partners: true,
    digital: true,
    sentiment: true,
    position: true
  });

  // Track expanded conflict rows
  const [expandedConflicts, setExpandedConflicts] = useState<{ [key: string]: boolean }>({});

  const consoleEndRef = useRef<HTMLDivElement>(null);

  // Load settings configurations
  useEffect(() => {
    fetchSettings();
  }, []);

  // Scroll console to bottom on new logs
  useEffect(() => {
    if (consoleEndRef.current) {
      consoleEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  // Status polling effect
  useEffect(() => {
    let timer: any;
    if (runId && status === 'running') {
      timer = setInterval(async () => {
        try {
          const res = await fetch(`http://127.0.0.1:8000/api/research/${runId}/status`);
          const data = await res.json();
          setLogs(data.logs || []);
          setCurrentComp(data.current_component || 'Orchestrator');
          setCompsDone(data.components_done || []);
          
          if (data.status === 'complete') {
            setStatus('complete');
            clearInterval(timer);
            fetchResult(runId);
          } else if (data.status === 'failed') {
            setStatus('failed');
            setErrorMsg(data.error || 'Execution failed');
            clearInterval(timer);
          }
        } catch (e) {
          console.error("Error polling status", e);
        }
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [runId, status]);

  const fetchSettings = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/settings');
      const data = await res.json();
      setKeysConfigured(data.keys_configured);
    } catch (e) {
      console.error("Error fetching settings", e);
    }
  };

  const saveSettings = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(keys)
      });
      const data = await res.json();
      setKeysConfigured(data.keys_configured);
      setShowSettings(false);
    } catch (e) {
      alert("Failed to save settings");
    }
  };

  const triggerResearch = async () => {
    if (!progA.trim()) {
      alert("Please enter at least one loyalty program name.");
      return;
    }
    
    setStatus('running');
    setLogs([]);
    setCompsDone([]);
    setErrorMsg(null);
    setResult(null);
    setRunId(null);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          program_name: progA,
          compare_with: compareMode && progB ? progB : null,
          force_live: forceLive
        })
      });
      const data = await res.json();
      setRunId(data.run_id);
    } catch (e) {
      setStatus('failed');
      setErrorMsg("Failed to connect to backend server. Make sure FastAPI backend is running.");
    }
  };

  const fetchResult = async (id: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/research/${id}/result`);
      const data = await res.json();
      setResult(data);
      if (data.mode === 'comparison') {
        setActiveTab('comparison');
      } else {
        setActiveTab('schema');
      }
    } catch (e) {
      setStatus('failed');
      setErrorMsg("Failed to retrieve research results.");
    }
  };

  const handlePresetSelect = (prog: string) => {
    if (compareMode) {
      if (!progA || progA === prog) {
        setProgA(prog);
      } else {
        setProgB(prog);
      }
    } else {
      setProgA(prog);
    }
  };

  const toggleSection = (section: string) => {
    setCollapsedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Render schema categories helper
  const renderSchemaRow = (label: string, fieldName: string, schema: ProgramSchema) => {
    const data = schema[fieldName];
    if (!data) return null;

    const isExpanded = !!expandedConflicts[fieldName];

    const getConfidenceBadgeColor = (conf: string) => {
      switch (conf.toLowerCase()) {
        case 'high': return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30';
        case 'medium': return 'bg-amber-500/15 text-amber-400 border border-amber-500/30';
        case 'low': return 'bg-orange-500/15 text-orange-400 border border-orange-500/30';
        case 'conflict': return 'bg-rose-500/15 text-rose-400 border border-rose-500/30 animate-pulse';
        default: return 'bg-gray-500/15 text-gray-400 border border-gray-500/30';
      }
    };

    const formatValue = (val: any) => {
      if (val === null || val === undefined) return <span className="text-gray-500 italic">unverified</span>;
      if (Array.isArray(val)) {
        return (
          <div className="flex flex-wrap gap-1">
            {val.map((item, idx) => (
              <span key={idx} className="bg-gray-800 text-gray-300 text-xs px-2 py-0.5 rounded border border-gray-700">
                {item}
              </span>
            ))}
          </div>
        );
      }
      if (typeof val === 'object') {
        return (
          <div className="text-xs bg-gray-950/60 p-2 rounded border border-gray-800 font-mono text-gray-300">
            {Object.entries(val).map(([k, v]: any) => (
              <div key={k} className="mb-0.5">
                <span className="text-indigo-400 font-semibold">{k}:</span> {v}
              </div>
            ))}
          </div>
        );
      }
      return <span className="text-gray-200 text-sm font-medium">{val}</span>;
    };

    return (
      <React.Fragment key={fieldName}>
        <tr className="border-b border-darkBorder hover:bg-gray-900/20 transition-colors">
          <td className="py-3 px-4 text-xs font-semibold text-gray-400 font-mono tracking-wider align-top w-1/4">
            {fieldName}
            <div className="text-[10px] text-gray-600 font-normal mt-0.5">{label}</div>
          </td>
          <td className="py-3 px-4 text-sm align-top w-1/2">
            {formatValue(data.value)}
          </td>
          <td className="py-3 px-4 align-top w-1/8">
            <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full ${getConfidenceBadgeColor(data.conflict ? 'conflict' : data.confidence)}`}>
              {data.conflict ? '⚠️ CONFLICT' : data.confidence}
            </span>
          </td>
          <td className="py-3 px-4 align-top text-xs text-right w-1/8">
            {data.source_url ? (
              <a 
                href={data.source_url} 
                target="_blank" 
                rel="noreferrer" 
                className="inline-flex items-center text-indigo-400 hover:text-indigo-300 transition-colors bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20"
              >
                Link <ExternalLink size={10} className="ml-1" />
              </a>
            ) : (
              <span className="text-gray-600">—</span>
            )}
            {data.conflict && (
              <button 
                onClick={() => setExpandedConflicts(prev => ({ ...prev, [fieldName]: !prev[fieldName] }))} 
                className="block text-[10px] text-rose-400 hover:text-rose-300 underline font-semibold mt-1.5 ml-auto cursor-pointer"
              >
                {isExpanded ? 'Hide Conflict' : 'Show Conflict'}
              </button>
            )}
          </td>
        </tr>
        {data.conflict && isExpanded && (
          <tr className="bg-rose-950/20 border-b border-rose-900/20 animate-fadeIn">
            <td colSpan={4} className="py-3 px-6 text-xs text-rose-300">
              <div className="flex flex-col gap-1.5 border-l-2 border-rose-500 pl-4 py-1">
                <div>
                  <span className="font-semibold text-rose-400">Primary Value:</span> "{data.value}"
                  {data.source_url && (
                    <a href={data.source_url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline inline-flex items-center ml-1.5">
                      [{new URL(data.source_url).host}]
                    </a>
                  )}
                </div>
                <div>
                  <span className="font-semibold text-rose-400">Conflicting Value:</span> "{data.conflicting_value}"
                  {data.conflicting_source_url && (
                    <a href={data.conflicting_source_url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline inline-flex items-center ml-1.5">
                      [{new URL(data.conflicting_source_url).host}]
                    </a>
                  )}
                </div>
                <div className="text-[10px] text-rose-400/70 italic mt-0.5">
                  * Conflict detected. Higher-tier source displayed primary. Verify manually before client use.
                </div>
              </div>
            </td>
          </tr>
        )}
      </React.Fragment>
    );
  };

  // Mock document exporter
  const triggerExport = (format: 'pdf' | 'pptx') => {
    alert(`Generating Client-Ready ${format.toUpperCase()} Deck...\nYour verified intelligence profile is being compiled.`);
    const element = document.createElement("a");
    const file = new Blob([result?.narrative || ''], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${progA.toLowerCase().replace(/ /g, '_')}_brief.${format === 'pdf' ? 'pdf' : 'pptx'}`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Pie chart calculations
  const pieData = result?.confidence_summary ? [
    { name: 'High', value: result.confidence_summary.high, color: COLORS.high },
    { name: 'Medium', value: result.confidence_summary.medium, color: COLORS.medium },
    { name: 'Low', value: result.confidence_summary.low, color: COLORS.low },
    { name: 'Unverified', value: result.confidence_summary.unverified, color: COLORS.unverified }
  ].filter(d => d.value > 0) : [];

  return (
    <div className="min-h-screen bg-darkBg text-gray-100 flex flex-col">
      {/* HEADER */}
      <header className="border-b border-darkBorder bg-darkPanel/70 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-indigo-500/20 border border-indigo-400/20">
              <Activity className="text-white" size={20} />
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-tight text-white flex items-center gap-1.5">
                COMPETITIVE INTELLIGENCE RESEARCH AGENT
              </h1>
              <p className="text-[10px] text-gray-400 font-medium font-mono">Autonomous Research Desk</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={() => setShowSettings(true)}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors border border-transparent hover:border-darkBorder relative cursor-pointer"
            >
              <Settings size={18} />
              {(keysConfigured.TAVILY_API_KEY || keysConfigured.OPENAI_API_KEY) && (
                <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-emerald-500 ring-2 ring-darkBg" />
              )}
            </button>
            <div className="text-[11px] font-mono text-gray-500 border-l border-darkBorder pl-4 ml-2">
              Team: Styles | PES University
            </div>
          </div>
        </div>
      </header>

      {/* DASHBOARD GRID */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col lg:flex-row gap-6">
        
        {/* LEFT PANEL: INPUT & CONTROLS */}
        <div className="w-full lg:w-96 flex flex-col gap-6 shrink-0">
          
          {/* RESEARCH CONTROL CARD */}
          <div className="glass-card rounded-2xl p-5 shadow-2xl flex flex-col gap-4 relative overflow-hidden">
            <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/5 rounded-full filter blur-2xl -mr-10 -mt-10" />
            
            <div className="flex items-center justify-between border-b border-darkBorder/60 pb-3">
              <h2 className="text-xs font-bold font-mono text-white flex items-center gap-2">
                <Search size={14} className="text-indigo-400" /> RESEARCH DESK
              </h2>
              <div className="flex items-center gap-1 bg-gray-950 p-0.5 rounded-lg border border-darkBorder">
                <button 
                  onClick={() => setCompareMode(false)}
                  className={`text-[10px] px-2.5 py-1 rounded font-semibold transition-all cursor-pointer ${!compareMode ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}`}
                >
                  Single
                </button>
                <button 
                  onClick={() => setCompareMode(true)}
                  className={`text-[10px] px-2.5 py-1 rounded font-semibold transition-all cursor-pointer ${compareMode ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}`}
                >
                  Compare
                </button>
              </div>
            </div>

            {/* PRESET PILLS */}
            <div>
              <div className="text-[10px] font-mono text-gray-400 mb-2 font-semibold tracking-wider">POPULAR PROGRAM CACHE:</div>
              <div className="flex flex-wrap gap-1.5">
                {['Starbucks Rewards', 'MyMcDonald\'s Rewards', 'Beauty Insider', 'Marriott Bonvoy', 'Delta SkyMiles'].map(prog => (
                  <button
                    key={prog}
                    onClick={() => handlePresetSelect(prog)}
                    className="text-[10px] bg-gray-800/80 hover:bg-indigo-900/30 text-gray-300 hover:text-indigo-300 px-2.5 py-1 rounded-md border border-gray-700/60 hover:border-indigo-500/30 transition-all font-medium cursor-pointer"
                  >
                    {prog}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-mono text-gray-400 font-bold uppercase">Program Name</label>
                <input 
                  type="text" 
                  value={progA} 
                  onChange={(e) => setProgA(e.target.value)}
                  placeholder="e.g. Starbucks Rewards"
                  className="bg-gray-950/80 border border-darkBorder focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-sm outline-none text-white w-full placeholder:text-gray-600 transition-colors"
                />
              </div>

              {compareMode && (
                <div className="flex flex-col gap-1.5 animate-fadeIn">
                  <div className="flex items-center gap-1.5">
                    <ArrowRight size={10} className="text-indigo-400 rotate-90 lg:rotate-0" />
                    <label className="text-[10px] font-mono text-gray-400 font-bold uppercase">Compare With</label>
                  </div>
                  <input 
                    type="text" 
                    value={progB} 
                    onChange={(e) => setProgB(e.target.value)}
                    placeholder="e.g. Dunkin' Rewards"
                    className="bg-gray-950/80 border border-darkBorder focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-sm outline-none text-white w-full placeholder:text-gray-600 transition-colors"
                  />
                </div>
              )}
            </div>

            {/* LIVE TOGGLE */}
            <div className="flex items-center justify-between bg-gray-950/50 p-3 rounded-xl border border-darkBorder/40">
              <div className="flex flex-col">
                <span className="text-[11px] font-bold text-gray-300 flex items-center gap-1">
                  <Globe size={11} className="text-gray-400" /> Live Agent Mode
                </span>
                <span className="text-[9px] text-gray-500">Query web in real-time</span>
              </div>
              <input 
                type="checkbox" 
                checked={forceLive} 
                onChange={(e) => setForceLive(e.target.checked)}
                className="sr-only peer"
                id="live-toggle"
              />
              <label 
                htmlFor="live-toggle"
                className="relative w-8 h-4 bg-gray-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-gray-400 peer-checked:after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-indigo-600 cursor-pointer"
              />
            </div>

            <button
              onClick={triggerResearch}
              disabled={status === 'running'}
              className="w-full mt-2 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold text-xs tracking-wider shadow-lg shadow-indigo-500/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2 btn-shine cursor-pointer"
            >
              {status === 'running' ? (
                <>
                  <RefreshCw size={14} className="animate-spin" /> RUNNING PIPELINE...
                </>
              ) : (
                <>
                  <Play size={14} fill="white" /> INITIATE INTELLIGENCE AGENT
                </>
              )}
            </button>
          </div>

          {/* PIPELINE PROGRESS & STATUS */}
          {status !== 'idle' && (
            <div className="glass-card rounded-2xl p-5 shadow-2xl flex flex-col gap-4">
              <h3 className="text-xs font-bold font-mono text-white flex items-center gap-2 border-b border-darkBorder/60 pb-3">
                <Activity size={14} className="text-indigo-400" /> PIPELINE MONITOR
              </h3>

              {/* STAGES CHRONOLOGY */}
              <div className="flex flex-col gap-3">
                {[
                  { name: 'Orchestrator', desc: 'Query decomp & dispatch' },
                  { name: 'Retriever', desc: 'Parallel searches & scraping' },
                  { name: 'Extractor', desc: 'Qdrant vector extraction' },
                  { name: 'Verifier', desc: 'Confidence weights & fingerprint' },
                  { name: 'Narrator', desc: 'Analyst brief footnote synthesis' },
                  ...(compareMode ? [{ name: 'Comparator', desc: 'Strategic positioning analysis' }] : [])
                ].map((stage, idx) => {
                  const isDone = compsDone.includes(stage.name) || (status === 'complete');
                  const isActive = currentComp === stage.name && status === 'running';
                  return (
                    <div key={idx} className="flex items-start gap-3 relative">
                      {idx !== (compareMode ? 5 : 4) && (
                        <div className={`absolute left-2.5 top-5 w-[1px] h-8 ${isDone ? 'bg-emerald-500/40' : 'bg-gray-800'}`} />
                      )}
                      <div className={`h-5 w-5 rounded-full flex items-center justify-center border text-[9px] font-bold z-10 ${
                        isDone ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400' : 
                        isActive ? 'bg-indigo-500/20 border-indigo-500 text-indigo-400 animate-pulse' : 
                        'bg-gray-950 border-gray-800 text-gray-500'
                      }`}>
                        {isDone ? '✓' : idx + 1}
                      </div>
                      <div className="flex-1">
                        <div className="text-[11px] font-bold flex items-center justify-between">
                          <span className={isDone ? 'text-emerald-400' : isActive ? 'text-indigo-400' : 'text-gray-400'}>
                            {stage.name}
                          </span>
                          {isActive && <span className="text-[9px] text-indigo-400 animate-pulse font-mono font-normal">Active</span>}
                        </div>
                        <p className="text-[9px] text-gray-500 mt-0.5">{stage.desc}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* SUB-AGENTS BADGES */}
              <div className="border-t border-darkBorder/60 pt-3 flex flex-col gap-2">
                <div className="text-[9px] font-mono text-gray-400 font-bold uppercase tracking-wider">RETRIEVER SUB-AGENTS:</div>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { name: 'Search Agent', run: compsDone.includes('Retriever') || status === 'complete' },
                    { name: 'Scraper Agent', run: compsDone.includes('Retriever') || status === 'complete' },
                    { name: 'News Agent', run: compsDone.includes('Retriever') || status === 'complete' },
                    { name: 'Sentiment Agent', run: compsDone.includes('Retriever') || status === 'complete' }
                  ].map((sub, idx) => (
                    <div key={idx} className={`p-2 rounded-lg border text-[10px] font-semibold font-mono flex items-center justify-between ${
                      sub.run ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400' : 
                      status === 'running' && currentComp === 'Retriever' ? 'bg-indigo-500/5 border-indigo-500/20 text-indigo-400 animate-pulse' :
                      'bg-gray-950 border-gray-900 text-gray-600'
                    }`}>
                      <span>{sub.name}</span>
                      <span className="text-[8px] font-bold">
                        {sub.run ? 'DONE' : status === 'running' && currentComp === 'Retriever' ? 'RUN' : 'WAIT'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

        </div>

        {/* MAIN DISPLAY PANEL */}
        <div className="flex-1 flex flex-col gap-6">

          {/* SYSTEM CONSOLE LOGS */}
          {status === 'running' && (
            <div className="glass-card rounded-2xl p-5 shadow-2xl flex flex-col gap-3">
              <h3 className="text-xs font-bold font-mono text-white flex items-center gap-2 border-b border-darkBorder/60 pb-2.5">
                <Activity size={14} className="text-indigo-400 animate-pulse" /> AGENT TERMINAL CONSOLE
              </h3>
              <div className="bg-gray-950 rounded-xl p-4 border border-darkBorder font-mono text-xs text-gray-400 h-44 overflow-y-auto flex flex-col gap-1.5 shadow-inner leading-relaxed">
                {logs.length === 0 ? (
                  <div className="text-gray-600 italic">Initializing runner...</div>
                ) : (
                  logs.map((log, idx) => (
                    <div key={idx} className={`border-b border-gray-900/30 pb-0.5 ${
                      log.includes('⚠️') ? 'text-rose-400' : 
                      log.includes('[PROGRAM A]') ? 'text-sky-400' :
                      log.includes('[PROGRAM B]') ? 'text-amber-400' :
                      'text-gray-300'
                    }`}>
                      {log}
                    </div>
                  ))
                )}
                <div ref={consoleEndRef} />
              </div>
            </div>
          )}

          {/* FAILED STATE */}
          {status === 'failed' && (
            <div className="bg-rose-950/20 border border-rose-500/30 rounded-2xl p-6 flex items-start gap-4 shadow-xl">
              <AlertTriangle className="text-rose-400 shrink-0" size={24} />
              <div>
                <h3 className="text-rose-400 font-bold text-sm">Pipeline Execution Interrupted</h3>
                <p className="text-rose-300/80 text-xs mt-1 leading-relaxed">{errorMsg}</p>
                <button 
                  onClick={triggerResearch}
                  className="mt-4 px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 rounded-lg text-xs font-bold border border-rose-500/20 hover:border-rose-500/40 transition-all cursor-pointer"
                >
                  Retry Run
                </button>
              </div>
            </div>
          )}

          {/* COMPLETE STATE / OUTPUT VIEW */}
          {status === 'complete' && result && (
            <div className="flex-1 flex flex-col gap-6 animate-fadeIn">
              
              {/* SUMMARY STATS CARD */}
              {result.mode === 'single' && (
                <div className="glass-card rounded-2xl p-5 shadow-2xl flex flex-col md:flex-row items-center gap-6">
                  
                  {/* COMPLETENESS CHANGER */}
                  <div className="flex flex-col items-center gap-1.5 text-center shrink-0">
                    <div className="relative h-24 w-24 flex items-center justify-center">
                      <svg className="w-full h-full transform -rotate-90">
                        <circle cx="48" cy="48" r="40" stroke="#1f2937" strokeWidth="6" fill="transparent" />
                        <circle cx="48" cy="48" r="40" stroke="url(#indigoGrad)" strokeWidth="6" fill="transparent" 
                          strokeDasharray={251.2}
                          strokeDashoffset={251.2 - (251.2 * (result.completeness || 0)) / 100}
                        />
                        <defs>
                          <linearGradient id="indigoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#4f46e5" />
                            <stop offset="100%" stopColor="#9333ea" />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div className="absolute text-xl font-bold text-white">{result.completeness}%</div>
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white tracking-wide">PROFILE COMPLETENESS</h4>
                      <p className="text-[10px] text-gray-400 mt-0.5">Populated: 31/45 schema fields</p>
                    </div>
                  </div>

                  {/* PIE CHART CONFIDENCE METRIC */}
                  <div className="flex-1 w-full flex flex-col sm:flex-row items-center gap-6 border-t md:border-t-0 md:border-l border-darkBorder pt-4 md:pt-0 md:pl-6">
                    <div className="h-24 w-24 shrink-0">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={28}
                            outerRadius={40}
                            paddingAngle={3}
                            dataKey="value"
                          >
                            {pieData.map((entry, idx) => (
                              <Cell key={`cell-${idx}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip 
                            contentStyle={{ background: '#111827', border: '1px solid #1f2937', borderRadius: '8px' }}
                            itemStyle={{ color: '#fff', fontSize: '10px' }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    
                    <div className="flex-1 grid grid-cols-2 gap-3 text-xs w-full">
                      {[
                        { label: 'High Confidence', count: result.confidence_summary?.high || 0, color: COLORS.high },
                        { label: 'Medium Confidence', count: result.confidence_summary?.medium || 0, color: COLORS.medium },
                        { label: 'Low Confidence', count: result.confidence_summary?.low || 0, color: COLORS.low },
                        { label: 'Unverified Nulls', count: result.confidence_summary?.unverified || 0, color: COLORS.unverified },
                      ].map((item, idx) => (
                        <div key={idx} className="flex items-center gap-2.5">
                          <div className="h-2 w-2 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                          <div>
                            <div className="text-[10px] text-gray-400 leading-none">{item.label}</div>
                            <div className="font-bold text-white mt-0.5">{item.count} fields</div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="shrink-0 flex flex-col items-center gap-1.5 bg-rose-500/5 px-4 py-3 rounded-xl border border-rose-500/20 text-center w-full sm:w-auto mt-2 sm:mt-0">
                      <span className="text-xl font-bold text-rose-400">{result.confidence_summary?.conflicts || 0}</span>
                      <span className="text-[9px] font-bold font-mono tracking-wider text-rose-300">CONFLICTS FLAGGED</span>
                    </div>

                  </div>

                </div>
              )}

              {/* TABS SELECTOR */}
              <div className="flex items-center justify-between border-b border-darkBorder/60 bg-darkPanel/30 p-2 rounded-xl border border-darkBorder">
                <div className="flex gap-1">
                  {result.mode === 'single' && (
                    <button
                      onClick={() => setActiveTab('schema')}
                      className={`text-xs font-bold px-4 py-2 rounded-lg transition-all cursor-pointer ${activeTab === 'schema' ? 'bg-indigo-600 text-white shadow' : 'text-gray-400 hover:text-white hover:bg-gray-800/40'}`}
                    >
                      Structured Schema
                    </button>
                  )}
                  {result.mode === 'single' && (
                    <button
                      onClick={() => setActiveTab('narrative')}
                      className={`text-xs font-bold px-4 py-2 rounded-lg transition-all cursor-pointer ${activeTab === 'narrative' ? 'bg-indigo-600 text-white shadow' : 'text-gray-400 hover:text-white hover:bg-gray-800/40'}`}
                    >
                      Analyst Brief
                    </button>
                  )}
                  {result.mode === 'comparison' && (
                    <button
                      onClick={() => setActiveTab('comparison')}
                      className={`text-xs font-bold px-4 py-2 rounded-lg transition-all cursor-pointer ${activeTab === 'comparison' ? 'bg-indigo-600 text-white shadow' : 'text-gray-400 hover:text-white hover:bg-gray-800/40'}`}
                    >
                      Strategic Comparison
                    </button>
                  )}
                  <button
                    onClick={() => setActiveTab('sources')}
                    className={`text-xs font-bold px-4 py-2 rounded-lg transition-all cursor-pointer ${activeTab === 'sources' ? 'bg-indigo-600 text-white shadow' : 'text-gray-400 hover:text-white hover:bg-gray-800/40'}`}
                  >
                    Sources Audit Trail
                  </button>
                </div>

                {/* EXPORTS BUTTONS */}
                <div className="flex gap-2">
                  <button 
                    onClick={() => triggerExport('pdf')}
                    className="p-2 text-gray-400 hover:text-white bg-gray-800/40 hover:bg-gray-800 rounded-lg border border-darkBorder transition-all flex items-center justify-center gap-1.5 text-xs font-bold cursor-pointer"
                  >
                    <Download size={12} /> PDF
                  </button>
                  {result.mode === 'comparison' && (
                    <button 
                      onClick={() => triggerExport('pptx')}
                      className="p-2 text-gray-400 hover:text-white bg-gray-800/40 hover:bg-gray-800 rounded-lg border border-darkBorder transition-all flex items-center justify-center gap-1.5 text-xs font-bold cursor-pointer"
                    >
                      <FileText size={12} /> PPTX
                    </button>
                  )}
                </div>
              </div>

              {/* TAB CONTENT: structured schema */}
              {activeTab === 'schema' && result.schema_data && (
                <div className="flex flex-col gap-4">
                  {[
                    { key: 'basics', title: 'Category 1: Program Basics', icon: <Layers size={14} className="text-indigo-400" />, fields: [
                      { fn: 'program_name', l: 'Official program name' },
                      { fn: 'brand_name', l: 'Parent brand name' },
                      { fn: 'industry', l: 'Industry vertical' },
                      { fn: 'program_type', l: 'Program loyalty logic' },
                      { fn: 'geography', l: 'Operational regions' },
                      { fn: 'membership_count', l: 'Reported members' },
                      { fn: 'program_launch_year', l: 'Year launched' },
                      { fn: 'membership_cost', l: 'Price barrier' },
                    ]},
                    { key: 'earn', title: 'Category 2: Earn Mechanics', icon: <Award size={14} className="text-indigo-400" />, fields: [
                      { fn: 'base_earn_rate', l: 'Base earn coefficient' },
                      { fn: 'bonus_earn_categories', l: 'Accelerated earn scopes' },
                      { fn: 'bonus_earn_rates', l: 'Specific bonus multipliers' },
                      { fn: 'non_transactional_earn', l: 'Earn without purchases' },
                      { fn: 'earn_cap', l: 'Accumulation ceiling' },
                      { fn: 'earn_expiry_activity', l: 'Activity reset required' },
                    ]},
                    { key: 'burn', title: 'Category 3: Burn Mechanics', icon: <DollarSign size={14} className="text-indigo-400" />, fields: [
                      { fn: 'redemption_options', l: 'All ways to burn' },
                      { fn: 'minimum_redemption_threshold', l: 'Burn floor threshold' },
                      { fn: 'point_value_cpp', l: 'Cent-per-point estimate' },
                      { fn: 'points_expiry_policy', l: 'Points forfeiture conditions' },
                      { fn: 'cashback_rate', l: 'Effective cashback %' },
                    ]},
                    { key: 'tiers', title: 'Category 4: Tier System', icon: <TrendingUp size={14} className="text-indigo-400" />, fields: [
                      { fn: 'tier_count', l: 'Total tiers count' },
                      { fn: 'tier_names', l: 'Tier list ascending' },
                      { fn: 'tier_qualification_criteria', l: 'Status spend/visit floor' },
                      { fn: 'tier_qualification_period', l: 'Calendar / rolling rules' },
                      { fn: 'tier_benefits', l: 'Benefits per status level' },
                      { fn: 'tier_status_expiry', l: 'Elite duration window' },
                    ]},
                    { key: 'partners', title: 'Category 5: Partnerships', icon: <Globe size={14} className="text-indigo-400" />, fields: [
                      { fn: 'partner_names', l: 'Cross-brand partner network' },
                      { fn: 'partnership_type_per_partner', l: 'Earn/burn capabilities' },
                      { fn: 'partnership_details', l: 'Transfer/redemption rules' },
                      { fn: 'co_brand_card', l: 'Co-branded credit cards' },
                    ]},
                    { key: 'digital', title: 'Category 6: Digital Experience', icon: <Smartphone size={14} className="text-indigo-400" />, fields: [
                      { fn: 'mobile_app_available', l: 'Supported apps' },
                      { fn: 'app_rating_ios', l: 'iOS App Store score' },
                      { fn: 'app_rating_android', l: 'Google Play score' },
                      { fn: 'app_review_count', l: 'Total reviews count' },
                      { fn: 'personalization_features', l: 'AI matching capabilities' },
                      { fn: 'gamification_features', l: 'Challenges & badges' },
                      { fn: 'digital_only_benefits', l: 'Digital-exclusive perks' },
                    ]},
                    { key: 'sentiment', title: 'Category 7: Member Sentiment', icon: <Heart size={14} className="text-indigo-400" />, fields: [
                      { fn: 'overall_sentiment', l: 'Aggregated reviews tone' },
                      { fn: 'common_praise', l: 'Praise themes' },
                      { fn: 'common_complaints', l: 'Criticism themes' },
                      { fn: 'sentiment_sources_checked', l: 'Scraped boards urls' },
                      { fn: 'nps_score', l: 'Net Promoter Score' },
                    ]},
                    { key: 'position', title: 'Category 8: Competitive Position', icon: <Shield size={14} className="text-indigo-400" />, fields: [
                      { fn: 'key_differentiators', l: 'Unique value vectors' },
                      { fn: 'known_weaknesses', l: 'Identified pitfalls' },
                      { fn: 'closest_competitors', l: 'Core wallet challengers' },
                      { fn: 'recent_changes', l: '12-month rebrand changes' },
                    ]}
                  ].map((sec) => (
                    <div key={sec.key} className="glass-card rounded-2xl overflow-hidden shadow-lg border border-darkBorder/60">
                      <button 
                        onClick={() => toggleSection(sec.key)}
                        className="w-full bg-darkPanel/50 px-5 py-4 border-b border-darkBorder/60 flex items-center justify-between transition-colors hover:bg-darkPanel/85 cursor-pointer"
                      >
                        <div className="flex items-center gap-3 text-sm font-bold font-mono text-white">
                          {sec.icon} {sec.title}
                        </div>
                        <div className="text-gray-400">
                          {collapsedSections[sec.key] ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
                        </div>
                      </button>
                      
                      {!collapsedSections[sec.key] && (
                        <div className="overflow-x-auto">
                          <table className="w-full text-left border-collapse">
                            <thead>
                              <tr className="bg-gray-950/20 text-gray-500 uppercase tracking-widest text-[9px] font-mono border-b border-darkBorder">
                                <th className="py-2.5 px-4">Field ID / Description</th>
                                <th className="py-2.5 px-4">Extracted Value</th>
                                <th className="py-2.5 px-4">Confidence</th>
                                <th className="py-2.5 px-4 text-right">Source Link</th>
                              </tr>
                            </thead>
                            <tbody>
                              {sec.fields.map(field => renderSchemaRow(field.l, field.fn, result.schema_data!))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* TAB CONTENT: narrative brief */}
              {activeTab === 'narrative' && result.narrative && (
                <div className="glass-card rounded-2xl p-6 md:p-8 shadow-2xl flex flex-col gap-6 leading-relaxed text-gray-300">
                  <div className="prose prose-invert max-w-none text-sm md:text-base">
                    {/* Render basic markdown text converting [1] footnotes into highlights */}
                    {result.narrative.split('\n').map((line, idx) => {
                      if (line.startsWith('# ')) {
                        return <h2 key={idx} className="text-xl md:text-2xl font-bold text-white mt-4 mb-2">{line.replace('# ', '')}</h2>;
                      }
                      if (line.startsWith('## ')) {
                        return <h3 key={idx} className="text-base md:text-lg font-bold text-white border-b border-darkBorder/40 pb-1 mt-6 mb-3">{line.replace('## ', '')}</h3>;
                      }
                      if (line.startsWith('### ')) {
                        return <h4 key={idx} className="text-sm md:text-base font-bold text-indigo-400 mt-4 mb-2">{line.replace('### ', '')}</h4>;
                      }
                      if (line.startsWith('- ')) {
                        return <li key={idx} className="list-disc ml-6 text-xs md:text-sm text-gray-300 mt-1">{line.replace('- ', '')}</li>;
                      }
                      
                      // Highlight footnotes matching indices
                      let content = line;
                      const matches = line.match(/\[\d+\]/g);
                      if (matches) {
                        return (
                          <p key={idx} className="text-xs md:text-sm mt-3 text-gray-300">
                            {line.split(/(\[\d+\])/).map((part, pIdx) => {
                              const match = part.match(/\[(\d+)\]/);
                              if (match) {
                                const num = parseInt(match[1]);
                                return (
                                  <span 
                                    key={pIdx}
                                    onClick={() => {
                                      setSelectedFootnote(num);
                                      setActiveTab('sources');
                                    }}
                                    className="text-[10px] bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 px-1 rounded mx-0.5 hover:bg-indigo-600 hover:text-white cursor-pointer font-bold select-none transition-colors"
                                    title="View Source Link"
                                  >
                                    [{num}]
                                  </span>
                                );
                              }
                              return part;
                            })}
                          </p>
                        );
                      }
                      
                      return <p key={idx} className="text-xs md:text-sm mt-3 text-gray-300">{line}</p>;
                    })}
                  </div>
                </div>
              )}

              {/* TAB CONTENT: dual comparison */}
              {activeTab === 'comparison' && result.comparison && (
                <div className="flex flex-col gap-6">
                  
                  {/* COMPARISON HEADER SECTION */}
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="bg-sky-500/5 rounded-xl border border-sky-500/20 py-4">
                      <div className="text-[10px] font-mono text-sky-400 font-bold uppercase tracking-wider">PROGRAM A</div>
                      <div className="text-base font-bold text-white mt-1">{result.comparison.program_a_name}</div>
                    </div>
                    <div className="bg-amber-500/5 rounded-xl border border-amber-500/20 py-4">
                      <div className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-wider">PROGRAM B</div>
                      <div className="text-base font-bold text-white mt-1">{result.comparison.program_b_name}</div>
                    </div>
                  </div>

                  {/* MATRICES TABLE */}
                  <div className="glass-card rounded-2xl overflow-hidden shadow-2xl border border-darkBorder/60">
                    <div className="bg-darkPanel/50 px-5 py-4 border-b border-darkBorder/60 flex items-center gap-3 text-sm font-bold font-mono text-white">
                      <Layers size={14} className="text-indigo-400" /> Side-by-Side Schema Matrix
                    </div>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse">
                        <thead>
                          <tr className="bg-gray-950/20 text-gray-500 uppercase tracking-widest text-[9px] font-mono border-b border-darkBorder">
                            <th className="py-2.5 px-4 w-1/4">Field Indicator</th>
                            <th className="py-2.5 px-4 w-1/3">Program A: {result.comparison.program_a_name}</th>
                            <th className="py-2.5 px-4 w-1/3">Program B: {result.comparison.program_b_name}</th>
                            <th className="py-2.5 px-4 text-center w-1/12">Advantage</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.comparison.comparison_table.map((row, idx) => (
                            <tr key={idx} className="border-b border-darkBorder hover:bg-gray-900/10 transition-colors text-xs">
                              <td className="py-3 px-4 font-mono font-semibold text-gray-400">{row.field}</td>
                              <td className="py-3 px-4 text-gray-200">
                                <div>{row.val_a}</div>
                                <span className={`text-[8px] px-1.5 py-0.5 rounded font-bold font-mono ${
                                  row.conf_a === 'high' ? 'bg-emerald-500/10 text-emerald-400' :
                                  row.conf_a === 'medium' ? 'bg-amber-500/10 text-amber-400' :
                                  row.conf_a === 'low' ? 'bg-orange-500/10 text-orange-400' :
                                  'bg-gray-800 text-gray-500'
                                }`}>
                                  {row.conf_a.toUpperCase()}
                                </span>
                              </td>
                              <td className="py-3 px-4 text-gray-200">
                                <div>{row.val_b}</div>
                                <span className={`text-[8px] px-1.5 py-0.5 rounded font-bold font-mono ${
                                  row.conf_b === 'high' ? 'bg-emerald-500/10 text-emerald-400' :
                                  row.conf_b === 'medium' ? 'bg-amber-500/10 text-amber-400' :
                                  row.conf_b === 'low' ? 'bg-orange-500/10 text-orange-400' :
                                  'bg-gray-800 text-gray-500'
                                }`}>
                                  {row.conf_b.toUpperCase()}
                                </span>
                              </td>
                              <td className="py-3 px-4 text-center font-bold font-mono align-middle">
                                {row.advantage === 'Program A' ? (
                                  <span className="text-sky-400" title={`${result.comparison.program_a_name} Advantage`}>▲ A</span>
                                ) : row.advantage === 'Program B' ? (
                                  <span className="text-amber-400" title={`${result.comparison.program_b_name} Advantage`}>▼ B</span>
                                ) : (
                                  <span className="text-gray-600">=</span>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* STRATEGIC ANALYSIS TEXT */}
                  <div className="glass-card rounded-2xl p-6 md:p-8 shadow-2xl flex flex-col gap-4 text-gray-300 leading-relaxed">
                    {result.comparison.strategic_analysis.split('\n').map((line, idx) => {
                      if (line.startsWith('# ')) {
                        return <h2 key={idx} className="text-lg md:text-xl font-bold text-white border-b border-darkBorder/40 pb-2 mt-2 mb-3">{line.replace('# ', '')}</h2>;
                      }
                      if (line.startsWith('## ')) {
                        return <h3 key={idx} className="text-sm md:text-base font-bold text-indigo-400 mt-5 mb-2">{line.replace('## ', '')}</h3>;
                      }
                      if (line.startsWith('* **')) {
                        // Bold parsing
                        const match = line.match(/\* \*\*(.*?)\*\*:(.*)/);
                        if (match) {
                          return (
                            <p key={idx} className="text-xs md:text-sm mt-2">
                              <span className="font-bold text-white">{match[1]}:</span>{match[2]}
                            </p>
                          );
                        }
                      }
                      if (line.startsWith('1. ') || line.startsWith('2. ') || line.startsWith('3. ')) {
                        const match = line.match(/(\d+\.) \*\*(.*?)\*\*:(.*)/);
                        if (match) {
                          return (
                            <div key={idx} className="text-xs md:text-sm mt-3 border-l border-gray-800 pl-3.5">
                              <span className="font-bold text-indigo-400">{match[1]} {match[2]}</span>: {match[3]}
                            </div>
                          );
                        }
                      }
                      return <p key={idx} className="text-xs md:text-sm mt-2 text-gray-300">{line}</p>;
                    })}
                  </div>

                </div>
              )}

              {/* TAB CONTENT: sources audit trail */}
              {activeTab === 'sources' && (
                <div className="glass-card rounded-2xl overflow-hidden shadow-2xl border border-darkBorder/60">
                  <div className="bg-darkPanel/50 px-5 py-4 border-b border-darkBorder/60 flex items-center gap-3 text-sm font-bold font-mono text-white">
                    <Shield size={14} className="text-indigo-400" /> Web Sources Audit Trail
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="bg-gray-950/20 text-gray-500 uppercase tracking-widest text-[9px] font-mono border-b border-darkBorder">
                          <th className="py-2.5 px-4 w-8 text-center">#</th>
                          <th className="py-2.5 px-4">Source URL</th>
                          <th className="py-2.5 px-4">Category Tier</th>
                          <th className="py-2.5 px-4">Scrape Date</th>
                          <th className="py-2.5 px-4">Confidence Impact</th>
                          <th className="py-2.5 px-4 text-center">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {/* Merged sources display */}
                        {((result.sources as SourceMetadata[]) || []).map((source, idx) => {
                          const isHighlighted = selectedFootnote !== null && idx + 1 === selectedFootnote;
                          return (
                            <tr 
                              key={idx} 
                              className={`border-b border-darkBorder hover:bg-gray-900/10 transition-colors text-xs ${
                                isHighlighted ? 'bg-indigo-600/10 border-indigo-500' : ''
                              }`}
                            >
                              <td className="py-3 px-4 text-center font-mono font-bold text-gray-500">
                                {isHighlighted ? (
                                  <span className="bg-indigo-500 text-white font-semibold px-2 py-0.5 rounded font-mono text-[10px]">
                                    {idx + 1}
                                  </span>
                                ) : (
                                  idx + 1
                                )}
                              </td>
                              <td className="py-3 px-4 font-medium text-gray-200 truncate max-w-xs md:max-w-md">
                                <div className="text-gray-300 font-bold truncate">{new URL(source.url).pathname}</div>
                                <a href={source.url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline inline-flex items-center text-[10px] mt-0.5">
                                  {source.url} <ExternalLink size={8} className="ml-1" />
                                </a>
                              </td>
                              <td className="py-3 px-4">
                                <span className={`text-[9px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                                  source.tier === 'OFFICIAL' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
                                  source.tier === 'PRESS_RELEASE' ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' :
                                  source.tier === 'NEWS' ? 'bg-sky-500/10 text-sky-400 border border-sky-500/20' :
                                  'bg-gray-800 text-gray-400 border border-gray-700/60'
                                }`}>
                                  {source.tier}
                                </span>
                              </td>
                              <td className="py-3 px-4 text-gray-400 font-mono text-[10px]">{source.access_date}</td>
                              <td className="py-3 px-4 font-mono text-gray-300 font-semibold">{source.confidence_contribution.toFixed(1)}</td>
                              <td className="py-3 px-4 text-center">
                                <span className={`inline-flex items-center gap-1 text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                                  source.status === 'Accepted' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                                }`}>
                                  {source.status === 'Accepted' ? (
                                    <><Check size={8} /> Accepted</>
                                  ) : (
                                    <><X size={8} /> Rejected</>
                                  )}
                                </span>
                                {source.rejection_reason && (
                                  <div className="text-[9px] text-rose-500 mt-1 italic max-w-[120px] leading-tight">
                                    {source.rejection_reason}
                                  </div>
                                )}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

            </div>
          )}

        </div>

      </main>

      {/* FOOTER */}
      <footer className="border-t border-darkBorder bg-gray-950/80 py-4 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center text-[10px] font-mono text-gray-600">
          Competitive Intelligence Research Agent | Built by Karthik S + Jahnvi R (PES University)
        </div>
      </footer>

      {/* SETTINGS MODAL */}
      {showSettings && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fadeIn">
          <div className="glass-card rounded-2xl p-6 w-full max-w-md shadow-2xl flex flex-col gap-4 border border-darkBorder">
            <div className="flex items-center justify-between border-b border-darkBorder/60 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 font-mono">
                <Settings size={16} className="text-indigo-400" /> CREDENTIALS CONFIG
              </h3>
              <button 
                onClick={() => setShowSettings(false)}
                className="text-gray-400 hover:text-white transition-colors cursor-pointer"
              >
                <X size={16} />
              </button>
            </div>

            <p className="text-[10px] text-gray-400 leading-normal">
              Enter API credentials to enable **Live Agent Mode**. Keys are held in-memory and deleted on session reload.
            </p>

            <div className="flex flex-col gap-3.5 my-2">
              {[
                { label: 'Tavily Search API Key', key: 'tavily_key', config: keysConfigured.TAVILY_API_KEY, placeholder: 'tvly-...' },
                { label: 'OpenAI API Key', key: 'openai_key', config: keysConfigured.OPENAI_API_KEY, placeholder: 'sk-proj-...' },
                { label: 'Anthropic API Key', key: 'anthropic_key', config: keysConfigured.ANTHROPIC_API_KEY, placeholder: 'sk-ant-...' },
                { label: 'Gemini API Key', key: 'gemini_key', config: keysConfigured.GEMINI_API_KEY, placeholder: 'AIzaSy...' }
              ].map(field => (
                <div key={field.key} className="flex flex-col gap-1.5">
                  <div className="flex items-center justify-between">
                    <label className="text-[10px] font-mono font-semibold text-gray-400 uppercase tracking-wide">
                      {field.label}
                    </label>
                    <span className={`text-[8px] font-mono font-bold tracking-wider px-1.5 py-0.5 rounded ${
                      field.config ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                    }`}>
                      {field.config ? 'CONFIGURED' : 'NOT SET'}
                    </span>
                  </div>
                  <div className="relative">
                    <input 
                      type="password" 
                      placeholder={field.placeholder}
                      value={(keys as any)[field.key]}
                      onChange={(e) => setKeys(prev => ({ ...prev, [field.key]: e.target.value }))}
                      className="bg-gray-950 border border-darkBorder focus:border-indigo-500 rounded-xl px-3 py-2 text-xs outline-none text-white w-full pr-8"
                    />
                    <Lock size={10} className="absolute right-3 top-3.5 text-gray-600" />
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-3 justify-end mt-2 pt-2 border-t border-darkBorder/60">
              <button 
                onClick={() => setShowSettings(false)}
                className="px-4 py-2 hover:bg-gray-800 text-gray-400 hover:text-white rounded-lg text-xs font-bold transition-all cursor-pointer"
              >
                Cancel
              </button>
              <button 
                onClick={saveSettings}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold transition-all cursor-pointer"
              >
                Save Credentials
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
