"""
Mary Malone's Research Manager
Handles tool discovery, documentation, and context injection for the team
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from .mary_context import MaryContext, get_mary_context


class MaryResearchManager:
    """Mary manages tool research and context for the entire team."""

    def __init__(self):
        """Initialize Mary's research manager."""
        self.mary = get_mary_context()
        self.tools_db = []
        self.research_log = []
        self.agents_context = {}

    def add_tool_discovery(self, tool_name: str, category: str,
                          summary: str, relevant_agents: List[str],
                          source_url: str = "", version: str = "") -> Dict[str, Any]:
        """Mary discovers and documents a new tool."""

        tool_doc = {
            "id": f"tool_{len(self.tools_db)}",
            "name": tool_name,
            "category": category,
            "discovered_date": self.mary.short_date,
            "summary": summary,
            "relevant_agents": relevant_agents,
            "source_url": source_url,
            "version": version,
            "status": "discovered",
            "last_verified": self.mary.short_date,
        }

        self.tools_db.append(tool_doc)

        # Log the discovery
        self.research_log.append({
            "action": "discovered_tool",
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "by": "Mary",
        })

        return tool_doc

    def get_context_for_agent(self, agent_name: str) -> Dict[str, Any]:
        """Get contextual information for a specific agent's research."""
        return {
            "agent": agent_name,
            "date": self.mary.short_date,
            "month_year": self.mary.month_year,
            "reminder": self.mary.get_agent_reminder(agent_name),
            "search_guidelines": self.mary.get_search_guidelines(),
            "tech_versions": self.mary.tech_versions,
        }

    def start_research_session(self, query: str, agent_name: str = "Unassigned") -> Dict[str, Any]:
        """Start a research session with Mary's context."""
        session_id = f"session_{len(self.research_log)}"

        session = {
            "id": session_id,
            "query": query,
            "agent": agent_name,
            "started": datetime.now().isoformat(),
            "context": self.get_context_for_agent(agent_name),
            "findings": [],
        }

        self.research_log.append({
            "action": "research_session_started",
            "session_id": session_id,
            "query": query,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
        })

        return session

    def document_finding(self, session_id: str, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Document a research finding."""
        documented = {
            **finding,
            "documented_date": self.mary.short_date,
            "timestamp": datetime.now().isoformat(),
        }

        return documented

    def create_agents_md(self, agents: List[Any]) -> str:
        """Create agents.md - the living context file Mary maintains."""

        agents_list = "\n".join([
            f"- **{agent.name}** ({agent.role}): {agent.description}"
            for agent in agents
        ])

        return f"""# The Wisdom Council - Living Context
**Maintained by Mary Malone** 🔬

**Last Updated**: {self.mary.month_year}
**Current Date**: {self.mary.short_date}

---

## Quick Status
- **Total Agents**: {len(agents)}
- **Tools Discovered**: {len(self.tools_db)}
- **Research Sessions**: {len(self.research_log)}
- **Knowledge State**: Current through {self.mary.month_year}

---

## The 8 Agents of the Wisdom Council

{agents_list}

---

## Mary's Current Research Context

### 📅 Temporal Context
- **Today**: {self.mary.month_year}
- **Research Advantage**: Access to 2025-2026 information
- **Claude API Cutoff**: February 2025

### 📊 Technology Versions (Mary Tracks)
{chr(10).join(f"- **{k}**: {v}" for k, v in self.mary.tech_versions.items())}

### 🔬 Mary's Search Guidelines
{self.mary.get_search_guidelines()}

---

## Recently Discovered Tools
{self._format_tools_list() if self.tools_db else "None yet - Mary is actively researching"}

---

## How Mary Helps the Team

### Context Injection
Mary automatically injects her research context into **all team web searches**:
- Current date and month/year
- Technology version baselines
- Search quality guidelines
- Community activity verification

### Tool Documentation
When Mary finds new tools:
1. **Documents** with full metadata
2. **Maps** to relevant agents
3. **Updates** agents.md
4. **Reminds** team to use current information

### Knowledge Synthesis
Mary maintains this context file so the team:
- Always researches with current date awareness
- Knows the latest technology versions
- Follows consistent quality standards
- Never loses track of what's current

---

## Using Mary's Research System

### For Tool Discovery
```bash
mary research "machine learning frameworks 2026"
mary research "Python web frameworks" --category APIs
mary research --trending --period "last-3-months"
```

### For Team Research
All agents automatically get Mary's context when searching:
```
✓ Current date injected
✓ Guidelines applied
✓ Technology versions referenced
✓ Timestamps verified
```

---

## Mary's Standards for Tools

A tool is "worthy" according to Mary if:
- ✅ Actively maintained (commits in last 30 days)
- ✅ Community engagement (issues/discussions active)
- ✅ Recent documentation (updated in 2025+)
- ✅ Clear roadmap for future
- ✅ Solves a real problem

Red flags Mary watches for:
- ❌ No commits in 6+ months
- ❌ Outdated dependencies
- ❌ Only Python 3.9 support (old!)
- ❌ Abandoned GitHub issues
- ❌ Documentation from 2023 or earlier

---

## Contact Mary

When you need:
- **New tool research**: `mary research [topic]`
- **Context reminder**: `mary context --agent [AgentName]`
- **Tools report**: `mary report tools`
- **Status**: `mary status`

---

*This document is the living context for the Wisdom Council*
*Mary updates it automatically as the team researches and discovers*
*All research should reference this context: {self.mary.short_date}*
"""

    def _format_tools_list(self) -> str:
        """Format tools list for markdown."""
        if not self.tools_db:
            return ""

        tools_md = "| Tool | Category | Status | Agents | Date |\n"
        tools_md += "|------|----------|--------|--------|------|\n"

        for tool in self.tools_db:
            agents = ", ".join(tool["relevant_agents"])
            tools_md += f"| **{tool['name']}** | {tool['category']} | {tool['status']} | {agents} | {tool['discovered_date']} |\n"

        return tools_md

    def export_tools_obsidian(self) -> Dict[str, str]:
        """Export tools for Obsidian vault structure."""

        by_category = {}
        by_agent = {}

        for tool in self.tools_db:
            # By category
            cat = tool["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tool)

            # By agent
            for agent in tool["relevant_agents"]:
                if agent not in by_agent:
                    by_agent[agent] = []
                by_agent[agent].append(tool)

        return {
            "by_category": by_category,
            "by_agent": by_agent,
            "all_tools": self.tools_db,
        }

    def save_to_file(self, filepath: Path):
        """Save Mary's research database to file."""
        data = {
            "updated": datetime.now().isoformat(),
            "date": self.mary.short_date,
            "tools": self.tools_db,
            "research_log": self.research_log,
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: Path):
        """Load Mary's research database from file."""
        if not filepath.exists():
            return

        with open(filepath, 'r') as f:
            data = json.load(f)
            self.tools_db = data.get("tools", [])
            self.research_log = data.get("research_log", [])


# Global Mary research manager
mary_research_manager = MaryResearchManager()


def get_mary_research_manager() -> MaryResearchManager:
    """Get the global Mary research manager."""
    return mary_research_manager
