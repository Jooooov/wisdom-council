"""
Business Analyzer - Main orchestrator for business analysis
- Coordinates context analysis
- Runs market research
- Executes competitive analysis
- Prepares for agent discussion
"""

import asyncio
from typing import Dict, Any
from pathlib import Path

from .context_analyzer import ContextAnalyzer
from .market_research import research_market
from .competitive_analyzer import analyze_competitive_position


class BusinessAnalyzer:
    """Main business analysis orchestrator."""

    def __init__(self, project_path: str, project_name: str):
        self.project_path = project_path
        self.project_name = project_name
        self.context = None
        self.market_research = None
        self.competitive_analysis = None
        self.business_case = {
            "project_name": project_name,
            "status": "ANALYZING",
            "context": None,
            "extra_context": None,
            "market_research": None,
            "competitive_analysis": None,
            "ready_for_agent_discussion": False
        }

    async def run_full_analysis(self, extra_context: str = None) -> Dict[str, Any]:
        """Run complete business analysis."""
        if extra_context:
            self.business_case["extra_context"] = extra_context
        print("\n" + "=" * 70)
        print("🏢 BUSINESS ANALYSIS: Comprehensive Market & Competitive Review")
        print("=" * 70)

        try:
            # Step 1: Analyze context
            print("\n📍 STEP 1: Understanding Project Context")
            print("-" * 70)
            context_analyzer = ContextAnalyzer(self.project_path, self.project_name)
            self.context = await context_analyzer.analyze()

            if not self.context.get("is_business"):
                print("\n⚠️  Project is NOT identified as a business project")
                print("   Type: " + self.context.get("project_type", "Unknown"))
                print("   This analysis is for BUSINESS projects only")
                self.business_case["status"] = "NOT_BUSINESS"
                return self.business_case

            print("\n✅ Project identified as BUSINESS")
            print(f"   Type: {self.context.get('project_type')}")
            print(f"   Objectives: {len(self.context.get('objectives', []))} found")

            self.business_case["context"] = self.context

            # Step 2: Market research
            print("\n📊 STEP 2: Market Research")
            print("-" * 70)
            self.market_research = await research_market(
                self.project_name,
                self.context.get("project_type"),
                self.context.get("objectives", [])
            )

            print("✅ Market research completed")
            print(f"   Competitors found: {len(self.market_research.get('competitors', []))}")
            print(f"   Gaps identified: {len(self.market_research.get('gaps', []))}")
            print(f"   Opportunities: {len(self.market_research.get('opportunities', []))}")

            self.business_case["market_research"] = self.market_research

            # Step 3: Competitive analysis
            print("\n🎯 STEP 3: Competitive Analysis")
            print("-" * 70)
            self.competitive_analysis = analyze_competitive_position(
                self.context,
                self.market_research
            )

            print("✅ Competitive analysis completed")
            print(f"   Advantages: {len(self.competitive_analysis.get('competitive_advantages', []))}")
            print(f"   Disadvantages: {len(self.competitive_analysis.get('competitive_disadvantages', []))}")
            print(f"   Threats: {len(self.competitive_analysis.get('threats', []))}")
            print(f"   Viability Score: {self.competitive_analysis.get('viability_score', 0)}/100")

            self.business_case["competitive_analysis"] = self.competitive_analysis

            # Step 4: Prepare for discussion
            print("\n📋 STEP 4: Preparing Business Case for Agent Discussion")
            print("-" * 70)
            self._prepare_business_case()

            self.business_case["status"] = "READY"
            self.business_case["ready_for_agent_discussion"] = True

            print("✅ Business case prepared and ready for agent discussion")

            return self.business_case

        except Exception as e:
            print(f"\n❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
            self.business_case["status"] = "FAILED"
            self.business_case["error"] = str(e)
            return self.business_case

    def _prepare_business_case(self):
        """Prepare business case summary for agent discussion."""
        summary = {
            "project_name": self.project_name,
            "project_type": self.context.get("project_type"),
            "viability_score": self.competitive_analysis.get("viability_score"),
            "key_points": {
                "advantages": self.competitive_analysis.get("competitive_advantages", [])[:3],
                "disadvantages": self.competitive_analysis.get("competitive_disadvantages", [])[:3],
                "threats": self.competitive_analysis.get("threats", [])[:3],
                "market_gaps": self.market_research.get("gaps", [])[:2],
                "opportunities": self.market_research.get("opportunities", [])[:2],
            },
            "discussion_questions": self._generate_discussion_questions()
        }

        self.business_case["summary"] = summary

    def _generate_discussion_questions(self) -> list:
        """Generate discussion questions for agents."""
        questions = [
            "Is the market opportunity large enough to justify investment?",
            "Can we differentiate effectively from existing competitors?",
            "What are the biggest risks we need to mitigate?",
            "What is our go-to-market strategy?",
            "Do we have the resources to execute on this?",
            "What is the timeline to profitability?",
            "Should we proceed (GO) or pivot/cancel (NO-GO)?"
        ]
        return questions


async def analyze_business(project_path: str, project_name: str, extra_context: str = None) -> Dict[str, Any]:
    """Factory function for business analysis."""
    analyzer = BusinessAnalyzer(project_path, project_name)
    return await analyzer.run_full_analysis(extra_context=extra_context)
