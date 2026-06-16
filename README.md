# Autonomous Competitive Intelligence Research Agent
## Team Styles | PES University

An autonomous, source-verified loyalty program competitive research agent. Given only a program or brand name, the system discovers sources, scrapes terms and FAQs, runs fingerprint filtering, resolves conflicts, and generates structured profiles (35+ fields) alongside strategic narratives and comparisons.

```
User Query → [1] Orchestrator → [2] Retriever (4 parallel agents) → [3] Extractor → [4] Verifier → [5] Narrator → [6] Comparator → Final Report
```

---

## Features & Implementation Highlights

1. **6-Component Pipeline Architecture**:
   - **Orchestrator (Planner)**: Decomposes target programs, runs sub-agents in parallel, and coordinates comparison workflows.
   - **Retriever**:
     - *Search Agent*: Categorized, targeted search queries.
     - *Scraper Agent*: Fetches raw web content, running fingerprint checks to validate relevance.
     - *News Agent*: Tracks recent 12-month press releases/updates.
     - *Sentiment Agent*: Gathers App Store, Google Play, Trustpilot, and Reddit reviews.
   - **Extractor**: Searches vector store (Qdrant) and parses values from scraped content.
   - **Verifier (Jahnvi's Layer)**: Checks domain authority, runs Company Fingerprint filters, clusters matching entities, and detects data conflicts.
   - **Narrator**: Generates footnote-cited client briefs in analyst voice.
   - **Comparator**: Performs dual matrix comparison with dynamic relative advantage markings.

2. **Jahnvi's Confidence Scoring System**:
   - Official Program Site/App: `3.0` weight
   - Official Press Release: `2.0` weight
   - Major News Outlets (Reuters, WSJ, Bloomberg): `1.5` weight
   - Industry Publications (Loyalty360, Points Guy): `1.2` weight
   - App Store Listing (Apple/Google): `1.0` weight
   - Review Aggregators (Trustpilot, G2): `0.7` weight
   - Reddit / Forums / Social Media: `0.5` weight
   - **Confidence Tiers**:
     - **HIGH**: Score $\ge 4.0$ (typically 2+ official sources agree).
     - **MEDIUM**: Score $2.0$ to $3.9$ (cross-verified).
     - **LOW**: Score $< 2.0$ (single source only).
     - **UNVERIFIED**: Marked `null` (never fabricated).

3. **User Credentials Control Drawer**:
   - Supports in-memory storage of `TAVILY_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GEMINI_API_KEY` for live research mode.
   - Pre-cached high-fidelity profiles for popular programs (**Starbucks Rewards**, **McDonald's MyMcDonald's Rewards**, **Sephora Beauty Insider**, **Marriott Bonvoy**, and **Delta SkyMiles**) to support instant offline validation and demos.

---

## Directory Structure

```
├── backend/
│   ├── main.py            # FastAPI application endpoints
│   ├── pipeline.py        # 6-agent orchestration pipeline logic
│   ├── schema.py          # Pydantic schema mappings for the 45 fields
│   ├── cached_data.py     # Pre-cached loyalty program profiles
│   ├── test_pipeline.py   # Logical test script
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # React client console dashboard
│   │   ├── index.css      # Core styles & Tailwind directives
│   │   └── main.tsx       # React mounting entrypoint
│   ├── package.json       # Node dependency descriptors
│   ├── tailwind.config.js # Tailwind CSS setup
│   └── postcss.config.js  # PostCSS bundler pipeline config
├── run.bat                # Windows one-click startup script
└── README.md              # Documentation
```

---

## Setup & Execution

### Option A: One-Click Startup (Windows)
Double-click the **`run.bat`** script at the root of the workspace.
This will:
1. Install backend requirements via `pip`.
2. Start the FastAPI backend server in a separate terminal window.
3. Start the React/Vite development server in another terminal window.
4. Launch your default browser to: **`http://localhost:5173`**

### Option B: Manual CLI Startup

#### 1. Start FastAPI Backend:
```bash
# Navigate to backend and install packages
cd backend
pip install -r requirements.txt

# Start the server (runs on port 8000)
python main.py
```

#### 2. Start Vite React Frontend:
```bash
# Navigate to frontend and install packages
cd frontend
npm install

# Start the development server (runs on port 5173)
npm run dev
```

---

## Logical Verification Tests
To run the logical verification tests and assert the scoring formulas:
```bash
python backend/test_pipeline.py
```
This ensures the confidence algorithm, fingerprint matcher, and source classification models are running with absolute mathematical consistency.
