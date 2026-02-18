"""
Mary Malone's Research Context Management
Maintains current date, technology versions, and context for all team research
"""

from datetime import datetime
from pathlib import Path
import json
from typing import Dict, Any, List


class MaryContext:
    """Manages the research context that Mary injects into all team searches."""

    def __init__(self):
        """Initialize Mary's context manager."""
        self.current_date = datetime.now()
        self.month_year = self.current_date.strftime("%B %Y")
        self.iso_date = self.current_date.isoformat()
        self.short_date = self.current_date.strftime("%Y-%m-%d")

        # Technology versions (Mary tracks)
        self.tech_versions = {
            "python": "3.14+",
            "nodejs": "22.x",
            "typescript": "5.x",
            "react": "19.x",
            "vue": "3.x",
            "angular": "18.x",
            "fastapi": "0.115+",
            "django": "5.1+",
            "flask": "3.1+",
            "rust": "1.75+",
            "go": "1.22+",
            "claude_api_cutoff": "February 2025",
        }

        self.discovered_tools: List[Dict[str, Any]] = []

    def get_context_for_search(self) -> Dict[str, Any]:
        """Get the complete context for web searches."""
        return {
            "date": self.short_date,
            "full_date": self.month_year,
            "iso_date": self.iso_date,
            "guidelines": self.get_search_guidelines(),
            "tech_versions": self.tech_versions,
        }

    def get_search_guidelines(self) -> str:
        """Mary's guidelines for all team web searches."""
        return f"""
🔬 Mary Malone's Research Guidelines (Feb 2026)

📅 CURRENT DATE: {self.month_year}
⏰ SEARCH ADVANTAGE: You have access to 2025-2026 information
📌 KNOWLEDGE CUTOFF: Claude's cutoff is February 2025

🎯 WHEN SEARCHING FOR TOOLS/FRAMEWORKS:
  ✓ Include "{self.current_date.year}" or "latest" in queries
  ✓ Check GitHub stars updated recently
  ✓ Look for recent release notes (2025-2026)
  ✓ Verify active maintenance (commits in last 30 days)
  ✓ Find current version numbers (see below)
  ✓ Check community adoption trends
  ✓ Cross-reference multiple sources

📊 MARY'S STANDARDS:
  ✓ Always cite publication date
  ✓ Compare against 2025 baselines
  ✓ Flag if information is older than 6 months
  ✓ Note deprecations and end-of-life dates
  ✓ Verify through GitHub, Stack Overflow, Reddit communities

⚠️  RED FLAGS TO WATCH:
  ✗ Documentation hasn't been updated in >12 months
  ✗ Last commit >6 months ago (abandonment)
  ✗ No recent GitHub activity
  ✗ Only mentions Python 3.9 (too old for 2026)
  ✗ No active community/forum activity
"""

    def add_discovered_tool(self, tool_name: str, category: str,
                           summary: str, relevant_agents: List[str],
                           source_url: str = "") -> Dict[str, Any]:
        """Mary documents a newly discovered tool."""
        tool_record = {
            "name": tool_name,
            "category": category,
            "discovered_date": self.short_date,
            "summary": summary,
            "relevant_agents": relevant_agents,
            "source_url": source_url,
            "status": "discovered",
        }
        self.discovered_tools.append(tool_record)
        return tool_record

    def get_context_reminder(self) -> str:
        """String that Mary reminds to all agents before they search."""
        return f"""
🔬 Mary Malone Reminder - Current Context:
   📅 Date: {self.month_year}
   🔍 All searches should reference 2025-2026 information
   📊 Technology versions are {self.month_year}
   🎯 Prioritize recent activity & maintenance
"""

    def get_agent_reminder(self, agent_name: str) -> str:
        """Personalized reminder for each agent before search."""
        return f"""
{agent_name}, Mary reminds you:
Today is {self.month_year}. When you search:
  • Include the year ({self.current_date.year}) in queries
  • Verify tool is actively maintained
  • Check latest version numbers
  • Cross-reference sources
  • Timestamp all findings

Mary's current tech baselines: {json.dumps(self.tech_versions, indent=2)}
"""

    def export_to_markdown(self) -> str:
        """Export context as markdown for documentation."""
        return f"""# Mary Malone's Research Context

**Updated**: {self.month_year}
**Current Date**: {self.short_date}

## Context Summary
- Claude API Cutoff: February 2025
- Current Research Advantage: Access to 2025-2026 data
- Technology Snapshot: {self.month_year}

## Active Technology Versions
{chr(10).join(f"- **{k}**: {v}" for k, v in self.tech_versions.items())}

## Discovered Tools This Session
{chr(10).join(f"- **{t['name']}** ({t['category']}): {t['summary']}" for t in self.discovered_tools) if self.discovered_tools else "None yet"}

## Research Guidelines
{self.get_search_guidelines()}

---
*Maintained by Mary Malone, Tools Manager & Context Keeper*
*Auto-injected into all team web searches*
"""


# Global instance - Mary's context is always available
mary_context = MaryContext()


def get_mary_context() -> MaryContext:
    """Get the global Mary context instance."""
    return mary_context


def inject_mary_context(original_query: str) -> str:
    """
    Inject Mary's context into a search query.
    Used when any agent is about to do a web search.
    """
    context = get_mary_context()
    return f"""{original_query}

[Mary's Context: {context.short_date}, looking for recently updated 2025-2026 information]"""


def get_mary_research_system_prompt() -> str:
    """System prompt for Mary's research sessions."""
    context = get_mary_context()
    return f"""You are Mary Malone, Scientist and Tools Manager for the Wisdom Council.

Current Date: {context.month_year}
Your Role: Discover, analyze, and document tools for the team

Remember:
1. All search results should reference 2025-2026 information
2. Verify tool maintenance and community activity
3. Always include timestamps and sources
4. Check GitHub stars, commits, and activity
5. Compare against known baselines
6. Flag deprecated or abandoned projects

Technology Versions You Track:
{json.dumps(context.tech_versions, indent=2)}

When you discover a tool, document it in the format:
- Name: [Tool name]
- Category: [Category]
- Status: [Emerging/Growing/Mature]
- Best For: [List of relevant agents]
- Summary: [2-3 sentence description]
- Last Updated: [Latest release date]
- Community: [Activity level]
- Source: [URL]
"""
