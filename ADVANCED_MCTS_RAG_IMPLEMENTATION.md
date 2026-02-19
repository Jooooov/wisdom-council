# Advanced Multi-Agent MCTS + RAG System
## For Claude Sonnet 4.6 Implementation Planning

**Status**: Planning Phase
**Target Environment**: MacBook Air M4, 16GB RAM
**Model**: Qwen3-4B-MLX-4bit (sequential execution)
**Framework**: LangGraph + MCTS + RAG

---

## 📋 PROJECT CONTEXT FOR CLAUDE.COM

### Your Current System (His Dark Materials - Wisdom Council v2)

You have a working multi-agent system:

**8 Agents** (all with learning/memory):
- Lyra (Analyst) - Metrics, patterns, business
- Iorek (Architect) - Design, scalability
- Marisa (Developer) - Code optimization
- Serafina (Researcher) - Best practices
- Lee (Writer) - Documentation
- Coram (Validator) - Testing, risks
- Asriel (Coordinator) - Strategy
- Mary (Tools Manager) - Context keeper

**Working Infrastructure**:
- Hybrid Memory System (RAG + Graph + Patterns)
- War Room (Agent discussion via LLM)
- Context Analyzer (Project type detection)
- Mary's Context Injection (temporal + tech versions)
- RAM Guardian (pre-startup safety)
- Obsidian Vault integration

**Location**: `~/Desktop/apps/His Dark Materials/`

**Reusable Patterns** (DON'T rebuild):
1. Agent dataclass with learning_score
2. RAG memory with keyword-matching (no vector DB needed)
3. Orchestrator pattern (task assignment by specialization)
4. War Room for LLM-based agent discussion
5. Context analyzer with regex patterns
6. Mary as "Living Context Keeper"

---

## 🎯 NEW PHASE: Advanced Reasoning Layer

### Problem to Solve

Current Wisdom Council is **good for analysis** but **limited in reasoning depth**:
- Single-pass analysis per agent
- No explicit reasoning tree exploration
- Sequential execution (1 agent at a time)
- No backtracking when reasoning fails

**Goal**: Add reasoning capabilities while respecting 16GB RAM + 4B model constraints.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────┐
│  ADVANCED REASONING LAYER (NEW)             │
├─────────────────────────────────────────────┤
│ ┌──────────────────────────────────────┐   │
│ │  MCTS Tree Search                    │   │
│ │  ├─ Generate 4 reasoning branches    │   │
│ │  ├─ Score each (0-1)                 │   │
│ │  ├─ Expand top-2 (backtracking)      │   │
│ │  └─ Final path selection             │   │
│ └──────────────────────────────────────┘   │
│          ↓                                  │
│ ┌──────────────────────────────────────┐   │
│ │  Reasoning Agent (via Qwen3-4B)      │   │
│ │  ├─ Long CoT (chain-of-thought)      │   │
│ │  ├─ Step-by-step reasoning           │   │
│ │  └─ Explicit uncertainty marking     │   │
│ └──────────────────────────────────────┘   │
│          ↓                                  │
│ ┌──────────────────────────────────────┐   │
│ │  Dynamic Routing                     │   │
│ │  ├─ Route to specialized agent       │   │
│ │  ├─ Parallel when possible           │   │
│ │  └─ Serialize when memory constrained│   │
│ └──────────────────────────────────────┘   │
│          ↓                                  │
│ ┌──────────────────────────────────────┐   │
│ │  Experiential Memory                 │   │
│ │  ├─ Store reasoning paths            │   │
│ │  ├─ Retrieve similar past steps      │   │
│ │  └─ Learn from previous decisions    │   │
│ └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│  EXISTING WISDOM COUNCIL (keep as-is)       │
│  ├─ 8 Agents                                │
│  ├─ War Room discussion                     │
│  ├─ Hybrid memory (RAG + Graph)             │
│  └─ Obsidian integration                    │
└─────────────────────────────────────────────┘
```

---

## 🎭 Agent Roles (Themed)

Keep similar to Wisdom Council but adapted for reasoning:

### Lyra (Exploradora) - Initial Idea Generation
- **Input**: Business idea / problem statement
- **Process**:
  - Generate 4 creative initial approaches
  - Flag assumptions explicitly
  - Rate confidence (0-1)
- **Output**: JSON with branches + uncertainty

### Will (Executor) - Practical Validation
- **Input**: Lyra's branches
- **Process**:
  - Check feasibility of each approach
  - Fact-check against RAG memory
  - Identify practical constraints
- **Output**: Validation score + blockers

### Mrs. Coulter (Crítica) - Adversarial Review
- **Input**: Current reasoning path
- **Process**:
  - Devil's advocate perspective
  - Find hidden risks/assumptions
  - Suggest counter-arguments
- **Output**: Risk assessment + alternative angles

### Iorek (Analista) - Financial/Math
- **Input**: Validated approach
- **Process**:
  - Calculate ROI / costs
  - Model scenarios (best/mid/worst case)
  - Quantify impact
- **Output**: Financial projections + confidence

### Meta-Daemon (Orquestrador) - Decision Node
- **Input**: All agent outputs
- **Process**:
  - Decides if MCTS should expand or backtrack
  - Routes to next phase
  - Manages tree depth
- **Output**: Next action (expand/collapse/output)

---

## 🧠 MCTS Tree Search (Simplified for 4B Model)

### Algorithm

```
MCTS(business_idea, max_depth=3, branches_per_node=4):

  1. ROOT NODE = business_idea

  2. EXPAND PHASE:
     - Lyra generates 4 branches (reasoning paths)
     - Each branch = different approach/assumption set

  3. SIMULATION PHASE (per branch):
     - Will validates practical feasibility
     - Mrs. Coulter identifies risks
     - Iorek calculates ROI
     - Get score = (feasibility + ROI + risk_mitigation) / 3

  4. BACKPROPAGATION:
     - Top-2 scoring branches → expand deeper
     - Low-scoring → prune (save RAM)

  5. REPEAT: Up to max_depth (e.g., 3 levels deep)

  6. OUTPUT:
     - Full tree as JSON
     - Best path highlighted
     - Decision rationale
```

### Memory Management (Critical!)

```
Per iteration:
- Qwen3-4B context: 4k-8k tokens
- Only keep active branches in memory
- Archive explored paths to disk
- Use "reasoning state" files:
  ~/.mcts_reasoning/
  ├─ tree_structure.json
  ├─ node_scores.json
  └─ explored_paths.jsonl
```

---

## 💾 Experiential Memory for Reasoning

### Store What Works

When a reasoning path succeeds:
```json
{
  "step_id": "business_analysis_001",
  "business_type": "SaaS",
  "input_description": "...",
  "reasoning_path": [
    {"agent": "Lyra", "thought": "...", "branches": 4},
    {"agent": "Will", "verdict": "feasible", "blockers": []},
    {"agent": "Iorek", "roi_3y": 2.5, "confidence": 0.85}
  ],
  "final_decision": "GO",
  "confidence": 0.92,
  "timestamp": "2026-02-19"
}
```

### Retrieve Similar Paths

When new business arrives:
```python
# Find past reasoning steps with similar context
similar_steps = memory.search(
  query="business_type:SaaS confidence>0.8",
  limit=3
)

# Inject as "reasoning prompts" to Qwen3
# "Here's how we analyzed similar cases..."
```

---

## 🔄 Dynamic Routing

### Sequential vs Parallel

```python
# Check available RAM before each phase
if available_ram > 8GB:
    # Can run multiple agents in parallel
    parallel_execution(will, coulter, iorek)
else:
    # Must serialize (1 agent at a time)
    execute_sequentially([will, coulter, iorek])
```

### Context Switching

- After each agent's analysis, save state to disk
- Load next agent's context fresh (prevents memory bloat)
- Reuse "meta-daemon" to decide routing

---

## 📊 Business Viability Analysis (Example Use Case)

### Input
```
Business Idea: "AI-powered tool for analyzing Reddit discussions
in real-time, generating market insights for crypto traders"

Constraints:
- Budget: $50k initial
- Team: 2-3 people
- Timeline: 6 months to MVP
```

### MCTS Process

**Level 0 (Root)**: The idea

**Level 1 (Lyra generates 4 branches)**:
1. Branch A: "Direct API → dashboard" (simplest)
2. Branch B: "Agent-based analysis" (most intelligent)
3. Branch C: "Hybrid (quick MVP + agent later)"
4. Branch D: "White-label for exchanges"

**Level 2 (Will + Mrs. Coulter + Iorek evaluate each)**:

Branch A:
- Will: ✓ Feasible, requires Reddit API keys
- Mrs. Coulter: ⚠️ Risk = crypto regulation + API changes
- Iorek: ROI 1.8x in 2 years, $12k dev cost
- Score: 0.72

Branch B:
- Will: ✓ Feasible with Qwen3-4B local
- Mrs. Coulter: ⚠️ Risk = model accuracy + latency
- Iorek: ROI 3.2x in 2 years, $35k dev cost
- Score: 0.81 ← TOP

Branch C:
- Will: ✓✓ Most feasible (phased approach)
- Mrs. Coulter: ✓ Mitigates most risks
- Iorek: ROI 2.8x, $18k phase 1
- Score: 0.88 ← BEST

Branch D:
- Will: ⚠️ Requires partnership agreements
- Mrs. Coulter: ⚠️ Market saturation in exchange APIs
- Iorek: ROI 2.1x, $40k to build
- Score: 0.65

**Level 3 (Expand top-2: C and B)**:

Branch C, Sub-1 (MVP Phase):
- Validate with small trader cohort
- Score: 0.85

Branch C, Sub-2 (Full Phase):
- Scale to 1000s of traders
- Score: 0.91

**Final Output**:
```json
{
  "recommendation": "STRONGLY GO",
  "confidence": 0.91,
  "best_path": "Branch C (Hybrid) → MVP Phase → Scale Phase",
  "financial_projection": {
    "year_1": "$0 (dev)",
    "year_2": "$90k revenue",
    "year_3": "$360k revenue"
  },
  "key_risks": [
    "API rate limiting (mitigation: batch queries)",
    "Regulatory: Monitor SEC/CFTC crypto rules"
  ],
  "team_requirements": ["Python dev", "Crypto domain knowledge"],
  "timeline": "Phase 1: 8 weeks, Phase 2: 12 weeks"
}
```

---

## 📁 File Structure (Modular)

```
~/Desktop/apps/His Dark Materials/
├── core/
│   ├── reasoning/                    ← NEW
│   │   ├── mcts_tree.py              (Tree node, expand, score)
│   │   ├── reasoning_agent.py        (CoT + step-by-step)
│   │   ├── dynamic_router.py         (Sequential vs parallel)
│   │   └── reasoning_memory.py       (Store/retrieve reasoning paths)
│   │
│   ├── agents/
│   │   └── __init__.py               (REUSE + add new agents)
│   │
│   ├── analysis/                     (REUSE existing)
│   ├── memory/                       (REUSE existing)
│   ├── obsidian/                     (REUSE existing)
│   └── llm/                          (REUSE existing)
│
├── advanced_reasoning.py             ← NEW (main entry point)
├── config_reasoning.yaml             ← NEW (MCTS depth, branches, etc.)
└── examples/
    └── business_viability_example.py ← NEW (end-to-end example)
```

---

## 🎯 Implementation Phases

### Phase 1: Core MCTS + Qwen3 Integration (2-3 days)
- [ ] MCTS tree structure (nodes, branches, scoring)
- [ ] Reasoning agent with Qwen3-4B + CoT prompts
- [ ] Memory management (state to disk)
- [ ] Basic dynamic routing (sequential first)

### Phase 2: Agent Integration (2-3 days)
- [ ] Lyra: Branch generation (4 approaches)
- [ ] Will: Practical validation
- [ ] Mrs. Coulter: Risk identification
- [ ] Iorek: Financial modeling
- [ ] Meta-Daemon: Routing decisions

### Phase 3: Experiential Memory (2 days)
- [ ] Store reasoning paths (JSON)
- [ ] Retrieve similar past steps
- [ ] Inject as prompts to Qwen3
- [ ] Learning feedback loop

### Phase 4: End-to-End Testing (1-2 days)
- [ ] Example: Business viability analysis
- [ ] RAM profiling (ensure <8GB at peak)
- [ ] Output: JSON tree + recommendation
- [ ] Obsidian integration (optional)

---

## 🔧 Technical Constraints & Solutions

| Constraint | Problem | Solution |
|-----------|---------|----------|
| **4B Model** | Limited reasoning in one pass | MCTS explores multiple paths → combine insights |
| **16GB RAM** | Can't load big embeddings/vector DB | Keyword-matching RAG (lightweight) |
| **Sequential** | Slow if run agents one-by-one | RAM check → serialize when needed |
| **Low latency needed?** | Qwen3 is slow | Accept 5-10 min per analysis (tree search) |
| **Long context** | Need reasoning history | Save state to disk, load fresh per iteration |

---

## ✅ Deliverables

1. **MCTS Tree Search**: Generate 4 branches, score, expand top-2
2. **Reasoning Agent**: Qwen3-4B with long CoT + uncertainty marking
3. **4 Specialized Agents**: Lyra, Will, Mrs. Coulter, Iorek (themed)
4. **Experiential Memory**: Store/retrieve reasoning paths
5. **Dynamic Routing**: RAM-aware parallel/sequential execution
6. **End-to-End Example**: Business viability with full JSON output
7. **Modular Code**: Easy to extend (add agents, modify MCTS depth, etc.)

---

## 🚀 Success Criteria

- ✅ Runs on 16GB MacBook Air M4
- ✅ MCTS explores 3 levels × 4 branches = reasonable tree
- ✅ Qwen3-4B produces coherent reasoning (no hallucinations)
- ✅ Outputs structured JSON with decision + confidence
- ✅ Memory persists across runs (learning)
- ✅ Analysis completes in < 10 min per business idea
- ✅ Code is modular (add new agents/change MCTS depth easily)

---

## 📚 References from Existing Code

You can copy these patterns:
- **Agent Dataclass**: `core/agents/__init__.py` (has learning_score)
- **Memory System**: `core/memory/hybrid_memory.py` (RAG + Graph)
- **Context Injection**: `core/research/mary_context.py` (temporal + guidelines)
- **War Room**: `core/orchestration/war_room.py` (agent discussion)
- **RAM Manager**: `core/llm/ram_manager.py` (safety checks)

---

## 🎓 Key Design Decisions

1. **Use MCTS, not transformer-based planning**: MCTS is simpler, more interpretable, doesn't need huge context
2. **Keyword RAG, not vector embeddings**: Saves RAM, faster, good enough for this use case
3. **Sequential agents, not true parallelism**: Simplifies coordination, RAM-friendly
4. **Disk persistence for state**: Let tree search run 10 mins without crashing
5. **Themed agents (Lyra, Will, etc.)**: Makes outputs less robotic, easier to audit decisions
6. **Confidence scores everywhere**: So user knows how much to trust each recommendation

---

## 💡 Next: Ready for Implementation

**You now have**:
1. Clear architecture (MCTS + agents + memory)
2. Themed agent roles (Lyra, Will, Mrs. Coulter, Iorek)
3. Example use case (business viability)
4. Modular structure (reuse existing code)
5. Constraints handled (16GB RAM, 4B model)

**Next step**: Copy this document to claude.com + Sonnet 4.6 and ask for:
> "Implement Phase 1 + Phase 2 (MCTS + agents integration), with focus on:
> - Code modularity (I'll add more agents later)
> - RAM efficiency (target: <8GB at peak)
> - Clear prompts for Qwen3 CoT reasoning
> - Example end-to-end: business viability analysis"

---

**Ready to build! 🚀**
