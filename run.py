#!/usr/bin/env python3
"""
The Wisdom Council v2 - Simplified, Practical, Powerful

A leaner multi-agent system that works on REAL projects.
With Qwen3-4B-4bit and RAM guardrails.
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

# CRITICAL: Check RAM before anything else
def check_ram_before_startup():
    """Verify RAM is sufficient before starting."""
    try:
        from core.llm import create_ram_manager, create_mlx_loader

        ram = create_ram_manager()
        loader = create_mlx_loader(ram)

        can_load, message = loader.check_ram_availability()

        print("\n" + "="*70)
        print("🛡️  RAM GUARDIAN - Pre-Startup Check")
        print("="*70)
        print(message)

        if not can_load:
            print("\n" + "!"*70)
            print("❌ CANNOT START - INSUFFICIENT RAM")
            print("!"*70)
            print("\nPlease:")
            print("  1. Close ALL browser tabs")
            print("  2. Close Slack, Discord, email clients")
            print("  3. Close IDEs and editors")
            print("  4. Restart your MacBook")
            print("  5. Try again")
            sys.exit(1)
        else:
            print("\n✅ RAM check passed - safe to proceed\n")
            return True
    except Exception as e:
        print(f"\n⚠️  Could not verify RAM: {e}")
        print("Attempting to continue anyway...")
        return False


from core.agents import list_agents, find_best_agent_for_task
from core.tasks import TaskManager, Task, TaskStatus
from core.memory import Memory
from core.INTEGRATION.file_sync import get_project_finder
from core.content import ContentReader
from core.research.mary_context import get_mary_context, get_mary_research_system_prompt
from core.research.mary_research_manager import get_mary_research_manager
from core.obsidian import sync_mary_to_obsidian
import asyncio
import httpx
from pathlib import Path


class WisdomCouncil:
    """The main Wisdom Council orchestrator."""

    def __init__(self):
        self.task_manager = TaskManager()
        self.memory = Memory()
        self.agents = list_agents()
        self.project_finder = get_project_finder()
        self.current_project = None
        self.llm_loaded = False

        # Mary Malone's systems
        self.mary_context = get_mary_context()
        self.mary_manager = get_mary_research_manager()
        self.agents_md_path = Path(__file__).parent / "agents.md"

    def print_header(self):
        """Print welcome header."""
        print("\n" + "="*70)
        print("  🧙‍♂️  THE WISDOM COUNCIL v2")
        print("  Qwen3-4B-4bit with RAM Protection")
        print("  Simplified. Practical. Powerful.")
        print("="*70 + "\n")

    def show_status(self):
        """Show system status."""
        print("\n📊 SYSTEM STATUS")
        print("-" * 70)
        print(f"Agents: {len(self.agents)} operational")
        for agent in self.agents:
            status = "🟢" if agent.is_active else "🔴"
            print(f"  {status} {agent.name:12s} ({agent.role:12s}) - Score: {agent.learning_score:.2f}")

        stats = self.memory.get_stats()
        print(f"\nMemory: {stats['total_experiences']} experiences recorded")
        print(f"Agents learned from: {stats.get('agents', 0)} agents")

        print()

    def list_projects(self):
        """List available projects - merged and enriched."""
        print("\n📁 AVAILABLE PROJECTS")
        print("-" * 70)

        projects = self.project_finder.find_all_projects(merge_duplicates=True)

        if not projects:
            print("❌ No real projects found")
            print("\nPlease ensure you have projects in:")
            print("  • ~/Obsidian-Vault/1 - Projectos/")
            print("  • ~/Desktop/Apps/ (with .git or README.md)")
            print()
            return []

        print(f"\nFound {len(projects)} real projects:\n")

        merged = [p for p in projects if p['source'] == 'MERGED']
        obsidian = [p for p in projects if p['source'] == 'Obsidian']
        apps = [p for p in projects if p['source'] == 'Apps']

        counter = 1

        # Mostrar projectos merged primeiro (enriquecidos)
        if merged:
            print("🎯 MERGED PROJECTS (Obsidian + App Code - Enriched):")
            for p in merged:
                has_outputs = " [📊 has outputs]" if p.get('has_outputs') else ""
                print(f"   {counter}. {p['title']}{has_outputs}")
                print(f"      📚 {p['obsidian_project']['description'][:45]}")
                print(f"      💻 {p['apps_project']['description'][:45]}")
                print(f"      ✨ ENRICHED - Contexto Obsidian + Código Apps")
                counter += 1

        # Mostrar projectos só de Obsidian
        if obsidian:
            print("\n📖 OBSIDIAN PROJECTS (Context Only):")
            for p in obsidian:
                print(f"   {counter}. {p['title']}")
                print(f"      {p['description'][:60]}")
                counter += 1

        # Mostrar projectos só de Apps
        if apps:
            print("\n💻 APP PROJECTS (Code Only):")
            for p in apps:
                has_outputs = " [📊 has outputs]" if p.get('has_outputs') else ""
                print(f"   {counter}. {p['title']}{has_outputs}")
                print(f"      {p['description'][:60]}")
                counter += 1

        print()
        return projects

    def work_on_project(self, project: dict):
        """Have agents work on a project - BUSINESS ANALYSIS or CODE ANALYSIS."""
        print(f"\n🚀 STARTING ANALYSIS: {project['title']}")
        print("-" * 70)
        print(f"⏳ Analyzing project structure and context...\n")

        # Determine if this is a business project
        asyncio.run(self._analyze_project_intelligent(project))

    async def _analyze_project_intelligent(self, project: dict):
        """Intelligent analysis - detects if business project and runs appropriate analysis."""
        from pathlib import Path
        from core.analysis.business_analyzer import analyze_business
        from core.orchestration.war_room import run_war_room
        from core.research.web_researcher import research_project
        from core.agents.devops_agent import DevOpsAgent
        from core.memory.rag_memory import create_rag_memory

        project_path = Path(project['path'])
        rag_memory = create_rag_memory()

        print("\n" + "=" * 70)
        print("🔍 COMPREHENSIVE PROJECT ANALYSIS")
        print("=" * 70)

        # Step 1: DevOps Analysis
        print("\n📊 Step 1/4: DevOps & Git Workflow Analysis")
        print("-" * 70)
        devops = DevOpsAgent(str(project_path))
        devops_status = devops.analyze_workflow()

        # Step 2: Web Research
        print("\n🌐 Step 2/4: Web Research - Finding Similar Projects & Tools")
        print("-" * 70)
        research_findings = await research_project(project['title'], project.get('type', 'software'))

        # Step 3: Business/Code Analysis
        print("\n📊 Step 3/4: Context & Business Analysis")
        print("-" * 70)
        business_case = await analyze_business(str(project_path), project['title'])

        # Add paths information for merged projects (for manual inputs search)
        if project.get('paths'):
            business_case['paths'] = project['paths']

        if business_case.get('status') == 'READY' and business_case.get('ready_for_agent_discussion'):
            # It's a business project - use War Room with LLM
            print("\n⚔️  Step 4/4: War Room Discussion with LLM Reasoning")
            print("-" * 70)
            print("🎯 Business project detected - Starting War Room discussion...")
            print("   Agents are thinking deeply about the business viability with reasoning.\n")

            result = await run_war_room(business_case, self.agents, str(project_path))

            # Step 5: Save comprehensive results
            if result.get('status') == 'COMPLETE':
                self._save_comprehensive_analysis(project, {
                    "devops": devops_status,
                    "research": research_findings,
                    "business": business_case,
                    "war_room": result
                })

                # Store in memory for future learning
                for agent in self.agents:
                    rag_memory.store_analysis(
                        agent.name,
                        project['title'],
                        {
                            "business_case": business_case,
                            "recommendation": result.get('recommendation', {}).get('decision'),
                            "project_type": business_case.get('project_type')
                        }
                    )
        else:
            # Not a business project - do code analysis
            print("\n💻 Step 4/4: Technical Analysis")
            print("-" * 70)
            await self._analyze_project_code(project)

            # Store code analysis in memory
            for agent in self.agents:
                rag_memory.store_analysis(
                    agent.name,
                    project['title'],
                    {"project_type": "code_focused"}
                )

    async def _analyze_project_code(self, project: dict):
        """Real analysis of project code."""
        from pathlib import Path

        project_path = Path(project['path'])
        findings = {
            "critical_issues": [],
            "performance_issues": [],
            "quick_wins": []
        }

        # 1. ANALYZE PYTHON FILES
        print(f"📊 Analyzing Python files...")
        py_files = list(project_path.glob("**/*.py"))[:10]
        py_files = [f for f in py_files if ".venv" not in str(f) and "__pycache__" not in str(f)]

        for py_file in py_files:
            try:
                with open(py_file) as f:
                    code = f.read()

                # Simple real analysis (not fake)
                issues = []
                if "TODO" in code or "FIXME" in code:
                    issues.append("Has unresolved TODOs/FIXMEs")
                if "hardcoded" in code.lower() or code.count("'") > 50:
                    issues.append("Possible hardcoded configuration")
                if "import sys" in code and "os.system" in code:
                    issues.append("Uses system calls (potential security concern)")
                if code.count("try:") > 10 and code.count("except:") > 5:
                    issues.append("Broad exception handling detected")

                if issues:
                    findings["critical_issues"].append({
                        "file": py_file.name,
                        "issues": issues,
                        "lines": len(code.split('\n'))
                    })
            except Exception as e:
                pass

        # 2. SEARCH WEB CONTEXT
        print(f"🔎 Searching for best practices context...")
        context = await self._search_context(project['title'])

        # 3. DISPLAY REAL FINDINGS
        print("\n" + "="*70)
        print("🔴 REAL FINDINGS")
        print("="*70)

        if findings["critical_issues"]:
            print(f"\n📁 Files with issues ({len(findings['critical_issues'])} found):")
            for item in findings["critical_issues"][:5]:
                print(f"\n  📄 {item['file']} ({item['lines']} lines)")
                for issue in item['issues']:
                    print(f"     • {issue}")
        else:
            print("\n✅ No obvious critical issues found")

        # 4. ACTIONABLE RECOMMENDATIONS
        print("\n" + "="*70)
        print("💡 ACTIONABLE IMPROVEMENTS")
        print("="*70)

        recommendations = [
            "1. [HIGH] Code Review: Check identified hardcoded values",
            "2. [MEDIUM] Testing: Add unit tests for core functions",
            "3. [MEDIUM] Documentation: Add docstrings to public APIs",
            "4. [LOW] Performance: Profile slow operations",
            "5. [LOW] Cleanup: Resolve all TODO/FIXME comments"
        ]

        for rec in recommendations:
            print(f"\n{rec}")

        # 5. RECORD REAL EXPERIENCE
        print("\n" + "="*70)
        print("📚 LEARNING RECORDED")
        print("="*70)

        for agent in self.agents:
            self.memory.add_experience(
                agent_id=agent.id,
                task=f"Code analysis of {project['title']}",
                approach=f"{agent.role} analyzed {len(py_files)} files with {len(findings['critical_issues'])} findings",
                result=f"Identified specific issues and recommendations",
                success=True,
                learned=f"Pattern recognition in {project['title']} codebase",
            )
            agent.complete_task(success=True)
            print(f"✅ {agent.name}: +1 experience (score: {agent.learning_score:.2f})")

        print(f"\n✨ Code analysis complete!")
        print()

    def _save_comprehensive_analysis(self, project: dict, analysis_data: dict):
        """Save comprehensive analysis results to multiple files."""
        from pathlib import Path

        project_path = Path(project['path'])
        results_dir = project_path / ".wisdom_council_analysis"
        results_dir.mkdir(exist_ok=True)

        # 1. DevOps Analysis
        devops_file = results_dir / "01_DEVOPS_ANALYSIS.md"
        try:
            devops_content = f"""# DevOps & Workflow Analysis

**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## Git Workflow Status

- Current Branch: {analysis_data['devops'].get('current_branch', 'Unknown')}
- Branches: {', '.join(analysis_data['devops'].get('branches', []))}
- Uncommitted Changes: {'Yes' if analysis_data['devops'].get('uncommitted_changes') else 'No'}

## Code Quality

{self._format_code_quality(analysis_data['devops'].get('code_quality', {}))}

## Recommendations

{self._format_recommendations(analysis_data['devops'].get('code_quality', {}))}
"""
            devops_file.write_text(devops_content)
        except Exception as e:
            print(f"⚠️  Could not save DevOps analysis: {e}")

        # 2. Research Findings
        research_file = results_dir / "02_RESEARCH_FINDINGS.md"
        try:
            research = analysis_data.get('research', {})
            research_content = f"""# Web Research Findings

## Similar Projects

{self._format_research_findings(research.get('similar_projects', []))}

## Useful Tools

{self._format_tools(research.get('useful_tools', []))}

## GitHub Repositories

{self._format_github_repos(research.get('github_repositories', []))}

## Best Practices

{self._format_practices(research.get('best_practices', []))}
"""
            research_file.write_text(research_content)
        except Exception as e:
            print(f"⚠️  Could not save research findings: {e}")

        # 3. Business Analysis
        business_file = results_dir / "03_BUSINESS_ANALYSIS.md"
        try:
            business = analysis_data.get('business', {})
            business_content = f"""# Business Analysis

**Project:** {project['title']}

## Market Research

- Competitors Found: {len(business.get('competitive_analysis', {}).get('competitors', []))}
- Market Gaps: {len(business.get('market_research', {}).get('gaps', []))}

## Competitive Position

- Viability Score: {business.get('viability_score', 0)}/100

## Key Findings

Advantages: {', '.join(business.get('competitive_analysis', {}).get('competitive_advantages', [])[:3])}

Threats: {', '.join(business.get('competitive_analysis', {}).get('threats', [])[:3])}
"""
            business_file.write_text(business_content)
        except Exception as e:
            print(f"⚠️  Could not save business analysis: {e}")

        # 4. War Room Results
        war_room_file = results_dir / "04_WAR_ROOM_DISCUSSION.md"
        try:
            war_room = analysis_data.get('war_room', {})
            war_room_content = f"""# War Room Discussion Results

**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## Executive Decision

**Recommendation:** {war_room.get('recommendation', {}).get('decision', 'UNDETERMINED')}

## Agent Perspectives

"""
            for agent_name, perspective in war_room.get('perspectives', {}).items():
                war_room_content += f"### {agent_name}\n"
                war_room_content += f"**Recommendation:** {perspective.get('recommendation', 'UNCLEAR')}\n\n"
                war_room_content += f"**Analysis:**\n{perspective.get('reasoning', 'N/A')}\n\n"

            war_room_content += f"""## Consensus

{war_room.get('consensus', {}).get('summary', 'N/A')}

## Final Reasoning

{war_room.get('recommendation', {}).get('reasoning', 'N/A')}

---

**Status:** {war_room.get('status', 'UNKNOWN')}
"""
            war_room_file.write_text(war_room_content)
        except Exception as e:
            print(f"⚠️  Could not save war room results: {e}")

        print(f"\n✅ Comprehensive analysis saved to: {results_dir}")

    # ===== Helper Methods =====

    def _format_code_quality(self, quality: dict) -> str:
        """Format code quality metrics."""
        return f"""
- Tests: {'✅' if quality.get('has_tests') else '❌'}
- Documentation: {'✅' if quality.get('has_docs') else '❌'}
- README: {'✅' if quality.get('has_readme') else '❌'}
- .gitignore: {'✅' if quality.get('has_gitignore') else '❌'}
- Requirements: {'✅' if quality.get('has_requirements') else '❌'}
"""

    def _format_recommendations(self, quality: dict) -> str:
        """Format DevOps recommendations."""
        recommendations = []
        if not quality.get('has_tests'):
            recommendations.append("Add unit tests in tests/ directory")
        if not quality.get('has_docs'):
            recommendations.append("Create docs/ directory with documentation")
        if not quality.get('has_readme'):
            recommendations.append("Add comprehensive README.md")
        if not quality.get('has_gitignore'):
            recommendations.append("Add .gitignore file")
        if not quality.get('has_requirements'):
            recommendations.append("Add requirements.txt or setup.py")

        return "\n".join([f"- {r}" for r in recommendations]) if recommendations else "No major recommendations"

    def _format_research_findings(self, projects: list) -> str:
        """Format research findings."""
        if not projects:
            return "No similar projects found"
        return "\n".join([f"- [{p['title']}]({p['url']}): {p['snippet']}" for p in projects[:5]])

    def _format_tools(self, tools: list) -> str:
        """Format tools list."""
        if not tools:
            return "No tools found"
        return "\n".join([f"- **{t['name']}**: {t['description']}" for t in tools[:5]])

    def _format_github_repos(self, repos: list) -> str:
        """Format GitHub repos."""
        if not repos:
            return "No repositories found"
        return "\n".join([f"- [{r['name']}]({r['url']}) ({r['language']}): {r['stars']} stars" for r in repos[:5]])

    def _format_practices(self, practices: list) -> str:
        """Format best practices."""
        if not practices:
            return "No practices found"
        return "\n".join([f"- [{p['topic']}]({p['url']}): {p['details']}" for p in practices[:5]])

    def _save_analysis_results(self, project: dict, war_room_result: dict):
        """Save War Room analysis results to file (legacy method)."""
        self._save_comprehensive_analysis(project, {"war_room": war_room_result})

    async def _search_context(self, project_name: str):
        """Search for context using Perplexity MCP."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    "http://localhost:3007/search",
                    json={"query": f"Best practices for {project_name} development"},
                )
                result = response.json()
                return result if "error" not in result else None
        except:
            return None

    # ===== Mary Malone's Research Methods =====

    def mary_research(self, query: str, category: str = None):
        """Mary conducts tool research."""
        print("\n" + "=" * 70)
        print("🔬 MARY MALONE - TOOL RESEARCH SESSION")
        print("=" * 70)
        print(f"\n📊 Mary's Research Context:")
        print(f"   📅 Date: {self.mary_context.month_year}")
        print(f"   🔍 Query: {query}")
        if category:
            print(f"   📁 Category: {category}")

        # Start research session
        session = self.mary_manager.start_research_session(query, "Mary")

        print(f"\n{self.mary_context.get_search_guidelines()}")
        print("\n" + "-" * 70)
        print("✨ Mary's research session started.")
        print("   When you find tools, Mary will document them.")
        print(f"   Session ID: {session['id']}")
        print("-" * 70 + "\n")

        return session

    def mary_show_context(self):
        """Show Mary's research context."""
        print("\n" + "=" * 70)
        print("🔬 MARY MALONE'S CURRENT RESEARCH CONTEXT")
        print("=" * 70)
        print(f"\n📅 Current Date: {self.mary_context.month_year}")
        print(f"   ISO: {self.mary_context.short_date}")

        print(f"\n📊 Technology Versions Mary Tracks:")
        for tech, version in self.mary_context.tech_versions.items():
            print(f"   • {tech}: {version}")

        print(f"\n🎯 Mary's Search Guidelines:")
        print(self.mary_context.get_search_guidelines())

        print(f"\n📚 Tools Discovered: {len(self.mary_manager.tools_db)}")
        if self.mary_manager.tools_db:
            for tool in self.mary_manager.tools_db[:5]:
                print(f"   • {tool['name']} ({tool['category']})")

        print()

    def mary_update_agents_md(self):
        """Mary updates the agents.md file."""
        print("\n" + "=" * 70)
        print("📝 MARY UPDATING agents.md")
        print("=" * 70)

        agents_md_content = self.mary_manager.create_agents_md(self.agents)

        try:
            self.agents_md_path.write_text(agents_md_content)
            print(f"\n✅ agents.md updated successfully!")
            print(f"   📁 Location: {self.agents_md_path}")
            print(f"   📊 Agents documented: {len(self.agents)}")
            print(f"   🔧 Tools tracked: {len(self.mary_manager.tools_db)}")
            print("\n📌 Key Updates:")
            print("   • Current date & time context")
            print("   • Technology version baselines")
            print("   • Mary's search guidelines")
            print("   • All discovered tools")
        except Exception as e:
            print(f"\n❌ Error updating agents.md: {e}")

        print()

    def mary_sync_obsidian(self):
        """Mary syncs tool database to Obsidian vault."""
        print("\n" + "=" * 70)
        print("🔗 MARY SYNCING TO OBSIDIAN VAULT")
        print("=" * 70)

        try:
            obsidian = sync_mary_to_obsidian(self.mary_manager)
            print(f"\n✅ Obsidian sync complete!")
            print(f"   📁 Vault: source mindpalace")
            print(f"   📂 Tools folder: 0 - tools")
            print(f"   📊 Files created:")
            print(f"      • _Index.md (main tools index)")
            print(f"      • by_category/ folder (tools by category)")
            print(f"      • by_agent/ folder (tools by agent)")
            print(f"      • Emerging Tools Tracker.md")
            print(f"\n🔗 Links created:")
            print(f"   • [[Category]] links for browsing")
            print(f"   • [[Agent's Tools]] links for each agent")
            print(f"   • Backlinks between tools and agents")
            print(f"\n📚 Tools synced: {len(self.mary_manager.tools_db)}")
        except Exception as e:
            print(f"\n❌ Error syncing Obsidian: {e}")
            import traceback
            traceback.print_exc()

        print()

    def mary_add_tool(self, name: str, category: str, summary: str,
                     relevant_agents: list, source: str = ""):
        """Mary documents a discovered tool."""
        tool = self.mary_manager.add_tool_discovery(
            name, category, summary, relevant_agents, source
        )
        print(f"\n✅ Mary documented: {name}")
        print(f"   📁 Category: {category}")
        print(f"   👥 For agents: {', '.join(relevant_agents)}")
        print(f"   📍 Source: {source if source else 'Unknown'}")
        return tool

    def mary_show_tools(self):
        """Show all tools Mary has discovered."""
        print("\n" + "=" * 70)
        print("🔧 MARY'S TOOL DATABASE")
        print("=" * 70)

        if not self.mary_manager.tools_db:
            print("\n No tools discovered yet.")
            print(" Mary is actively researching...\n")
            return

        print(f"\n📊 Total Tools: {len(self.mary_manager.tools_db)}\n")

        # Group by category
        by_category = {}
        for tool in self.mary_manager.tools_db:
            cat = tool['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tool)

        for category, tools in sorted(by_category.items()):
            print(f"\n📁 {category.upper()} ({len(tools)})")
            print("   " + "-" * 65)
            for tool in tools:
                agents = ", ".join(tool['relevant_agents'])
                print(f"   • {tool['name']}")
                print(f"     📝 {tool['summary']}")
                print(f"     👥 For: {agents}")
                if tool.get('source_url'):
                    print(f"     🔗 {tool['source_url']}")
                print()

        print()

    def interactive_menu(self):
        """Run interactive menu."""
        while True:
            print("\n" + "-" * 70)
            print("WHAT WOULD YOU LIKE TO DO?")
            print("-" * 70)
            print("\n1️⃣  Show system status")
            print("2️⃣  List available projects")
            print("3️⃣  Have agents work on a project")
            print("4️⃣  View agent learning history")
            print("5️⃣  View memory & experiences")
            print("0️⃣  Exit")
            print()

            choice = input("Choose (0-5): ").strip()

            if choice == "1":
                self.show_status()

            elif choice == "2":
                self.list_projects()

            elif choice == "3":
                projects = self.list_projects()
                if projects:
                    try:
                        num = int(input("\nWhich project? (number): ")) - 1
                        if 0 <= num < len(projects):
                            self.work_on_project(projects[num])
                        else:
                            print("❌ Invalid choice")
                    except ValueError:
                        print("❌ Invalid input")

            elif choice == "4":
                print("\n📚 AGENT LEARNING HISTORY")
                print("-" * 70)
                for agent in self.agents:
                    exps = self.memory.get_agent_experiences(agent.id)
                    learned = self.memory.get_agent_learning(agent.id)
                    print(f"\n{agent.name} ({agent.role}):")
                    print(f"  Tasks completed: {len(exps)}")
                    print(f"  Success rate: {self.memory.get_agent_success_rate(agent.id):.0%}")
                    if learned:
                        print(f"  Learned: {', '.join(learned[:3])}")
                print()

            elif choice == "5":
                stats = self.memory.get_stats()
                print("\n💾 MEMORY & EXPERIENCES")
                print("-" * 70)
                print(f"Total experiences: {stats['total_experiences']}")
                print(f"Active agents: {stats['agents']}")
                print(f"Overall success rate: {stats.get('overall_success_rate', 0):.0%}")

                if stats.get('agents_stats'):
                    print("\nAgent breakdown:")
                    for agent_id, astats in stats['agents_stats'].items():
                        agent = next((a for a in self.agents if a.id == agent_id), None)
                        if agent:
                            print(f"  {agent.name}: {astats['experiences']} tasks, "
                                  f"{astats['success_rate']:.0%} success")
                print()

            elif choice == "0":
                print("\n👋 The Wisdom Council closes. Farewell!\n")
                break

            else:
                print("❌ Invalid choice")

    def run(self):
        """Run the Wisdom Council."""
        self.print_header()
        self.show_status()

        # Use new CLI Menu instead of old interactive menu
        from core.ui import CLIMenu
        menu = CLIMenu(self)
        menu.run()


if __name__ == "__main__":
    # CRITICAL: Check RAM before starting
    if not check_ram_before_startup():
        print("⚠️  Proceeding with caution (RAM check failed)")

    try:
        council = WisdomCouncil()
        council.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
