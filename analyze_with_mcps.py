#!/usr/bin/env python3
"""
Real Project Analysis using MCPs + Local MLX
- MLX (Qwen3): Code analysis
- Perplexity MCP: Web research (port 3007)
- Obsidian MCP: Save findings (port 3001)
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.INTEGRATION.file_sync import get_project_finder
from core.mcp_analyzer import get_mcp_analyzer


async def main():
    """Run real analysis on a selected project"""

    print("\n" + "="*70)
    print("🔬 REAL ANALYSIS - Using MLX + MCPs")
    print("="*70)

    # Initialize analyzer
    print("\n🚀 Initializing analysis engine...")
    analyzer = get_mcp_analyzer()

    print(f"\nAvailable tools:")
    print(f"  {'✅' if analyzer.mlx_available else '❌'} MLX Local LLM (Qwen3)")
    print(f"  {'✅' if analyzer.perplexity_available else '❌'} Perplexity MCP (port 3007)")
    print(f"  {'✅' if analyzer.obsidian_available else '❌'} Obsidian MCP (port 3001)")
    print(f"  {'✅' if analyzer.paper_search_available else '❌'} Paper Search MCP (port 3003)")

    if not analyzer.mlx_available:
        print("\n❌ ERROR: MLX not available!")
        print("   Install with: pip install mlx-lm")
        return

    # Find projects
    print("\n📁 Finding projects...")
    finder = get_project_finder()
    projects = finder.find_all_projects()

    apps_projects = [p for p in projects if p['source'] == 'Apps']

    print(f"\nAvailable executable projects:")
    for i, p in enumerate(apps_projects, 1):
        print(f"  {i}. {p['title']}")

    # Select project
    choice = input("\nSelect project number (or '0' to exit): ").strip()

    if choice == '0':
        print("Exiting...")
        return

    try:
        project_idx = int(choice) - 1
        if project_idx < 0 or project_idx >= len(apps_projects):
            print("Invalid choice!")
            return
    except ValueError:
        print("Invalid input!")
        return

    selected_project = apps_projects[project_idx]

    print(f"\n" + "="*70)
    print(f"📊 ANALYZING: {selected_project['title']}")
    print(f"📂 Path: {selected_project['path']}")
    print("="*70)

    # Run analysis
    print(f"\n⏳ This may take a moment...")
    findings = await analyzer.analyze_project_real(
        selected_project['path'],
        selected_project['title']
    )

    # Display results
    print(f"\n" + "="*70)
    print("📊 ANALYSIS RESULTS")
    print("="*70)

    print(f"\n✅ Files analyzed: {len(findings['files_analyzed'])}")

    if findings['critical_problems']:
        print(f"\n🔴 CRITICAL PROBLEMS ({len(findings['critical_problems'])} found):")
        for problem in findings['critical_problems'][:5]:
            print(f"\n  File: {problem['file']}")
            print(f"  Issue: {problem['issue'].get('description', 'Unknown')}")

    if findings['performance_issues']:
        print(f"\n⚡ PERFORMANCE ISSUES ({len(findings['performance_issues'])} found):")
        for issue in findings['performance_issues'][:3]:
            print(f"\n  File: {issue['file']}")
            print(f"  Issue: {issue['issue'].get('description', 'Unknown')}")

    print(f"\n💡 ACTIONABLE FIXES ({len(findings['actionable_fixes'])} recommendations):")
    for fix in findings['actionable_fixes'][:5]:
        print(f"\n  [{fix['severity']}] {fix['problem']}")
        print(f"  File: {fix['file']}")
        print(f"  Time: {fix['estimated_time']}")
        if fix['fix_description']:
            print(f"  Fix: {fix['fix_description'][:100]}...")

    # Save to Obsidian
    if analyzer.obsidian_available:
        print(f"\n💾 Saving to Obsidian...")
        saved = await analyzer.save_to_obsidian(findings)
        if saved:
            print(f"✅ Analysis saved to Obsidian vault")
        else:
            print(f"⚠️  Could not save to Obsidian")

    # Search for context
    if analyzer.perplexity_available:
        print(f"\n🔎 Searching for relevant context...")
        context = await analyzer.search_context(
            selected_project['title'],
            f"Best practices for {selected_project['title']} optimization"
        )
        if "error" not in context:
            print(f"✅ Found research context")

    print(f"\n" + "="*70)
    print("✨ Analysis complete!")
    print("="*70 + "\n")


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
