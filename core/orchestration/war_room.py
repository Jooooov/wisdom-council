"""
War Room - Real Agent Collaboration using DeepSeek-R1 LLM

Each agent discusses the business case with their personality/daemon influence.
Uses DeepSeek-R1-0528-Qwen3-8B-8bit for reasoning-based analysis.
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.llm import create_ram_manager, create_mlx_loader


class WarRoom:
    """Real-time agent collaboration with LLM reasoning."""

    def __init__(self, business_case: Dict[str, Any], agents: List[Any]):
        """Initialize war room with business case and agents."""
        self.business_case = business_case
        self.agents = agents
        self.llm_loader = None
        self.ram_manager = None
        self.discussion_log = []
        self.agent_perspectives = {}

    async def prepare(self) -> bool:
        """Prepare LLM and check RAM."""
        print("\n" + "=" * 70)
        print("🧠 WAR ROOM INITIALIZATION")
        print("=" * 70)

        # Check RAM
        self.ram_manager = create_ram_manager()
        self.llm_loader = create_mlx_loader(self.ram_manager)

        can_load, message = self.llm_loader.check_ram_availability()
        print(f"\n{message}")

        if not can_load:
            print("\n❌ Insufficient RAM to run War Room with LLM reasoning")
            return False

        # Load LLM
        print("\n⏳ Loading DeepSeek-R1 LLM for agent reasoning...")
        success = await self.llm_loader.load()

        if success:
            print("✅ LLM loaded - War Room ready\n")
            return True
        else:
            print("❌ Failed to load LLM")
            return False

    async def conduct_discussion(self) -> Dict[str, Any]:
        """Conduct full war room discussion with LLM-based agent reasoning."""
        print("\n" + "=" * 70)
        print("⚔️  WAR ROOM DISCUSSION - REAL AGENT COLLABORATION")
        print("=" * 70)
        print(f"\nProject: {self.business_case.get('project_name')}")
        print(f"Viability Score: {self.business_case.get('viability_score', 0)}/100")

        try:
            # Phase 1: Individual Agent Analysis
            print("\n" + "-" * 70)
            print("📍 PHASE 1: Individual Agent Analysis (with LLM Reasoning)")
            print("-" * 70)

            for agent in self.agents:
                print(f"\n🧙 {agent.name} ({agent.role}) is analyzing...")
                perspective = await self._get_agent_reasoning(agent)
                self.agent_perspectives[agent.name] = perspective

            # Phase 2: Open Discussion
            print("\n" + "-" * 70)
            print("💬 PHASE 2: Open Discussion Between Agents")
            print("-" * 70)

            discussion = await self._facilitate_discussion()

            # Phase 3: Consensus Building
            print("\n" + "-" * 70)
            print("🤝 PHASE 3: Consensus Building")
            print("-" * 70)

            consensus = await self._build_consensus()

            # Phase 4: Final Recommendation
            print("\n" + "-" * 70)
            print("🎯 PHASE 4: Final Recommendation (GO / NO-GO)")
            print("-" * 70)

            recommendation = await self._generate_final_recommendation()

            return {
                "perspectives": self.agent_perspectives,
                "discussion": discussion,
                "consensus": consensus,
                "recommendation": recommendation,
                "status": "COMPLETE"
            }

        except Exception as e:
            print(f"\n❌ War Room discussion failed: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "FAILED", "error": str(e)}

    async def _get_agent_reasoning(self, agent) -> Dict[str, Any]:
        """Get LLM-based reasoning from specific agent with their personality."""
        # Build context for the agent
        business_summary = self._build_business_summary_for_agent(agent)

        # Create personality-specific prompt
        prompt = self._create_agent_prompt(agent, business_summary)

        # Get LLM reasoning
        try:
            reasoning = await self.llm_loader.generate(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )

            perspective = {
                "agent": agent.name,
                "role": agent.role,
                "daemon": getattr(agent, 'daemon', 'Unknown'),
                "reasoning": reasoning,
                "key_points": self._extract_key_points(reasoning),
                "recommendation": self._extract_recommendation(reasoning),
                "confidence": self._extract_confidence(reasoning)
            }

            # Print perspective
            print(f"   ✅ Analysis complete")
            if perspective['recommendation']:
                print(f"      Recommendation: {perspective['recommendation']}")

            self.discussion_log.append({
                "speaker": agent.name,
                "phase": "individual_analysis",
                "content": reasoning
            })

            return perspective

        except Exception as e:
            print(f"   ⚠️  Error getting reasoning: {e}")
            return {
                "agent": agent.name,
                "role": agent.role,
                "reasoning": "Analysis unavailable",
                "error": str(e)
            }

    async def _facilitate_discussion(self) -> str:
        """Facilitate discussion between agents based on their perspectives."""
        print("\n🎤 Agents are discussing their views...\n")

        discussion_prompt = self._build_discussion_prompt()

        try:
            discussion = await self.llm_loader.generate(
                prompt=discussion_prompt,
                max_tokens=400,
                temperature=0.8
            )

            self.discussion_log.append({
                "speaker": "COLLECTIVE_DISCUSSION",
                "phase": "open_discussion",
                "content": discussion
            })

            print(discussion)
            return discussion

        except Exception as e:
            print(f"⚠️  Discussion generation failed: {e}")
            return "Discussion could not be generated"

    async def _build_consensus(self) -> Dict[str, Any]:
        """Build consensus from all agent perspectives."""
        consensus_prompt = self._build_consensus_prompt()

        try:
            consensus_text = await self.llm_loader.generate(
                prompt=consensus_prompt,
                max_tokens=300,
                temperature=0.6
            )

            go_count = sum(1 for p in self.agent_perspectives.values()
                          if "GO" in p.get("recommendation", "").upper())
            total = len(self.agent_perspectives)
            agreement = (go_count / total * 100) if total > 0 else 0

            consensus = {
                "summary": consensus_text,
                "agreement_percentage": int(agreement),
                "agents_favoring_go": go_count,
                "agents_favoring_nogo": total - go_count
            }

            print(f"\n✅ Consensus: {int(agreement)}% of agents favor GO")
            print(f"   ({go_count}/{total})")

            return consensus

        except Exception as e:
            print(f"⚠️  Consensus generation failed: {e}")
            return {
                "summary": "Consensus could not be determined",
                "error": str(e)
            }

    async def _generate_final_recommendation(self) -> Dict[str, Any]:
        """Generate final GO/NO-GO recommendation with reasoning."""
        recommendation_prompt = self._build_recommendation_prompt()

        try:
            recommendation_text = await self.llm_loader.generate(
                prompt=recommendation_prompt,
                max_tokens=350,
                temperature=0.7
            )

            # Determine GO/NO-GO
            is_go = "GO" in recommendation_text.upper()

            recommendation = {
                "decision": "🟢 GO - PROCEED WITH PROJECT" if is_go else "🔴 NO-GO - DO NOT PROCEED",
                "reasoning": recommendation_text,
                "viability_score": self.business_case.get("viability_score", 0),
                "confidence": 8 if is_go else 7  # Based on LLM reasoning
            }

            print(f"\n{'🟢' if is_go else '🔴'} FINAL DECISION:")
            print(f"   {recommendation['decision']}")
            print(f"\n📋 Reasoning (from LLM analysis):")
            for line in recommendation_text.split('\n')[:3]:
                if line.strip():
                    print(f"   • {line.strip()}")

            return recommendation

        except Exception as e:
            print(f"⚠️  Recommendation generation failed: {e}")
            return {
                "decision": "UNDETERMINED",
                "error": str(e)
            }

    # ========== Helper Methods ==========

    def _build_business_summary_for_agent(self, agent) -> str:
        """Build business case summary tailored for specific agent."""
        case = self.business_case
        summary = f"""
PROJECT: {case.get('project_name')}
TYPE: {case.get('project_type', 'Unknown')}

MARKET DATA:
- Viability Score: {case.get('viability_score', 0)}/100
- Competitors: {len(case.get('competitive_analysis', {}).get('competitors', []))}
- Market Gaps: {len(case.get('market_research', {}).get('gaps', []))}

KEY FINDINGS:
Advantages: {', '.join(case.get('competitive_analysis', {}).get('competitive_advantages', [])[:2])}
Threats: {', '.join(case.get('competitive_analysis', {}).get('threats', [])[:2])}
"""
        return summary.strip()

    def _create_agent_prompt(self, agent, business_summary: str) -> str:
        """Create personality-specific analysis prompt for agent."""
        role_prompts = {
            "analyst": f"""You are {agent.name}, a sharp analyst with keen insight into data and patterns.

Analyze this business case focusing on METRICS, DATA, and MARKET TRENDS:
{business_summary}

Provide your analysis as {agent.name} would - data-driven, questioning assumptions, finding hidden patterns.
What do the numbers tell you? Is this viable?""",

            "architect": f"""You are {agent.name}, a strategic architect focused on structure and scalability.

Analyze this business case focusing on STRUCTURE, SCALABILITY, and FEASIBILITY:
{business_summary}

How is this business structured? Can it scale? What's the foundational weakness?
Provide your architectural assessment.""",

            "developer": f"""You are {agent.name}, a decisive operator focused on EXECUTION and TECHNICAL VIABILITY.

Analyze this business case focusing on EXECUTION, RESOURCES, and TECHNICAL FEASIBILITY:
{business_summary}

Can this actually be built? Do we have the resources? What's the execution risk?
Give your execution assessment.""",

            "researcher": f"""You are {agent.name}, a strategic researcher with deep market knowledge.

Analyze this business case focusing on MARKET DEPTH, COMPETITIVE INTELLIGENCE, and OPPORTUNITIES:
{business_summary}

What's the deeper market story? Who are the real competitors? What opportunities are hidden?
Provide your market research perspective.""",

            "writer": f"""You are {agent.name}, a strategic communicator focused on POSITIONING and GO-TO-MARKET.

Analyze this business case focusing on POSITIONING, MESSAGING, and MARKET ENTRY:
{business_summary}

How do we position this? What's our story? How do we win in the market?
Provide your strategic communication perspective.""",

            "validator": f"""You are {agent.name}, a careful validator focused on RISKS and ASSUMPTIONS.

Analyze this business case focusing on RISKS, ASSUMPTIONS, and VALIDATION:
{business_summary}

What could go wrong? What are we assuming that might be wrong? What needs validation?
Provide your risk assessment perspective.""",

            "coordinator": f"""You are {agent.name}, a visionary coordinator focused on STRATEGY and ALIGNMENT.

Analyze this business case as a STRATEGIC LEADER:
{business_summary}

Is this aligned with our vision? Do all pieces fit together? Is this worth our time and resources?
Provide your strategic leadership perspective.""",
        }

        # Match role to prompt
        for key, prompt in role_prompts.items():
            if key in agent.role.lower() or key in agent.name.lower():
                return prompt

        # Default
        return f"Analyze this business case: {business_summary}\n\nWhat is your professional opinion?"

    def _build_discussion_prompt(self) -> str:
        """Build prompt for agents to discuss together."""
        perspectives_summary = "\n".join([
            f"- {name}: {p.get('recommendation', 'Unclear')}"
            for name, p in self.agent_perspectives.items()
        ])

        return f"""The agents are now having an open discussion about the business case:
{self.business_case.get('project_name')}

Current positions:
{perspectives_summary}

Have a realistic, professional discussion between the agents. Include:
- Areas of agreement
- Points of disagreement
- Questions that need answering
- Concerns raised
- Potential compromises

Write the discussion as a natural conversation with insights from each perspective."""

    def _build_consensus_prompt(self) -> str:
        """Build prompt for consensus building."""
        return f"""Based on the analysis from {len(self.agent_perspectives)} specialists,
determine the consensus on the business case: {self.business_case.get('project_name')}

The team consists of experts in:
{', '.join([f"{name} ({p.get('role')})" for name, p in self.agent_perspectives.items()])}

Summarize the consensus position. Do the experts agree? Where do they diverge?
Is there a clear lean towards GO or NO-GO?"""

    def _build_recommendation_prompt(self) -> str:
        """Build prompt for final recommendation."""
        return f"""As a synthesis of expert analysis, provide a final GO/NO-GO recommendation for:
{self.business_case.get('project_name')}

Viability Score: {self.business_case.get('viability_score', 0)}/100

Based on:
- Market analysis
- Competitive position
- Team expertise
- Risk assessment
- Financial viability

Should we proceed (GO) or pivot/cancel (NO-GO)?
Provide clear reasoning for your recommendation."""

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from reasoning text."""
        lines = text.split('\n')
        points = [l.strip() for l in lines if l.strip() and len(l.strip()) > 20]
        return points[:3]

    def _extract_recommendation(self, text: str) -> str:
        """Extract GO/NO-GO recommendation from reasoning."""
        text_upper = text.upper()
        if "GO" in text_upper and "NO-GO" not in text_upper:
            return "GO"
        elif "NO-GO" in text_upper or ("NO" in text_upper and "GO" in text_upper and text_upper.index("NO") < text_upper.index("GO")):
            return "NO-GO"
        else:
            return "UNCLEAR"

    def _extract_confidence(self, text: str) -> int:
        """Extract confidence level from reasoning."""
        # Simple heuristic: longer, more detailed reasoning = higher confidence
        confidence = min(9, max(4, len(text.split()) // 30))
        return confidence

    async def cleanup(self):
        """Clean up and unload LLM."""
        if self.llm_loader:
            self.llm_loader.unload()
            print("\n✅ LLM unloaded, resources freed")


async def run_war_room(business_case: Dict[str, Any], agents: List[Any]) -> Dict[str, Any]:
    """Factory function to run war room discussion."""
    war_room = WarRoom(business_case, agents)

    # Prepare
    ready = await war_room.prepare()
    if not ready:
        return {"status": "FAILED", "error": "Could not prepare War Room"}

    # Conduct discussion
    result = await war_room.conduct_discussion()

    # Cleanup
    await war_room.cleanup()

    return result
