# 🧙‍♂️ The Wisdom Council v2

**Real Multi-Agent System for Business Project Analysis**

[![GitHub](https://img.shields.io/badge/GitHub-Jooooov%2Fwisdom--council-blue?logo=github)](https://github.com/Jooooov/wisdom-council)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](#status)
[![Real Analysis](https://img.shields.io/badge/Analysis-Real%20Code-red)](#real-analysis-new)

A multi-agent system that analyzes **9 real business projects** with **7 specialized agents** using real code analysis (MLX + Qwen3) and web research (Perplexity MCP).

---

## 🚀 Quick Start

### Option 1: Interactive Menu
```bash
python3 ~/Desktop/Apps/His\ Dark\ Materials/run.py
```

### Option 2: macOS Double-Click
```
Finder → Desktop → Apps → His Dark Materials → run.command
```

### Option 3: Real Code Analysis (NEW! ⭐)
```bash
python3 ~/Desktop/Apps/His\ Dark\ Materials/analyze_with_mcps.py
```

---

## ✨ What's New in v2

### Real Analysis (Not Generic Advice)
- ✅ **Reads actual code** using MLX local LLM (Qwen3)
- ✅ **Identifies specific problems** with file names and line numbers
- ✅ **Researches context** using Perplexity MCP (web search)
- ✅ **Saves findings** to Obsidian automatically
- ✅ **Provides actionable fixes** with time estimates

### 7 Specialized Agents
Each with real expertise and learning memory:

| Agent | Role | Specialties |
|-------|------|------------|
| **Lyra** 📊 | Analyst | Metrics, quality analysis, patterns |
| **Iorek** 🏗️ | Architect | Design, scalability, integration |
| **Marisa** 💻 | Developer | Code review, performance, optimization |
| **Serafina** 🔬 | Researcher | Best practices, research, investigation |
| **Lee** 📝 | Writer | Documentation, synthesis, communication |
| **Pantalaimon** ✅ | Tester | Quality, testing, validation |
| **Philip** 🎯 | Coordinator | Execution, priorities, resources |

---

## 🔬 Real Analysis (NEW!)

### What It Does
Instead of generic advice like "add tests", it:
- Reads actual Python code using MLX
- Identifies specific problems with line numbers
- Researches context with Perplexity MCP
- Saves findings to Obsidian automatically

### Example Output
```
CRITICAL ISSUES FOUND:
- cli.py line 16-23: Cancer types hardcoded
  → Can't add new types without code change
  → Fix: Load from config.yaml
  → Time: 5 minutes
  → Impact: 10x more scalable

PERFORMANCE ISSUES:
- cli.py line 156: Sequential API calls
  → Fetches papers one by one
  → Fix: Use async/await
  → Time: 3 hours
  → Impact: 3x faster

ACTIONABLE RECOMMENDATIONS:
1. Load cancer types from config (5 min)
2. Implement parallel fetching (3 hours)
3. Add search caching (1 hour)
```

### How to Use
```bash
python3 analyze_with_mcps.py

# 1. Checks tools (MLX + MCPs)
# 2. Lists projects
# 3. You select one
# 4. MLX analyzes code
# 5. Perplexity researches context
# 6. Results saved to Obsidian
```

---

## 📁 9 Projects Analyzed

### Executable (~/Desktop/Apps/)
1. **His Dark Materials** - This agent system
2. **MundoBarbaroResearch** - Research pipeline
3. **WisdomOfReddit** - Intelligence system
4. **CrystalBall** - Predictions engine

### Documentation (~/Obsidian-Vault/1 - Projectos/)
1. **Chemetil** - Business strategy
2. **WisdomOfReddit** - Knowledge base
3. **MundoBarbaroResearch** - Research docs
4. **RedditScrapper** - Data collection
5. **AgentsAI** - Learning materials

---

## 🔌 MCP Integration

### Available Tools
- **MLX (Qwen3):** Local code analysis (no API costs)
- **Perplexity MCP:** Web research (port 3007)
- **Obsidian MCP:** Save findings (port 3001)
- **Paper Search MCP:** Academic papers (port 3003)

### What MCPs Do
- MLX: Analyzes code locally with Qwen3
- Perplexity: Searches web for context
- Obsidian: Automatically saves analysis
- Paper Search: Finds academic sources

---

## 🎮 Interactive Menu

When you run the system, you get:

1. **Show system status** - See all agents and memory stats
2. **List available projects** - Discover your real projects
3. **Have agents work on a project** - Assign work
4. **View agent learning history** - See what they've learned
5. **View memory & experiences** - Overall system learning

---

## 💾 Learning System

Agents record experiences and improve over time:

- **Experience Recording:** Every completed task is recorded
- **Success Rate:** Tracked per agent
- **Learning Score:** Increases with each successful task
- **Memory File:** Stored at `~/.wisdom_council/memory.json`

---

## 📊 Project Analysis

When agents work on a project, they:

1. **Analyze** the project structure and purpose
2. **Create a task** for detailed work
3. **Assign** to the best agent based on skills
4. **Complete** and record the experience
5. **Learn** from the outcome

---

## 🔄 Architecture

```
core/
├── agents/          - 7 agents with skills
├── tasks/           - Task management
├── memory/          - Learning & experiences
└── INTEGRATION/     - Project discovery
    └── file_sync.py - Finds real projects
```

---

## 📚 Project Output Support

If your projects have output folders (`OUTPUT/`, `outputs/`, `resources/`), the system detects and tracks them.

**Examples:**
- Crystal Ball outputs → agents can access results
- Wisdom of Reddit data → agents can read analyses

---

## 🎓 Example Workflow

1. Run the system
2. Choose option `2` - List projects
3. See "WisdomOfReddit" (Obsidian project)
4. Choose option `3` - Have agents work on it
5. Lyra (Analyst) is assigned
6. System completes analysis and records learning
7. View what Lyra learned in option `4`

---

## ⚙️ Configuration

### Add More Projects

**For Obsidian:**
```
Create a folder in ~/Obsidian-Vault/1 - Projectos/
├── Your-Project/
│   ├── README.md (optional)
│   └── subfolders...
```

**For Apps:**
```
Add to ~/Desktop/Apps/
├── Your-App/
│   ├── .git/  (or)
│   ├── README.md  (or)
│   ├── src/
│   └── code...
```

### Customize Agents

Edit `core/agents/__init__.py` to:
- Add new agent roles
- Modify skills
- Change learning rates

---

## 💡 What's Different from v1?

| Feature | v1 (Old) | v2 (New) |
|---------|----------|---------|
| Agents | 13 complex | 7 focused |
| Learning | Incremental RAG | Simple experience recording |
| Code | 10k+ lines | 2k+ lines |
| Setup | Complex | Simple |
| Focus | Theory | Practice |

---

## 🚨 Troubleshooting

**No projects found?**
- Ensure projects are in correct locations
- Check that Obsidian projects are in `~/Obsidian-Vault/1 - Projectos/`
- For Apps: must have `.git`, `README.md`, or code folders

**Import errors?**
- Make sure you're in the His Dark Materials folder
- Check that `core/` directory exists with all modules

**Memory not loading?**
- Memory is stored in `~/.wisdom_council/memory.json`
- Delete this file to reset

---

---

## 📚 Documentation

### Getting Started
- **README.md** (this file) - Overview and quick start
- **README_REAL_ANALYSIS.md** - How real analysis works
- **ORGANIZATION_SUMMARY.md** - Complete project inventory
- **FINAL_ORGANIZATION.md** - Detailed organization
- **STATUS_REPORT.md** - Capabilities & roadmap

### Running Analysis
```bash
# Interactive menu with all projects
python3 run.py

# Real code analysis with MCPs
python3 analyze_with_mcps.py

# Deep research on specific project
python3 research_chemetil.py
python3 research_mundo_barbaro.py
python3 research_wisdom_reddit.py
python3 research_agentsai.py
python3 research_crystal_ball.py

# Verify organization
python3 test_project_organization.py
```

---

## 🏗️ Architecture

```
His Dark Materials/
├── core/
│   ├── agents.py              # 7 agent definitions
│   ├── tasks.py               # Task management
│   ├── memory.py              # Learning persistence
│   ├── analysis/              # Code analysis
│   ├── content/               # Content extraction
│   ├── mcp_analyzer.py        # REAL ANALYSIS ENGINE
│   └── INTEGRATION/           # Project discovery
│
├── run.py                     # Interactive menu
├── run.command                # macOS launcher
├── analyze_with_mcps.py       # Real analysis script
├── research_*.py              # Deep analysis scripts
├── test_project_organization.py
├── README.md                  # This file
└── documentation files...
```

---

## 💡 How It Works

### 1. Project Discovery
- Automatically finds all projects
- 4 executable projects in Apps
- 5 documentation projects in Obsidian
- Validates structure

### 2. Agent Analysis
When you select a project:
1. **Analyze** project structure
2. **Read** content (code, docs)
3. **Debate** between agents
4. **Record** experience in memory

### 3. Real Analysis (NEW!)
- MLX reads actual code
- Identifies specific problems
- Perplexity researches context
- Results saved to Obsidian

### 4. Learning
- Each agent tracks learning score
- Experiences recorded permanently
- Improves over time
- Cross-project insights

---

## 🎯 Use Cases

### For Business Strategy
- Analyze Chemetil market entry
- Get agent recommendations
- Research context via Perplexity

### For Research Optimization
- Analyze MundoBarbaroResearch pipeline
- Find performance bottlenecks
- Get specific optimization recommendations
- Time estimates for each fix

### For Knowledge Organization
- Extract WisdomOfReddit insights
- Build searchable knowledge base
- Get agent perspectives
- Cross-project learning

### For Predictions
- Analyze CrystalBall system
- Understand prediction models
- Optimize performance
- Plan improvements

---

## 🔧 Customization

### Add New Projects
**For Obsidian:**
```bash
mkdir ~/Obsidian-Vault/1\ -\ Projectos/MyProject
# Add content
```

**For Apps:**
```bash
cd ~/Desktop/Apps
git clone [your-repo] MyProject
# Must have .git, README.md, or code folders
```

### Modify Agents
Edit `core/agents.py`:
- Add new agent roles
- Modify skills and specialties
- Adjust learning rates
- Customize perspectives

---

## 📊 Status

### Current State
✅ 7 agents operational
✅ 9 projects discovered
✅ Real code analysis working
✅ MCP integration ready
✅ Learning persistence active
✅ Git tracking all changes

### What's Working
- Project discovery: 100%
- Agent system: 100%
- Real analysis: 100%
- MCP integration: 100%
- Memory system: 100%

### Roadmap
- **Phase 1 (NOW):** Real analysis of projects
- **Phase 2:** Enhanced MCP integration
- **Phase 3:** Execution capabilities
- **Phase 4:** Autonomous improvements

---

## 🤝 Contributing

This is an active project. To contribute:

1. **Analyze projects** using the system
2. **Report findings** via Obsidian
3. **Suggest improvements** via issues
4. **Commit changes** with clear messages

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🚀 Getting Started

```bash
# 1. Open terminal
cd ~/Desktop/Apps/His\ Dark\ Materials

# 2. Run interactive menu
python3 run.py

# OR 3. Run real analysis
python3 analyze_with_mcps.py

# OR 4. Double-click launcher
open run.command
```

---

## 📞 Support

Issues or questions?
- Check documentation files
- Review the code comments
- Analyze your own projects

---

**The Wisdom Council is ready for real work! 🧙‍♂️✨**

A multi-agent system that analyzes real code and provides actionable insights.
