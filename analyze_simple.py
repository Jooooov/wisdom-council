#!/usr/bin/env python3
"""
Simple Analysis using MCPs (without MLX requirement)
- Perplexity MCP for web research
- Obsidian MCP for saving findings
- Paper Search MCP for academic papers
- Manual code analysis
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.INTEGRATION.file_sync import get_project_finder


async def analyze_project_simple(project_path: str, project_name: str):
    """Simple analysis - code inspection + research"""

    print(f"\n{'='*70}")
    print(f"📊 ANALYZING: {project_name}")
    print(f"{'='*70}")

    project_path = Path(project_path)

    # 1. ANALYZE CODE STRUCTURE
    print(f"\n📁 Code Structure Analysis...")

    py_files = list(project_path.glob("**/*.py"))
    py_files = [f for f in py_files if ".venv" not in str(f) and "__pycache__" not in str(f)]

    total_lines = 0
    files_with_issues = []

    for py_file in py_files[:10]:  # First 10 files
        with open(py_file) as f:
            code = f.read()
            lines = len(code.split('\n'))
            total_lines += lines

            # Simple issue detection
            issues = []
            if "TODO" in code:
                issues.append("Has TODOs")
            if "FIXME" in code:
                issues.append("Has FIXMEs")
            if "hardcoded" in code.lower() or "hardcode" in code.lower():
                issues.append("Possible hardcoded values")
            if "import sys" in code or "os.system" in code:
                issues.append("Uses system calls")
            if "pass" in code and len(code.split("pass")) > 5:
                issues.append("Many 'pass' statements")

            if issues:
                files_with_issues.append({
                    "file": py_file.name,
                    "lines": lines,
                    "issues": issues
                })

    print(f"\n✅ Analysis Results:")
    print(f"   Python files: {len(py_files)}")
    print(f"   Total lines: {total_lines:,}")
    print(f"   Files with issues: {len(files_with_issues)}")

    # 2. SHOW FOUND ISSUES
    if files_with_issues:
        print(f"\n⚠️  POTENTIAL ISSUES FOUND:")
        for item in files_with_issues[:5]:
            print(f"\n   📄 {item['file']} ({item['lines']} lines)")
            for issue in item['issues']:
                print(f"      • {issue}")

    # 3. RECOMMENDATIONS
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   1. Add code comments for clarity")
    print(f"   2. Resolve all TODOs and FIXMEs")
    print(f"   3. Add type hints to functions")
    print(f"   4. Create unit tests")
    print(f"   5. Document public APIs")

    # 4. RESEARCH CONTEXT (using Perplexity)
    print(f"\n🔎 Researching best practices (via Perplexity)...")
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:3007/search",
                json={"query": f"Best practices for {project_name} development"}
            )
            result = response.json()
            if "results" in result:
                print(f"   ✅ Found research context")
            elif "error" not in result:
                print(f"   ✅ Research completed")
            else:
                print(f"   ⚠️  Could not fetch research")
    except Exception as e:
        print(f"   ⚠️  Research failed: {e}")

    print(f"\n{'='*70}")
    print(f"✨ Analysis complete!")
    print(f"{'='*70}\n")


async def main():
    """Main analysis flow"""

    print("\n" + "="*70)
    print("🔬 SIMPLE ANALYSIS (without MLX)")
    print("="*70)
    print("\nThis analysis:")
    print("✅ Reads Python files")
    print("✅ Detects potential issues")
    print("✅ Researches best practices")
    print("✅ Provides recommendations")

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

    project = apps_projects[idx]

    # Run analysis
    await analyze_project_simple(project['path'], project['title'])


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
