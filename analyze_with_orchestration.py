#!/usr/bin/env python3
"""
Complete Project Analysis with Agent Orchestration
- Discovers context
- Runs business analysis (if business)
- Orchestrates full multi-agent analysis
- Generates comprehensive report
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.INTEGRATION.file_sync import get_project_finder
from core.agents import list_agents
from core.memory import Memory
from core.analysis import analyze_business
from core.orchestration import orchestrate_analysis


async def main():
    """Main orchestrated analysis flow."""

    print("\n" + "="*70)
    print("🎼 FULL PROJECT ANALYSIS WITH AGENT ORCHESTRATION")
    print("="*70)
    print("\nThis comprehensive analysis:")
    print("✅ Discovers project context and type")
    print("✅ Analyzes business viability (if applicable)")
    print("✅ Orchestrates full multi-agent analysis")
    print("✅ Coordinates 7 agents working together")
    print("✅ Generates final synthesis and recommendations")

    # Find projects
    print("\n📁 Finding projects...")
    finder = get_project_finder()
    projects = finder.find_all_projects()

    apps_projects = [p for p in projects if p['source'] == 'Apps']

    print(f"\nAvailable projects:")
    for i, p in enumerate(apps_projects, 1):
        print(f"  {i}. {p['title']}")

    # Select project
    choice = input("\nSelect project number (or '0' to exit): ").strip()

    if choice == '0':
        print("Exiting...")
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(apps_projects):
            print("Invalid choice!")
            return
    except ValueError:
        print("Invalid input!")
        return

    selected_project = apps_projects[idx]

    # Initialize agents and memory
    agents = list_agents()
    memory = Memory()

    # Step 1: Business analysis (if applicable)
    print("\n" + "="*70)
    print("📊 PHASE 1: PROJECT CONTEXT & BUSINESS ANALYSIS")
    print("="*70)

    business_case = await analyze_business(
        selected_project['path'],
        selected_project['title']
    )

    context = business_case.get('context', {})
    is_business = business_case.get("ready_for_agent_discussion", False)

    # Step 2: Agent orchestration
    print("\n" + "="*70)
    print("🎼 PHASE 2: AGENT ORCHESTRATION")
    print("="*70)

    orchestration = await orchestrate_analysis(
        agents,
        memory,
        selected_project['path'],
        selected_project['title'],
        context
    )

    # Step 3: Final synthesis
    print("\n" + "="*70)
    print("📋 PHASE 3: FINAL SYNTHESIS")
    print("="*70)

    synthesis = orchestration.get('synthesis', {})
    print(f"\n📌 Summary: {synthesis.get('summary')}")
    print(f"\n🔍 Key Findings ({len(synthesis.get('key_findings', []))} total):")
    for finding in synthesis.get('key_findings', [])[:5]:
        print(f"   • {finding}")

    print(f"\n💡 Recommendations ({len(synthesis.get('recommendations', []))} total):")
    for rec in synthesis.get('recommendations', [])[:5]:
        print(f"   → {rec}")

    print(f"\n📈 Assessment: {synthesis.get('overall_assessment')}")

    # Step 4: Business recommendation (if business)
    if is_business and business_case.get('status') == 'READY':
        print("\n" + "="*70)
        print("💼 BUSINESS VIABILITY ASSESSMENT")
        print("="*70)

        competitive = business_case.get('competitive_analysis', {})
        print(f"Viability Score: {business_case.get('viability_score')}/100")
        print(f"Advantages: {len(competitive.get('competitive_advantages', []))}")
        print(f"Disadvantages: {len(competitive.get('competitive_disadvantages', []))}")
        print(f"Threats: {len(competitive.get('threats', []))}")

    # Step 5: Agent summary
    print("\n" + "="*70)
    print("👥 AGENT PARTICIPATION SUMMARY")
    print("="*70)

    assignments = orchestration.get('agent_assignments', {})
    print(f"\nAgents involved: {len(assignments)}")
    for agent_name, assignment in assignments.items():
        print(f"  ✅ {agent_name:12} - {assignment['task']}")

    # Record overall experience
    print("\n📚 Recording orchestration experience...")
    for agent in agents:
        memory.add_experience(
            agent_id=agent.id,
            task=f"Full orchestration for {selected_project['title']}",
            approach=f"Coordinated by orchestrator",
            result="comprehensive_analysis_completed",
            success=True,
            learned=f"Orchestrated analysis experience: {selected_project['title']}"
        )

    print("✅ All experiences recorded\n")

    # Final summary
    print("\n" + "="*70)
    print("✨ ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nProject: {selected_project['title']}")
    print(f"Type: {context.get('project_type')}")
    print(f"Agents Coordinated: {len(agents)}")
    print(f"Analyses Performed: {len(orchestration.get('analyses', []))}")
    print(f"Status: Ready for decision-making")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
