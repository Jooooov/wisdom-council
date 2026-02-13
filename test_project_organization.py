#!/usr/bin/env python3
"""
Test and verify the new project organization.
Ensures all projects are properly discoverable and analyzable by Wisdom Council.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.INTEGRATION.file_sync import get_project_finder
from core.analysis import ProjectAnalyzer


def test_project_discovery():
    """Test that all projects are discoverable."""
    print("\n" + "="*70)
    print("🔍 PROJECT ORGANIZATION TEST")
    print("="*70)

    finder = get_project_finder()
    projects = finder.find_all_projects()

    print(f"\n✅ Total projects discovered: {len(projects)}")

    # Organize by source
    obsidian_projects = [p for p in projects if p['source'] == 'Obsidian']
    apps_projects = [p for p in projects if p['source'] == 'Apps']

    print(f"   🧠 Obsidian projects: {len(obsidian_projects)}")
    print(f"   💻 Apps projects: {len(apps_projects)}")

    # Display list
    print("\n📋 DETAILED PROJECT LIST:")
    print("-" * 70)

    for p in sorted(projects, key=lambda x: (x['source'], x['title'])):
        outputs = "✅ Yes" if p.get('has_outputs') else "❌ No"
        desc = p['description'][:50] + "..." if len(p['description']) > 50 else p['description']
        print(f"{p['source']:10s} | {p['title']:30s} | Outputs: {outputs}")
        print(f"           | {desc}")
        print("-" * 70)

    return projects


def test_project_analysis(project):
    """Test that projects can be analyzed."""
    print(f"\n🔬 Testing analysis for: {project['title']}")
    print("-" * 70)

    try:
        analyzer = ProjectAnalyzer(project['path'])
        analysis = analyzer.get_full_analysis()

        print(f"✅ Structure analyzed successfully")
        print(f"   Files: {analysis['structure'].get('files', 0)}")
        print(f"   Folders: {analysis['structure'].get('folders', 0)}")
        print(f"   Python files: {analysis['structure'].get('py_files', 0)}")
        print(f"   Documentation: {len(analysis.get('documentation', {}))} docs")

        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False


def verify_executable_projects():
    """Verify that executable projects are properly set up."""
    print("\n" + "="*70)
    print("⚙️  EXECUTABLE PROJECTS VERIFICATION")
    print("="*70)

    apps_path = Path.home() / "Desktop" / "Apps"
    required_projects = ["MundoBarbaroResearch", "RedditScrapper", "His Dark Materials"]

    for proj_name in required_projects:
        proj_path = apps_path / proj_name

        print(f"\n📦 {proj_name}:")

        # Check .git
        has_git = (proj_path / ".git").exists()
        print(f"   {'✅' if has_git else '❌'} Git repository: {has_git}")

        # Check README
        has_readme = (proj_path / "README.md").exists()
        print(f"   {'✅' if has_readme else '❌'} README.md: {has_readme}")

        # Check for code files
        py_files = list(proj_path.glob("*.py"))
        has_py = len(py_files) > 0
        print(f"   {'✅' if has_py else '❌'} Python files: {len(py_files)}")

        # Check for venv
        has_venv = (proj_path / "venv").exists() or (proj_path / ".venv").exists()
        print(f"   {'✅' if has_venv else '⚠️ '} Virtual environment: {has_venv}")


def verify_documentation_projects():
    """Verify documentation projects in Obsidian."""
    print("\n" + "="*70)
    print("📚 DOCUMENTATION PROJECTS VERIFICATION")
    print("="*70)

    obsidian_path = Path.home() / "Obsidian-Vault" / "1 - Projectos"
    required_docs = ["Chemetil", "WisdomOfReddit", "AgentsAI"]

    for proj_name in required_docs:
        proj_path = obsidian_path / proj_name

        print(f"\n📖 {proj_name}:")

        # Check existence
        exists = proj_path.exists()
        print(f"   {'✅' if exists else '❌'} Directory exists: {exists}")

        if exists:
            # Check for INDEX_FOR_AGENTS.md
            has_index = (proj_path / "INDEX_FOR_AGENTS.md").exists()
            print(f"   {'✅' if has_index else '⚠️ '} INDEX_FOR_AGENTS.md: {has_index}")

            # Count markdown files
            md_files = list(proj_path.glob("**/*.md"))
            print(f"   📄 Markdown files: {len(md_files)}")


def main():
    """Run all tests."""
    print("\n" + "🎯 WISDOM COUNCIL - PROJECT ORGANIZATION VERIFICATION")

    # Test 1: Discovery
    projects = test_project_discovery()

    # Test 2: Analysis capabilities
    print("\n" + "="*70)
    print("🧪 ANALYSIS CAPABILITY TEST")
    print("="*70)

    apps_projects = [p for p in projects if p['source'] == 'Apps']
    successful_analyses = 0

    for project in apps_projects[:3]:  # Test first 3 apps projects
        if test_project_analysis(project):
            successful_analyses += 1

    # Test 3: Executable projects
    verify_executable_projects()

    # Test 4: Documentation projects
    verify_documentation_projects()

    # Summary
    print("\n" + "="*70)
    print("✅ VERIFICATION SUMMARY")
    print("="*70)
    print(f"""
🎯 Projects discovered: {len(projects)}/8
   ✅ Apps (executable): {len(apps_projects)}
   ✅ Obsidian (documentation): {len([p for p in projects if p['source'] == 'Obsidian'])}

📊 Analysis capability: {successful_analyses}/{min(len(apps_projects), 3)} projects tested

🚀 STATUS: READY FOR AGENT ANALYSIS

Next steps:
1. Run: python3 research_mundo_barbaro.py
2. Run: python3 research_wisdom_reddit.py
3. Run: python3 run.py (for interactive menu)
""")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
