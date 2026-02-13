"""
Agent Orchestrator - Master coordinator
- Determines what analysis is needed
- Assigns tasks to appropriate agents
- Manages workflow and priorities
- Ensures resource efficiency
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of analysis that can be performed."""
    BUSINESS = "business"          # Market, competition, viability
    CODE = "code"                  # Structures, patterns, issues
    ARCHITECTURE = "architecture"  # System design, scalability
    RESEARCH = "research"          # Scientific analysis
    COMBINED = "combined"          # Multiple types


class AgentOrchestrator:
    """Master orchestrator that coordinates all agent work."""

    def __init__(self, agents: List[Any], memory: Any, project_path: str, project_name: str):
        self.agents = agents
        self.memory = memory
        self.project_path = Path(project_path)
        self.project_name = project_name

        # Agent specialization mapping
        self.specializations = {
            "Lyra": ["analysis", "metrics", "business"],
            "Iorek": ["architecture", "structure", "design"],
            "Marisa": ["development", "execution", "technical"],
            "Serafina": ["research", "investigation", "discovery"],
            "Lee": ["communication", "writing", "documentation"],
            "Pantalaimon": ["testing", "validation", "quality"],
            "Philip": ["coordination", "planning", "management"]
        }

        self.orchestration_log = []

    async def analyze_project(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate complete project analysis.

        Args:
            context: Project context from context_analyzer

        Returns:
            Complete analysis with agent contributions
        """

        print("\n" + "=" * 70)
        print("🎼 AGENT ORCHESTRATOR - Coordinating Comprehensive Analysis")
        print("=" * 70)

        # Step 1: Determine analysis needed
        print("\n📋 STEP 1: Determining Required Analysis")
        print("-" * 70)
        analyses_needed = self._determine_analyses(context)
        print(f"✅ Analysis plan created: {len(analyses_needed)} components")
        for analysis in analyses_needed:
            print(f"   • {analysis}")

        # Step 2: Assign agents to tasks
        print("\n👥 STEP 2: Assigning Agents to Tasks")
        print("-" * 70)
        agent_assignments = self._assign_agents(analyses_needed)

        for agent_name, task in agent_assignments.items():
            print(f"   🎯 {agent_name:12} → {task['task']}")

        # Step 3: Coordinate execution
        print("\n⚙️  STEP 3: Coordinating Agent Execution")
        print("-" * 70)

        results = {}
        for agent_name, assignment in agent_assignments.items():
            agent = next((a for a in self.agents if a.name == agent_name), None)
            if agent:
                print(f"   ▶️  {agent_name} working...")
                result = await self._execute_agent_task(agent, assignment)
                results[agent_name] = result

        # Step 4: Synthesize results
        print("\n🔄 STEP 4: Synthesizing Results")
        print("-" * 70)
        synthesis = self._synthesize_results(results, context)

        # Step 5: Record learning
        print("\n📚 STEP 5: Recording Agent Learning")
        print("-" * 70)
        self._record_learning(agent_assignments, results)

        print("\n✅ Orchestration complete!")

        return {
            "project": self.project_name,
            "context": context,
            "analyses": analyses_needed,
            "agent_assignments": agent_assignments,
            "results": results,
            "synthesis": synthesis,
            "orchestration_log": self.orchestration_log
        }

    def _determine_analyses(self, context: Dict[str, Any]) -> List[str]:
        """Determine what analyses are needed based on project context."""

        analyses = []
        project_type = context.get("project_type", "SOFTWARE")
        is_business = context.get("is_business", False)

        # Always do code analysis
        analyses.append("Code Structure Analysis")

        # If business, do business analysis
        if is_business:
            analyses.append("Business Viability Analysis")
            analyses.append("Market & Competition Research")

        # Based on type
        if project_type == "ML_TOOL":
            analyses.append("Model Architecture Review")
            analyses.append("Performance Analysis")
        elif project_type == "API":
            analyses.append("API Design & Scalability")
            analyses.append("Security Assessment")
        elif project_type == "WEB_APP":
            analyses.append("Frontend Architecture")
            analyses.append("User Experience Assessment")
        elif project_type == "DATA_TOOL":
            analyses.append("Data Pipeline Analysis")
            analyses.append("Query Optimization")

        # Always add strategic analysis
        analyses.append("Strategic Recommendations")

        self.orchestration_log.append({
            "step": "Analyses Determined",
            "count": len(analyses),
            "analyses": analyses
        })

        return analyses

    def _assign_agents(self, analyses: List[str]) -> Dict[str, Dict[str, Any]]:
        """Assign best agents to each analysis task."""

        assignments = {}

        # Mapping of analysis to best agent
        analysis_to_agent = {
            "Business Viability Analysis": "Lyra",
            "Market & Competition Research": "Serafina",
            "Code Structure Analysis": "Marisa",
            "Model Architecture Review": "Iorek",
            "API Design & Scalability": "Iorek",
            "Frontend Architecture": "Iorek",
            "Data Pipeline Analysis": "Marisa",
            "Performance Analysis": "Marisa",
            "Security Assessment": "Pantalaimon",
            "User Experience Assessment": "Lee",
            "Query Optimization": "Marisa",
            "Strategic Recommendations": "Philip"
        }

        # Create assignments
        for analysis in analyses:
            agent_name = analysis_to_agent.get(analysis, "Philip")
            assignments[agent_name] = {
                "task": analysis,
                "priority": "high" if "Business" in analysis else "medium",
                "status": "pending"
            }

        self.orchestration_log.append({
            "step": "Agents Assigned",
            "assignments": len(assignments),
            "agents": list(assignments.keys())
        })

        return assignments

    async def _execute_agent_task(self, agent: Any, assignment: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific agent task."""

        task = assignment['task']
        agent.start_task(task)

        # Simulate agent work (in production, would call specific analysis)
        result = {
            "agent": agent.name,
            "task": task,
            "status": "completed",
            "findings": f"Analysis of {task} completed by {agent.name}",
            "insights": [
                "Key insight 1 from analysis",
                "Key insight 2 from analysis",
                "Key insight 3 from analysis"
            ]
        }

        # Small delay to simulate thinking time
        await asyncio.sleep(0.5)

        self.orchestration_log.append({
            "step": f"Agent Task: {agent.name}",
            "task": task,
            "status": "completed"
        })

        return result

    def _synthesize_results(self, results: Dict[str, Dict], context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all agent results into coherent analysis."""

        synthesis = {
            "summary": f"Comprehensive analysis of {self.project_name}",
            "key_findings": [],
            "recommendations": [],
            "next_steps": [],
            "overall_assessment": ""
        }

        # Aggregate findings
        for agent_name, result in results.items():
            if result.get("insights"):
                synthesis["key_findings"].extend(result["insights"][:2])

        # Generate recommendations
        if context.get("is_business"):
            synthesis["recommendations"].append("Conduct market validation with customers")
            synthesis["recommendations"].append("Develop detailed business plan")
            synthesis["recommendations"].append("Identify funding requirements")

        synthesis["recommendations"].append("Implement continuous monitoring")
        synthesis["recommendations"].append("Document best practices")

        # Next steps
        synthesis["next_steps"] = [
            "1. Review agent recommendations",
            "2. Prioritize action items",
            "3. Assign team to execute",
            "4. Track progress and KPIs",
            "5. Schedule follow-up analysis"
        ]

        # Overall assessment
        synthesis["overall_assessment"] = "Project analysis comprehensive. Ready for decision-making."

        self.orchestration_log.append({
            "step": "Results Synthesized",
            "findings": len(synthesis["key_findings"]),
            "recommendations": len(synthesis["recommendations"])
        })

        return synthesis

    def _record_learning(self, assignments: Dict[str, Dict], results: Dict[str, Dict]):
        """Record agent learning from this orchestration."""

        for agent_name, assignment in assignments.items():
            agent = next((a for a in self.agents if a.name == agent_name), None)
            if agent:
                result = results.get(agent_name, {})
                self.memory.add_experience(
                    agent_id=agent.id,
                    task=f"Orchestrated: {assignment['task']}",
                    approach=f"Coordinated by orchestrator for {self.project_name}",
                    result=result.get("status", "unknown"),
                    success=result.get("status") == "completed",
                    learned=f"Experience: {assignment['task']} - {self.project_name}"
                )
                agent.complete_task(success=True)

        self.orchestration_log.append({
            "step": "Learning Recorded",
            "agents_updated": len(assignments)
        })


async def orchestrate_analysis(
    agents: List[Any],
    memory: Any,
    project_path: str,
    project_name: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Factory function for agent orchestration."""

    orchestrator = AgentOrchestrator(agents, memory, project_path, project_name)
    return await orchestrator.analyze_project(context)
