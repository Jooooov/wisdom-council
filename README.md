# 🧙‍♂️ The Wisdom Council v2

**Simplified. Practical. Powerful.**

A leaner multi-agent system that works on REAL projects from your Obsidian vault and Apps folder.

---

## 🚀 Quick Start

### Option 1: Terminal
```bash
python3 ~/Desktop/Apps/His\ Dark\ Materials/run.py
```

### Option 2: macOS Double-Click
```
Finder → Desktop → Apps → His Dark Materials → run.command
```

---

## 🧠 7 Core Agents

Each agent has unique skills and learns from experience:

| Agent | Role | Specialties |
|-------|------|------------|
| **Lyra** | Analyst | Analysis, research, pattern recognition |
| **Iorek** | Architect | Design, architecture, planning |
| **Marisa** | Developer | Coding, implementation, debugging |
| **Serafina** | Researcher | Research, investigation, exploration |
| **Lee** | Writer | Documentation, writing, communication |
| **Pantalaimon** | Tester | Testing, validation, bug detection |
| **Philip** | Coordinator | Coordination, management, decisions |

---

## 📁 How Projects Are Found

### Obsidian Projects
- **Location:** `~/Obsidian-Vault/1 - Projectos/`
- **Format:** Each folder is a project
- **Example:** `WisdomOfReddit/`

### App Projects
Automatically detects projects with:
- `.git/` folder (git repository)
- `README.md` or `PROJECT_CONTEXT.md`
- `src/`, `code/`, or similar code folders
- `requirements.txt` or `package.json`

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

## 📖 Next Steps

1. **Run the system** and explore
2. **Add your projects** to Obsidian or Apps folders
3. **Let agents work** and build memory
4. **Scale up** with more agents if needed

---

## 🎯 Goals Met

✅ Simple and clean architecture
✅ Works with real projects
✅ Agents learn from experience
✅ Easy to understand and modify
✅ No complex dependencies

---

**Happy working! 🚀**

The Wisdom Council awaits your projects!
