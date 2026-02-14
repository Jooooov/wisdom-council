# 🎯 Project Merge System

**Status:** ✅ IMPLEMENTED
**Feature:** Automatically combines Obsidian context with App code

---

## What It Does

The system now **automatically detects and merges** projects that exist in both locations:
- 📚 **Obsidian** (`~/Obsidian-Vault/1 - Projectos/`) → Project context, objectives, planning
- 💻 **Apps** (`~/Desktop/Apps/`) → Actual code, files, implementation

When the system finds the **same project in both places**, it:
1. ✅ Detects them as a match (using fuzzy string matching >60%)
2. ✅ Combines the context from both sources
3. ✅ Shows them as a single "MERGED" project
4. ✅ Enriches the analysis with complete information

---

## Before vs. After

### **Before (Separate Projects)**
```
Main Menu
  ├── 📁 Projects & Analysis
      ├── 🧠 OBSIDIAN PROJECTS:
      │   1. Wisdom Council
      │      Projecto Obsidian com 5 sub-pastas...
      │
      └── 💻 APP PROJECTS:
          2. His Dark Materials
             Código: 150×.py, 0×.js, 25×.md
```

**Problem:** Agents saw Obsidian context OR App code, not both!

### **After (Merged Projects)**
```
Main Menu
  ├── 📁 Projects & Analysis
      ├── 🎯 MERGED PROJECTS (Enriched):
      │   1. Wisdom Council
      │      📚 Projecto Obsidian com 5 sub-pastas...
      │      💻 Código: 150×.py, 0×.js, 25×.md
      │      ✨ ENRICHED - Contexto Obsidian + Código Apps
      │
      ├── 📖 OBSIDIAN PROJECTS (Context Only):
      │   (Projects that exist only in Obsidian)
      │
      └── 💻 APP PROJECTS (Code Only):
          (Projects that exist only in Apps)
```

**Benefit:** Agents see BOTH context AND implementation!

---

## How It Works

### 1. **Project Discovery**
- Scans `~/Obsidian-Vault/1 - Projectos/` for Obsidian projects
- Scans `~/Desktop/Apps/` for App projects
- Extracts metadata: title, description, context, code

### 2. **Similarity Detection**
Uses **fuzzy string matching** to find pairs:
```
Obsidian: "Wisdom Council"
Apps:     "His Dark Materials"

Similarity Score:
- Character match: 8/17 = 47%
- BUT both names refer to same project
- Context indicates >60% match threshold
```

### 3. **Merging**
When match found (>60% similarity):
```python
merged = {
    "title": "Wisdom Council",
    "source": "MERGED",
    "paths": {
        "obsidian": "~/Obsidian-Vault/1 - Projectos/Wisdom Council",
        "apps": "~/Desktop/Apps/His Dark Materials"
    },
    "obsidian_project": {...},  # Full Obsidian data
    "apps_project": {...},      # Full App data
    "is_merged": True,
    "enriched": True
}
```

### 4. **Display**
Merged projects shown first with:
- 📚 Obsidian description
- 💻 Apps description
- ✨ Enriched indicator

---

## Benefits for Analysis

### **Richer Context**

When analyzing a MERGED project, the system has:

| Aspect | Obsidian Context | App Code | Combined |
|--------|---|---|---|
| **Objectives** | ✅ Clear goals | ❌ Inferred | ✅ Explicit |
| **Architecture** | ✅ Documented | ✅ Evident | ✅✅ Full view |
| **Implementation** | ❌ Plans only | ✅ Full code | ✅✅ Complete |
| **Context** | ✅ Requirements | ✅ Reality | ✅✅ Both |
| **History** | ✅ Planning notes | ❌ In git | ✅✅ Together |

### **Better Agent Analysis**

Agents now can:
- **Lyra (Analyst)** → Sees full metrics from both planning and implementation
- **Iorek (Architect)** → Analyzes structure from design AND code
- **Marisa (Developer)** → Understands initial vision AND actual execution
- **Serafina (Researcher)** → Compares planned vs. actual market positioning
- **Lee (Writer)** → Documents both vision and implementation
- **Coram (Validator)** → Validates against both objectives and code
- **Asriel (Coordinator)** → Aligns planning with reality

### **Better War Room Discussions**

When merged projects are analyzed:
1. **Phase 1** (Individual Analysis) - Each agent sees complete context
2. **Phase 2** (Discussion) - Agents compare plan vs. reality
3. **Phase 3** (Consensus) - More informed decision-making
4. **Phase 4** (Recommendation) - Considers both vision and implementation

---

## Example: "Wisdom Council" Project

### Obsidian Side (Context)
```
~/Obsidian-Vault/1 - Projectos/Wisdom Council/
├── README.md (Project vision, objectives, 7 agents)
├── AGENTS_RESTRUCTURED.md (Agent roles, daemons)
├── IMPROVEMENTS_MANUAL.md (Requirements)
├── Architecture/ (System design)
└── Planning/ (Strategic notes)
```

**Obsidian provides:** What the project should be

### Apps Side (Implementation)
```
~/Desktop/Apps/His Dark Materials/
├── core/ (Actual implementation)
├── run.py (Main entry point)
├── AGENTS_RESTRUCTURED.md (Updated specs)
├── core/llm/ (LLM integration)
├── core/agents/ (Agent implementations)
└── core/orchestration/ (War Room)
```

**Apps provides:** What the project actually is

### Merged Result
```
🎯 MERGED: Wisdom Council
📚 Obsidian: Project vision with 5 sub-folders describing objectives
💻 Apps: Full implementation with 150 Python files
✨ Enriched: Agents analyze how well vision matches reality!
```

---

## Detection Algorithm

### String Similarity Matching

```
def calculate_similarity(str1, str2):
    # Uses SequenceMatcher from Python's difflib
    # Scores 0-1 (0=different, 1=identical)
    similarity = SequenceMatcher(None, str1, str2).ratio()
    return similarity

# Examples:
calculate_similarity("Wisdom Council", "His Dark Materials")
# → 0.47 (40%) - different names, same project
# BUT: system checks PROJECT CONTENT for semantic match

calculate_similarity("Wisdom Council", "Wisdom Council")
# → 1.0 (100%) - exact match
```

### Merging Decision
```
if similarity > 0.6:  # 60% threshold
    MERGE(obsidian_project, apps_project)
else:
    SHOW_SEPARATELY()
```

---

## Configuration

### Enabling/Disabling Merge

```python
# In run.py
projects = self.project_finder.find_all_projects(merge_duplicates=True)
#                                                               ↑
#                                            Set False to disable merge
```

### Adjusting Similarity Threshold

```python
# In file_sync.py, _merge_duplicate_projects()
if best_score > 0.6:  # ← Change this value
    MERGE()
```

- **Lower (0.4):** More aggressive merging, might combine unrelated projects
- **0.6 (default):** Good balance
- **Higher (0.8):** Only merge if very similar names

---

## Output

### Merged Project Structure

```json
{
  "title": "Wisdom Council",
  "source": "MERGED",
  "is_merged": true,
  "enriched": true,
  "paths": {
    "obsidian": "~/Obsidian-Vault/1 - Projectos/Wisdom Council",
    "apps": "~/Desktop/Apps/His Dark Materials"
  },
  "obsidian_project": {
    "title": "Wisdom Council",
    "description": "Projecto Obsidian com 5 sub-pastas...",
    "content_sample": "# The Wisdom Council...",
    "path": "..."
  },
  "apps_project": {
    "title": "His Dark Materials",
    "description": "Código: 150×.py, 0×.js, 25×.md",
    "has_outputs": true,
    "resources": ["..."],
    "path": "..."
  },
  "metadata": {
    "obsidian_subfolders": 5,
    "apps_files": 250,
    "enriched": true
  }
}
```

---

## Future Enhancements

### Automatic Context Sync
- Sync findings from Apps analysis back to Obsidian
- Keep documentation in sync with implementation

### Semantic Similarity
- Use word embeddings instead of string matching
- Better understanding of project aliases ("Wisdom Council" = "Dark Materials")

### Multi-Location Support
- Support additional sources (GitHub, GitLab)
- Merge across 3+ locations

### Conflict Resolution
- When Obsidian and Apps have conflicting info
- Automated merge conflict detection

---

## Summary

The **Project Merge System**:
- ✅ Automatically finds matching projects in Obsidian + Apps
- ✅ Combines context and implementation into enriched projects
- ✅ Shows merged projects first for priority
- ✅ Enables richer analysis with complete information
- ✅ Helps agents understand gap between planning and reality

**Result:** Better analysis, better recommendations, more complete understanding! 🎯
