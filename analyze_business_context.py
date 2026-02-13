#!/usr/bin/env python3
"""
Business Context & Competitive Analysis
Comprehensive business analysis with agent consultation

Analyzes:
1. Project context and type
2. Market research and competition
3. Competitive advantages and threats
4. Agent discussion and consensus
5. GO/NO-GO recommendation
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.INTEGRATION.file_sync import get_project_finder
from core.agents import list_agents
from core.analysis import analyze_business, discuss_business_case
from core.memory import Memory


async def main():
    """Main business analysis flow."""

    print("\n" + "="*70)
    print("🏢 BUSINESS CONTEXT & COMPETITIVE ANALYSIS")
    print("="*70)
    print("\nThis analysis:")
    print("✅ Discovers project type and objectives")
    print("✅ Researches market and competition")
    print("✅ Analyzes competitive position")
    print("✅ Convenes agent consultation meeting")
    print("✅ Generates GO/NO-GO recommendation")

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

    # Run business analysis
    print()
    business_case = await analyze_business(
        selected_project['path'],
        selected_project['title']
    )

    # If it's a business, conduct agent discussion
    if business_case.get("status") == "READY" and business_case.get("ready_for_agent_discussion"):
        print("\n" + "="*70)
        print("📞 CONVENING AGENT CONSULTATION MEETING")
        print("="*70)

        agents = list_agents()
        memory = Memory()

        discussion_result = discuss_business_case(business_case, agents)

        # Record experiences
        print("\n📚 Recording consultation experiences...")
        for agent in agents:
            perspective = discussion_result['perspectives'].get(agent.name, {})
            memory.add_experience(
                agent_id=agent.id,
                task=f"Business consultation for {selected_project['title']}",
                approach=f"{agent.role}: {perspective.get('position', 'Consultant')}",
                result=f"Provided perspective: {perspective.get('recommendation', 'Unknown')}",
                success=True,
                learned=f"Business analysis expertise: {selected_project['title']}",
            )
            agent.complete_task(success=True)

        print("\n✅ All agent perspectives recorded in memory")

        # Display final summary
        print("\n" + "="*70)
        print("📊 FINAL BUSINESS ANALYSIS SUMMARY")
        print("="*70)

        recommendation = discussion_result.get('recommendation', {})
        print(f"\n{recommendation.get('decision', 'Unknown')}")
        print(f"Confidence: {recommendation.get('confidence', 0)}/10")

        print("\n📋 Summary of Findings:")
        context = business_case.get('context', {})
        print(f"  Project Type: {context.get('project_type')}")
        print(f"  Viability Score: {business_case.get('viability_score', 0)}/100")

        competitive = business_case.get('competitive_analysis', {})
        print(f"  Competitive Advantages: {len(competitive.get('competitive_advantages', []))}")
        print(f"  Competitive Disadvantages: {len(competitive.get('competitive_disadvantages', []))}")
        print(f"  Market Threats: {len(competitive.get('threats', []))}")

        print("\n✨ Business analysis complete!")

    else:
        print("\n⚠️  Project is not a business - skipping agent consultation")
        print("   This analysis is designed for business projects")

    print("\n" + "="*70 + "\n")


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
