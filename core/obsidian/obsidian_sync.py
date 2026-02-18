"""
Obsidian Vault Synchronization for Mary Malone's Tool Database
Syncs tools to Obsidian vault with proper structure and backlinks
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json


class ObsidianSync:
    """Syncs Mary's tool database to Obsidian vault."""

    def __init__(self, vault_path: str = None):
        """Initialize Obsidian sync."""
        if vault_path is None:
            # Use default path
            vault_path = "/Users/joaovicente/Library/Mobile Documents/iCloud~md~obsidian/Documents/source mindpalace"

        self.vault_root = Path(vault_path)
        self.tools_folder = self.vault_root / "0 - tools"
        self.tools_folder.mkdir(parents=True, exist_ok=True)

        # Create subfolders
        self.by_category_folder = self.tools_folder / "by_category"
        self.by_agent_folder = self.tools_folder / "by_agent"
        self.emerging_folder = self.tools_folder / "emerging"

        for folder in [self.by_category_folder, self.by_agent_folder, self.emerging_folder]:
            folder.mkdir(parents=True, exist_ok=True)

    def sync_tools(self, tools_data: List[Dict[str, Any]]):
        """Sync tools database to Obsidian."""
        print(f"\n🔗 Syncing {len(tools_data)} tools to Obsidian vault...")
        print(f"   📁 Vault: {self.vault_root.name}")
        print(f"   📂 Tools folder: {self.tools_folder.name}\n")

        # 1. Create index file
        self._create_tools_index(tools_data)

        # 2. Create tools by category
        self._create_category_files(tools_data)

        # 3. Create agent tool lists
        self._create_agent_tool_files(tools_data)

        # 4. Create emerging tools tracker
        self._create_emerging_tracker(tools_data)

        print("✅ Obsidian sync complete!")

    def _create_tools_index(self, tools: List[Dict[str, Any]]):
        """Create main tools index file."""
        index_content = f"""# 🔧 Tools Database - Mary Malone's Registry
**Last Updated**: {datetime.now().strftime('%B %d, %Y at %H:%M')}

## Quick Stats
- **Total Tools**: {len(tools)}
- **Categories**: {len(set(t['category'] for t in tools))}
- **For Agents**: 8 members of Wisdom Council

---

## Browse By...

### 📁 By Category
{self._generate_category_links(tools)}

### 👥 By Agent
{self._generate_agent_links(tools)}

### 🚀 Emerging Tools
[[Emerging Tools Tracker|Emerging Tools]]

---

## All Tools

| Tool | Category | Status | Agents | Date |
|------|----------|--------|--------|------|
{self._generate_tools_table(tools)}

---

## About This Database

Mary Malone maintains this tool database to help the Wisdom Council:
- **Discover** new tools and frameworks
- **Evaluate** tool quality and maintenance
- **Map** tools to agent specializations
- **Track** emerging technologies

All tools are verified for:
- ✅ Active maintenance (commits in last 30 days)
- ✅ Community engagement
- ✅ Recent documentation (2025+)
- ✅ Clear purpose and value

---

## How to Use

### For Agents
Each agent has a list of tools mapped to their role:
- [[Lyra's Tools|Lyra's Arsenal]] - Analysis tools
- [[Iorek's Tools|Iorek's Arsenal]] - Architecture tools
- [[Marisa's Tools|Marisa's Arsenal]] - Development tools
- [[Serafina's Tools|Serafina's Arsenal]] - Research tools
- [[Lee's Tools|Lee's Arsenal]] - Communication tools
- [[Coram's Tools|Coram's Arsenal]] - Validation tools
- [[Asriel's Tools|Asriel's Arsenal]] - Coordination tools
- [[Mary's Tools|Mary's Arsenal]] - Knowledge tools

### For Research
Browse by category to find tools for specific needs:
{self._generate_category_browse_list(tools)}

---

## Adding New Tools

When Mary discovers a new tool:
1. Tool is added to database
2. Obsidian files auto-update
3. Agent mappings created
4. Backlinks established
5. Index refreshed

---

*Maintained by Mary Malone, Tools Manager & Context Keeper*
*Part of the Wisdom Council Knowledge Base*
"""

        index_file = self.tools_folder / "_Index.md"
        index_file.write_text(index_content)
        print(f"   ✅ Created: {index_file.name}")

    def _create_category_files(self, tools: List[Dict[str, Any]]):
        """Create files organized by category."""
        # Group tools by category
        by_category = {}
        for tool in tools:
            cat = tool["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tool)

        for category, category_tools in sorted(by_category.items()):
            # Create category file
            cat_file = self.by_category_folder / f"{category}.md"

            content = f"""# 📚 {category.title()} Tools

**Category**: {category}
**Tools Count**: {len(category_tools)}
**Last Updated**: {datetime.now().strftime('%B %d, %Y')}

---

## Tools in This Category

{self._generate_category_tool_list(category_tools)}

---

## Related

- [[Tools Database|Back to Index]]
- [[Wisdom Council]]
- [[Mary Malone]]

---

*Mary's curated collection of {category.lower()} tools*
"""

            cat_file.write_text(content)
            print(f"   ✅ Category: {category}")

    def _create_agent_tool_files(self, tools: List[Dict[str, Any]]):
        """Create files for each agent's tools."""
        # Map tools to agents
        agent_tools = {
            "Lyra": [],
            "Iorek": [],
            "Marisa": [],
            "Serafina": [],
            "Lee": [],
            "Coram": [],
            "Asriel": [],
            "Mary": [],
        }

        for tool in tools:
            for agent in tool.get("relevant_agents", []):
                if agent in agent_tools:
                    agent_tools[agent].append(tool)

        # Create agent tool files
        agent_info = {
            "Lyra": ("Analyst", "📊", "data analysis, pattern recognition, insights"),
            "Iorek": ("Architect", "🏗️", "system design, architecture, structure"),
            "Marisa": ("Developer", "💻", "implementation, development, execution"),
            "Serafina": ("Researcher", "🔬", "research, investigation, discovery"),
            "Lee": ("Writer", "✍️", "communication, documentation, storytelling"),
            "Coram": ("Validator", "✅", "testing, validation, quality assurance"),
            "Asriel": ("Coordinator", "🎯", "coordination, leadership, strategy"),
            "Mary": ("Tools Manager", "🔬", "tools discovery, documentation, knowledge"),
        }

        for agent_name, tools_list in agent_tools.items():
            if not tools_list:
                continue

            role, emoji, description = agent_info.get(agent_name, (agent_name, "👤", ""))

            content = f"""# {emoji} {agent_name}'s Arsenal
**Role**: {role}
**Tools Count**: {len(tools_list)}
**Specialization**: {description}

---

## Available Tools

{self._generate_agent_tool_list(agent_name, tools_list)}

---

## How These Tools Help {agent_name}

{self._get_agent_tool_help(agent_name, tools_list)}

---

## Related

- [[Tools Database|Back to Index]]
- [[{agent_name} - Wisdom Council Member|{agent_name}]]
- [[Mary Malone]]

---

*Mary's curated selection of tools for {agent_name}'s work*
"""

            agent_file = self.by_agent_folder / f"{agent_name}'s Tools.md"
            agent_file.write_text(content)
            print(f"   ✅ Agent: {agent_name} ({len(tools_list)} tools)")

    def _create_emerging_tracker(self, tools: List[Dict[str, Any]]):
        """Create tracker for emerging tools."""
        emerging = [t for t in tools if t.get("status") == "discovered"]

        if not emerging:
            emerging = tools  # Show all if none marked as emerging

        content = f"""# 🚀 Emerging Tools Tracker
**Last Updated**: {datetime.now().strftime('%B %d, %Y at %H:%M')}

## Recently Discovered

Mary is actively researching and discovering new tools. Here are the latest findings:

| Tool | Category | Discovered | Agents | Notes |
|------|----------|-----------|--------|-------|
{self._generate_emerging_table(emerging)}

---

## How to Evaluate New Tools

Mary uses these criteria:
- ✅ Active maintenance (commits in 30 days)
- ✅ Community engagement (issues/discussions)
- ✅ Recent documentation (2025+)
- ✅ Clear roadmap
- ✅ Solves real problem

## Process

1. **Discovery** - Mary finds promising tool
2. **Analysis** - Evaluates against criteria
3. **Documentation** - Records findings
4. **Integration** - Maps to relevant agents
5. **Approval** - Added to main database

---

## Contact Mary

To suggest a tool or discuss findings:
- [[Mary Malone]] - Tools Manager
- Tools are continuously evaluated
- New discoveries added regularly

---

*Part of the Wisdom Council's knowledge base*
*Maintained by Mary Malone*
"""

        emerging_file = self.tools_folder / "Emerging Tools Tracker.md"
        emerging_file.write_text(content)
        print(f"   ✅ Emerging tracker: {len(emerging)} tools")

    def _generate_category_links(self, tools: List[Dict[str, Any]]) -> str:
        """Generate links to category files."""
        categories = sorted(set(t["category"] for t in tools))
        links = [f"- [[{cat}|{cat} Tools]]" for cat in categories]
        return "\n".join(links)

    def _generate_agent_links(self, tools: List[Dict[str, Any]]) -> str:
        """Generate links to agent tool files."""
        agents = ["Lyra", "Iorek", "Marisa", "Serafina", "Lee", "Coram", "Asriel", "Mary"]
        links = [f"- [[{agent}'s Tools|{agent}'s Arsenal]]" for agent in agents]
        return "\n".join(links)

    def _generate_tools_table(self, tools: List[Dict[str, Any]]) -> str:
        """Generate markdown table of all tools."""
        rows = []
        for tool in sorted(tools, key=lambda t: t["name"]):
            agents = ", ".join(tool.get("relevant_agents", []))
            rows.append(
                f"| **{tool['name']}** | {tool['category']} | {tool.get('status', 'active')} | {agents} | {tool.get('discovered_date', 'N/A')} |"
            )
        return "\n".join(rows)

    def _generate_category_browse_list(self, tools: List[Dict[str, Any]]) -> str:
        """Generate browse list for categories."""
        categories = sorted(set(t["category"] for t in tools))
        items = [f"- **{cat}**: [[{cat}|{len([t for t in tools if t['category'] == cat])} tools]]"
                 for cat in categories]
        return "\n".join(items)

    def _generate_category_tool_list(self, category_tools: List[Dict[str, Any]]) -> str:
        """Generate list of tools in a category."""
        items = []
        for tool in sorted(category_tools, key=lambda t: t["name"]):
            agents = ", ".join([f"[[{a}'s Tools|{a}]]" for a in tool.get("relevant_agents", [])])
            items.append(
                f"- **{tool['name']}**\n"
                f"  - 📝 {tool.get('summary', 'No description')}\n"
                f"  - 👥 For: {agents}\n"
                f"  - 🔗 [{tool.get('source_url', 'Link')}]({tool.get('source_url', '#')})"
            )
        return "\n".join(items)

    def _generate_agent_tool_list(self, agent_name: str, tools: List[Dict[str, Any]]) -> str:
        """Generate list of tools for an agent."""
        items = []
        for tool in sorted(tools, key=lambda t: t["name"]):
            items.append(
                f"- **{tool['name']}** ({tool['category']})\n"
                f"  - {tool.get('summary', 'No description')}\n"
                f"  - [[{tool['category']}|Browse category]]\n"
                f"  - 🔗 [{tool.get('source_url', 'Link')}]({tool.get('source_url', '#')})"
            )
        return "\n".join(items)

    def _get_agent_tool_help(self, agent_name: str, tools: List[Dict[str, Any]]) -> str:
        """Get description of how tools help an agent."""
        helps = {
            "Lyra": "These tools help Lyra analyze data, recognize patterns, and seek hidden truths.",
            "Iorek": "These tools help Iorek design robust structures, provide strength, and resolve conflicts.",
            "Marisa": "These tools help Marisa execute with ambition, drive projects, and take decisive action.",
            "Serafina": "These tools help Serafina conduct deep research, see big pictures, and gather wisdom.",
            "Lee": "These tools help Lee create clear communication, tell stories, and document discoveries.",
            "Coram": "These tools help Coram validate thoroughly, test carefully, and identify risks.",
            "Asriel": "These tools help Asriel coordinate strategies, command loyalty, and drive visions.",
            "Mary": "These tools help Mary discover, understand, and document tools for the team.",
        }
        return helps.get(agent_name, f"These tools support {agent_name}'s work in the Wisdom Council.")

    def _generate_emerging_table(self, tools: List[Dict[str, Any]]) -> str:
        """Generate table of emerging tools."""
        rows = []
        for tool in sorted(tools, key=lambda t: t.get("discovered_date", ""), reverse=True)[:10]:
            agents = ", ".join(tool.get("relevant_agents", []))
            rows.append(
                f"| [[{tool['name']}|{tool['name']}]] | {tool['category']} | {tool.get('discovered_date', 'N/A')} | {agents} | {tool.get('summary', '')[:50]}... |"
            )
        return "\n".join(rows)


def sync_mary_to_obsidian(mary_manager):
    """Sync Mary's tool database to Obsidian vault."""
    obsidian = ObsidianSync()
    obsidian.sync_tools(mary_manager.tools_db)
    return obsidian
