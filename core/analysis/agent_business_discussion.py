"""
Agent Business Discussion Module
- Agents discuss business viability as consultants
- Each agent provides perspective based on their role
- Generates consensus and GO/NO-GO recommendation
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class AgentBusinessDiscussion:
    """Facilitates business discussion between agents."""

    def __init__(self, business_case: Dict[str, Any], agents: List[Any]):
        self.business_case = business_case
        self.agents = agents
        self.perspectives = {}
        self.consensus = None
        self.recommendation = None

    def conduct_discussion(self) -> Dict[str, Any]:
        """Conduct full business discussion."""
        print("\n" + "=" * 70)
        print("🎤 AGENT CONSULTATION MEETING")
        print("=" * 70)
        print(f"\nProject: {self.business_case.get('project_name')}")
        print(f"Viability Score: {self.business_case.get('viability_score', 0)}/100")

        # Each agent gives perspective
        print("\n" + "-" * 70)
        print("💬 AGENT PERSPECTIVES")
        print("-" * 70)

        for agent in self.agents:
            perspective = self._get_agent_perspective(agent)
            self.perspectives[agent.name] = perspective

            print(f"\n🎯 {agent.name} ({agent.role}):")
            print(f"   Position: {perspective['position']}")
            print(f"   Key Points:")
            for point in perspective['key_points'][:2]:
                print(f"     • {point}")
            print(f"   Recommendation: {perspective['recommendation']}")

        # Generate consensus
        print("\n" + "-" * 70)
        print("🤝 CONSENSUS BUILDING")
        print("-" * 70)

        self.consensus = self._build_consensus()
        print(f"\nConsensus: {self.consensus['summary']}")
        print(f"Agreement Level: {self.consensus['agreement_percentage']}%")

        # Final recommendation
        print("\n" + "-" * 70)
        print("🎯 FINAL RECOMMENDATION")
        print("-" * 70)

        self.recommendation = self._generate_recommendation()
        print(f"\n{self.recommendation['decision']}")
        print(f"Confidence: {self.recommendation['confidence']}/10")
        print(f"\nReasoning:")
        for reason in self.recommendation['reasoning']:
            print(f"  • {reason}")

        print(f"\nNext Steps:")
        for step in self.recommendation['next_steps']:
            print(f"  → {step}")

        return {
            "perspectives": self.perspectives,
            "consensus": self.consensus,
            "recommendation": self.recommendation
        }

    def _get_agent_perspective(self, agent) -> Dict[str, Any]:
        """Get specific agent perspective based on their role."""
        role = agent.role.lower()
        business_case = self.business_case

        perspective = {
            "position": "",
            "key_points": [],
            "recommendation": "",
            "confidence": 0
        }

        # Extract data
        advantages = business_case.get('competitive_analysis', {}).get('competitive_advantages', [])
        disadvantages = business_case.get('competitive_analysis', {}).get('competitive_disadvantages', [])
        threats = business_case.get('competitive_analysis', {}).get('threats', [])
        viability = business_case.get('viability_score', 50)

        if "analyst" in role or "lyra" in agent.name.lower():
            perspective["position"] = "Data-Driven"
            perspective["key_points"] = [
                f"Market viability score: {viability}/100",
                f"Identified {len(advantages)} competitive advantages",
                f"Identified {len(disadvantages)} disadvantages",
                "Need strong metrics to justify investment"
            ]
            perspective["recommendation"] = "GO" if viability > 60 else "NO-GO"
            perspective["confidence"] = 9

        elif "architect" in role or "iorek" in agent.name.lower():
            perspective["position"] = "Structural"
            perspective["key_points"] = [
                "Scalability is critical for business success",
                f"Current structure requires {'minimal' if len(disadvantages) < 3 else 'significant'} architectural work",
                "Integration with existing platforms is feasible",
                "Need modular design for market expansion"
            ]
            perspective["recommendation"] = "GO" if len(disadvantages) <= 3 else "CONDITIONAL"
            perspective["confidence"] = 8

        elif "developer" in role or "marisa" in agent.name.lower():
            perspective["position"] = "Execution"
            perspective["key_points"] = [
                "Project is technically feasible to execute",
                "Development timeline is realistic (6-12 months)",
                "Resource requirements are manageable",
                "Quality standards can be maintained"
            ]
            perspective["recommendation"] = "GO"
            perspective["confidence"] = 8

        elif "researcher" in role or "serafina" in agent.name.lower():
            perspective["position"] = "Market Intelligence"
            perspective["key_points"] = [
                f"Market has {len(business_case.get('market_research', {}).get('competitors', []))} competitors",
                f"Identified {len(business_case.get('market_research', {}).get('opportunities', []))} market opportunities",
                f"Identified {len(business_case.get('market_research', {}).get('gaps', []))} market gaps",
                "Competitive landscape is well-researched and understood"
            ]
            perspective["recommendation"] = "GO" if len(advantages) > 0 else "NEEDS_STUDY"
            perspective["confidence"] = 9

        elif "writer" in role or "lee" in agent.name.lower():
            perspective["position"] = "Positioning"
            perspective["key_points"] = [
                "Clear value proposition can be articulated",
                "Market messaging is compelling",
                "Brand positioning is differentiated",
                "Customer communication strategy is viable"
            ]
            perspective["recommendation"] = "GO"
            perspective["confidence"] = 7

        elif "tester" in role or "pantalaimon" in agent.name.lower():
            perspective["position"] = "Risk Assessment"
            perspective["key_points"] = [
                f"Identified {len(threats)} significant threats",
                "Risk mitigation strategies are required",
                "Contingency planning is necessary",
                "Market validation is critical before launch"
            ]
            perspective["recommendation"] = "CONDITIONAL" if threats else "GO"
            perspective["confidence"] = 8

        elif "coordinator" in role or "philip" in agent.name.lower():
            perspective["position"] = "Overall Viability"
            perspective["key_points"] = [
                f"Overall viability score: {viability}/100",
                f"Team consensus is {'strong' if viability > 70 else 'mixed' if viability > 50 else 'weak'}",
                "Resource allocation is optimal",
                "Timeline and milestones are realistic"
            ]
            perspective["recommendation"] = "GO" if viability > 65 else "CONDITIONAL" if viability > 50 else "NO-GO"
            perspective["confidence"] = 9

        return perspective

    def _build_consensus(self) -> Dict[str, Any]:
        """Build consensus from all perspectives."""
        go_votes = sum(1 for p in self.perspectives.values() if "GO" in p['recommendation'])
        conditional_votes = sum(1 for p in self.perspectives.values() if "CONDITIONAL" in p['recommendation'])
        no_go_votes = sum(1 for p in self.perspectives.values() if "NO-GO" in p['recommendation'])
        total = len(self.perspectives)

        if go_votes >= total * 0.7:
            decision = "STRONG GO"
        elif go_votes + conditional_votes >= total * 0.7:
            decision = "GO WITH CONDITIONS"
        elif no_go_votes >= total * 0.5:
            decision = "NO-GO"
        else:
            decision = "NEEDS FURTHER STUDY"

        agreement = int((max(go_votes, conditional_votes, no_go_votes) / total) * 100)

        return {
            "decision": decision,
            "summary": f"{go_votes} strong GO, {conditional_votes} conditional, {no_go_votes} NO-GO",
            "agreement_percentage": agreement
        }

    def _generate_recommendation(self) -> Dict[str, Any]:
        """Generate final GO/NO-GO recommendation."""
        viability = self.business_case.get('viability_score', 50)
        consensus = self.consensus['decision']
        advantages = len(self.business_case.get('competitive_analysis', {}).get('competitive_advantages', []))

        # Decision logic
        if viability >= 70 and "GO" in consensus:
            decision = "✅ GO - Project is viable and recommended"
            confidence = 9
        elif viability >= 60 and "CONDITIONAL" not in consensus:
            decision = "✅ GO WITH CAUTION - Address key risks first"
            confidence = 7
        elif viability >= 50:
            decision = "⚠️  CONDITIONAL GO - Dependent on risk mitigation"
            confidence = 6
        elif viability >= 30:
            decision = "❌ PIVOT REQUIRED - Current structure not viable"
            confidence = 7
        else:
            decision = "❌ NO-GO - Market conditions not favorable"
            confidence = 8

        # Reasoning
        reasoning = []
        if advantages > 2:
            reasoning.append("Clear competitive advantages identified")
        if viability > 60:
            reasoning.append(f"Market viability score is positive ({viability}/100)")
        if "GO" in consensus:
            reasoning.append("Team consensus supports proceeding")
        if not reasoning:
            reasoning.append("Insufficient positive indicators for GO recommendation")

        # Next steps
        next_steps = []
        if "GO" in decision:
            next_steps = [
                "Validate market assumptions with customer interviews",
                "Create detailed 12-month execution plan",
                "Secure necessary resources and funding",
                "Begin MVP development",
                "Set up metrics and KPIs for tracking"
            ]
        elif "CONDITIONAL" in decision:
            next_steps = [
                "Address identified risks and threats",
                "Conduct additional market research",
                "Build contingency plans",
                "Schedule review after risk mitigation",
                "Re-assess viability before full commitment"
            ]
        else:
            next_steps = [
                "Identify pivot opportunities",
                "Research adjacent markets",
                "Consider partnership or acquisition opportunities",
                "Archive learnings for future reference",
                "Explore related business models"
            ]

        return {
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "next_steps": next_steps
        }


def discuss_business_case(business_case: Dict[str, Any], agents: List[Any]) -> Dict[str, Any]:
    """Factory function for agent business discussion."""
    discussion = AgentBusinessDiscussion(business_case, agents)
    return discussion.conduct_discussion()
