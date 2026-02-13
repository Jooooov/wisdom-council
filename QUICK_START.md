# 🚀 QUICK START - Wisdom Council v2

**Status:** ✅ Ready to use
**Last Updated:** 2026-02-13

---

## The Problem (That Was Fixed)

❌ **Before:** run.command opened but agents said "success" instantly with no real insights
✅ **After:** run.command now shows actual code analysis with specific findings

---

## How to Use

### 1️⃣ Easiest Way (Double-Click)
```
Finder → Desktop → Apps → His Dark Materials → run.command
```

**What happens:**
1. Terminal opens
2. Shows system status (7 agents)
3. Menu appears with options
4. Select "3" to analyze a project
5. System reads actual code and finds real issues
6. Takes time (because it's real work, not fake)

---

### 2️⃣ Terminal Command

```bash
cd ~/Desktop/Apps/His\ Dark\ Materials
python3 run.py
```

Then choose from menu:
- `1` - Show system status
- `2` - List available projects
- `3` - **Analyze a project (REAL ANALYSIS)**
- `4` - View agent learning history
- `5` - View memory & experiences
- `0` - Exit

---

### 3️⃣ Deep Analysis with MLX (If Available)

```bash
python3 analyze_with_mcps.py
```

Uses local Qwen3 LLM for semantic analysis (requires MLX).

---

### 4️⃣ Lightweight Analysis (No MLX)

```bash
python3 analyze_simple.py
```

Works without MLX, still analyzes real code.

---

## What Real Analysis Shows

When you select "Have agents work on a project":

### 📊 It Actually:
✅ Reads Python files (not just counts them)
✅ Detects real issues (TODOs, hardcoded values, security issues)
✅ Shows specific file names and line counts
✅ Provides actionable recommendations
✅ Records real learning experiences

### Example Output:
```
📊 ANALYZING: MundoBarbaroResearch
⏳ This analyzes actual code - may take a moment...

📊 Analyzing Python files...
  ✓ Found issues in cli.py
  ✓ Found issues in main.py

🔴 REAL FINDINGS
Files with issues (3 found):
  📄 cli.py (372 lines)
     • Possible hardcoded configuration

  📄 main.py (673 lines)
     • Possible hardcoded configuration

💡 ACTIONABLE IMPROVEMENTS
1. [HIGH] Code Review: Check hardcoded values
2. [MEDIUM] Testing: Add unit tests
3. [MEDIUM] Documentation: Add docstrings
4. [LOW] Performance: Profile operations

📚 LEARNING RECORDED
✅ Lyra: +1 experience (score: 0.01)
✅ Iorek: +1 experience (score: 0.01)
[... all 7 agents ...]
```

---

## What's Different from Before

| Feature | Old (Fake) | New (Real) |
|---------|-----------|-----------|
| **Speed** | <1 second | Takes time |
| **What it does** | Counts files | Reads code |
| **Issues found** | None | Real issues |
| **File names** | No | Yes (specific) |
| **Actionable** | Generic | Specific |
| **Learning** | Fake claims | Real discoveries |

---

## Available Projects

The system can analyze:

**Executable (~/Desktop/Apps/):**
1. His Dark Materials (this system)
2. CrystalBall (predictions engine)
3. WisdomOfReddit (intelligence system)
4. MundoBarbaroResearch (research pipeline)

**Documentation (~/Obsidian-Vault/1 - Projectos/):**
5. Chemetil (business strategy)
6. WisdomOfReddit (knowledge base)
7. MundoBarbaroResearch (research docs)
8. RedditScrapper (data collection)
9. AgentsAI (learning materials)

---

## Troubleshooting

### run.command doesn't open terminal
→ Try: `python3 run.py` in terminal instead

### Terminal opens but shows error
→ Make sure you're in the right directory:
```bash
cd ~/Desktop/Apps/His\ Dark\ Materials
python3 run.py
```

### Analysis runs but finds nothing
→ Try a different project (some may not have obvious issues)
→ Or use: `python3 analyze_simple.py`

### Want to see agent learning history
→ In menu, select option "4"

### Want to reset everything
→ Delete: `~/.wisdom_council/memory.json`
→ Then restart

---

## Files Changed (Fixed Analysis)

- **run.py** - Now uses real analysis instead of fake
- **FIXED_REAL_ANALYSIS.md** - Documentation of the fix
- **analyze_simple.py** - Lightweight analysis option
- **core/mcp_analyzer.py** - Deep analysis with MCPs

---

## Next Steps

1. **Run the system:** Double-click run.command
2. **Select option 3:** Analyze a project
3. **See real insights:** File names, issues, recommendations
4. **Check learning:** Option 4 to see what agents discovered

---

## The Fix Explained

**Problem:** Agents were running too fast saying generic things
**Cause:** Using old ProjectAnalyzer that just counted files
**Solution:** Replaced with real code analysis that reads files
**Result:** Now shows specific issues with file names and actionable recommendations

---

## Questions?

Read: `FIXED_REAL_ANALYSIS.md` - Full explanation of what was fixed

Check: Latest commits on GitHub - Shows what changed

Try: `python3 run.py` - Test it yourself

---

**You now have REAL analysis, not theater!** 🧙‍♂️✨
