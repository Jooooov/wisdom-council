"""
Competitive Analysis Module
- Analyzes competitive advantages
- Identifies threats and risks
- Evaluates market positioning
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class CompetitiveAnalyzer:
    """Analyzes competitive position and viability."""

    def __init__(self, project_context: Dict[str, Any], market_research: Dict[str, Any]):
        self.context = project_context
        self.market = market_research
        self.analysis = {
            "competitive_advantages": [],
            "competitive_disadvantages": [],
            "threats": [],
            "barriers_to_entry": None,
            "market_differentiation": [],
            "estimated_tam": None,
            "viability_score": 0
        }

    def analyze(self) -> Dict[str, Any]:
        """Conduct competitive analysis."""
        print("🎯 COMPETITIVE ANALYSIS")
        print("-" * 70)

        self._identify_advantages()
        self._identify_disadvantages()
        self._identify_threats()
        self._assess_barriers()
        self._assess_differentiation()
        self._calculate_viability()

        return self.analysis

    def _identify_advantages(self):
        """Identify competitive advantages."""
        print("  ✅ Identifying advantages...")

        advantages = []

        # From project type
        project_type = self.context.get("project_type")
        if project_type:
            if project_type == "ML_TOOL":
                advantages.append("Can provide AI/ML capabilities ahead of competitors")
            elif project_type == "DATA_TOOL":
                advantages.append("Can provide data-driven insights")
            elif project_type == "API":
                advantages.append("Can provide robust integration capabilities")

        # From objectives
        objectives = self.context.get("objectives", [])
        if any("unique" in obj.lower() for obj in objectives):
            advantages.append("Project emphasizes unique value proposition")

        # If solving a gap found in market research
        gaps = self.market.get("gaps", [])
        if gaps:
            advantages.append(f"Addresses market gap: {gaps[0][:50]}")

        self.analysis["competitive_advantages"] = advantages

    def _identify_disadvantages(self):
        """Identify competitive disadvantages."""
        print("  ❌ Identifying disadvantages...")

        disadvantages = []

        # Many competitors already exist?
        competitors = self.market.get("competitors", [])
        if len(competitors) > 5:
            disadvantages.append("Highly competitive market (5+ major competitors)")

        # Established players
        if any("google" in c.lower() or "amazon" in c.lower() or "microsoft" in c.lower()
               for c in competitors):
            disadvantages.append("Market has well-funded tech giants")

        # New project
        structure = self.context.get("structure", {})
        if structure.get("python_files", 0) < 5:
            disadvantages.append("Early stage project (few files/incomplete)")

        self.analysis["competitive_disadvantages"] = disadvantages

    def _identify_threats(self):
        """Identify market threats."""
        print("  ⚠️  Identifying threats...")

        threats = []

        # From market research
        market_summary = self.market.get("market_overview", {}).get("summary", "")

        if any(x in market_summary.lower() for x in ["declining", "shrinking", "saturated"]):
            threats.append("Market is declining or saturated")

        if any(x in market_summary.lower() for x in ["disruption", "changing"]):
            threats.append("Market is undergoing disruption")

        # Competitor threats
        competitors = self.market.get("competitors", [])
        if len(competitors) > 10:
            threats.append("Very high competition (10+ players)")

        # Regulatory
        if any(x in self.context.get("project_name", "").lower() for x in ["health", "finance", "legal"]):
            threats.append("Potential regulatory barriers")

        self.analysis["threats"] = threats

    def _assess_barriers(self):
        """Assess barriers to entry."""
        print("  🔐 Assessing barriers to entry...")

        barriers = {
            "technical_complexity": "Medium",
            "capital_required": "Low-Medium",
            "regulatory_requirements": "None",
            "network_effects": "Low"
        }

        project_type = self.context.get("project_type")
        if project_type in ["ML_TOOL", "API", "DATA_TOOL"]:
            barriers["technical_complexity"] = "High"

        if "business" in self.context.get("project_name", "").lower():
            barriers["capital_required"] = "Medium-High"

        self.analysis["barriers_to_entry"] = barriers

    def _assess_differentiation(self):
        """Assess market differentiation strategy."""
        print("  🎨 Assessing differentiation...")

        differentiation = []

        # From project characteristics
        if self.context.get("project_type") == "ML_TOOL":
            differentiation.append("AI/ML capabilities differentiation")

        if any("real-time" in obj.lower() for obj in self.context.get("objectives", [])):
            differentiation.append("Real-time processing differentiation")

        if any("local" in obj.lower() or "privacy" in obj.lower() for obj in self.context.get("objectives", [])):
            differentiation.append("Privacy/Local-first differentiation")

        # Default if none found
        if not differentiation:
            differentiation.append("Need to define clear differentiation strategy")

        self.analysis["market_differentiation"] = differentiation

    def _calculate_viability(self):
        """Calculate market viability score (0-100)."""
        print("  📊 Calculating viability score...")

        score = 50  # Base score

        # Adjust based on advantages
        advantages = len(self.analysis["competitive_advantages"])
        score += advantages * 10

        # Adjust based on disadvantages
        disadvantages = len(self.analysis["competitive_disadvantages"])
        score -= disadvantages * 10

        # Adjust based on threats
        threats = len(self.analysis["threats"])
        score -= threats * 5

        # Cap between 0-100
        score = max(0, min(100, score))

        self.analysis["viability_score"] = score


def analyze_competitive_position(context: Dict[str, Any], market_research: Dict[str, Any]) -> Dict[str, Any]:
    """Factory function for competitive analysis."""
    analyzer = CompetitiveAnalyzer(context, market_research)
    return analyzer.analyze()
