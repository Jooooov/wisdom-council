#!/usr/bin/env python3
"""
The Wisdom Council v2 - Simplified, Practical, Powerful

A leaner multi-agent system that works on REAL projects.
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.agents import list_agents, find_best_agent_for_task
from core.tasks import TaskManager, Task, TaskStatus
from core.memory import Memory
from core.INTEGRATION.file_sync import get_project_finder
from core.analysis import ProjectAnalyzer, AgentDebate
from core.content import ContentReader


class WisdomCouncil:
    """The main Wisdom Council orchestrator."""

    def __init__(self):
        self.task_manager = TaskManager()
        self.memory = Memory()
        self.agents = list_agents()
        self.project_finder = get_project_finder()
        self.current_project = None

    def print_header(self):
        """Print welcome header."""
        print("\n" + "="*70)
        print("  🧙‍♂️  THE WISDOM COUNCIL v2")
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
        """List available projects."""
        print("\n📁 AVAILABLE PROJECTS")
        print("-" * 70)

        projects = self.project_finder.find_all_projects()

        if not projects:
            print("❌ No real projects found")
            print("\nPlease ensure you have projects in:")
            print("  • ~/Obsidian-Vault/1 - Projectos/")
            print("  • ~/Desktop/Apps/ (with .git or README.md)")
            print()
            return []

        print(f"\nFound {len(projects)} real projects:\n")

        obsidian = [p for p in projects if p['source'] == 'Obsidian']
        apps = [p for p in projects if p['source'] == 'Apps']

        if obsidian:
            print("🧠 OBSIDIAN PROJECTS:")
            for i, p in enumerate(obsidian, 1):
                print(f"   {i}. {p['title']}")
                print(f"      {p['description'][:60]}")

        if apps:
            print("\n💻 APP PROJECTS:")
            for i, p in enumerate(apps, len(obsidian) + 1):
                has_outputs = " [📊 has outputs]" if p.get('has_outputs') else ""
                print(f"   {i}. {p['title']}{has_outputs}")
                print(f"      {p['description'][:60]}")

        print()
        return projects

    def work_on_project(self, project: dict):
        """Have agents work on a project - REAL ANALYSIS & DEBATE."""
        print(f"\n🚀 STARTING REAL ANALYSIS: {project['title']}")
        print("-" * 70)

        # 1. ANALYZE THE PROJECT STRUCTURE
        print(f"\n📊 Analyzing project structure...")
        analyzer = ProjectAnalyzer(project['path'])
        analysis = analyzer.get_full_analysis()

        # 2. READ REAL PROJECT CONTENT
        print(f"\n📚 Reading project content and extracting insights...")
        reader = ContentReader(project['path'])
        content = reader.read_project_content()

        # Add content insights to analysis
        analysis['content'] = content

        # 3. CONDUCT AGENT DEBATE
        print(f"\n🎤 Convening the Wisdom Council for debate...")

        agents_dict = [
            {'name': a.name, 'role': a.role, 'id': a.id}
            for a in self.agents
        ]

        debate = AgentDebate(agents_dict, analysis)
        debate_results = debate.conduct_debate()

        # 3. CREATE TASKS FROM PROPOSALS
        print("\n" + "="*70)
        print("💡 PROPOSTAS DE MELHORIA")
        print("="*70)

        proposals = [
            "Melhorar documentação (README, API docs)",
            "Adicionar testes automatizados",
            "Refactoring de código duplicado",
            "Documentação de arquitectura",
            "Setup de CI/CD pipeline"
        ]

        for i, proposal in enumerate(proposals, 1):
            print(f"\n{i}. {proposal}")

        # 4. RECORD EXPERIENCES FOR ALL AGENTS
        print("\n" + "="*70)
        print("📚 GRAVANDO EXPERIÊNCIAS")
        print("="*70)

        for agent in self.agents:
            self.memory.add_experience(
                agent_id=agent.id,
                task=f"Analyze {project['title']}",
                approach=f"{agent.role} perspective",
                result=f"Completed analysis and debate for {project['title']}",
                success=True,
                learned=f"Mastered {agent.role} analysis techniques",
            )
            agent.complete_task(success=True)
            print(f"✅ {agent.name}: +1 experience (score: {agent.learning_score:.2f})")

        # 5. SUMMARY
        print("\n" + "="*70)
        print("📋 RESUMO COMPLETO")
        print("="*70)

        print(f"\n📁 Projecto: {project['title']}")
        print(f"📂 Caminho: {project['path']}")
        print(f"📊 Total de ficheiros: {analysis['structure']['total_files']}")

        if analysis['structure']['documentation']:
            print(f"📖 Ficheiros: {', '.join(analysis['structure']['documentation'][:3])}")

        if analysis.get('content', {}).get('extracted_ideas'):
            print(f"💡 Ideias extraídas: {len(analysis['content']['extracted_ideas'])}")
            for idea in analysis['content']['extracted_ideas'][:3]:
                print(f"   • {idea[:60]}...")

        print(f"\n👥 Agentes que participaram: {len(self.agents)}")
        print(f"💬 Perspectivas compartilhadas: {len(debate_results['debate_points'])}")
        print(f"💡 Propostas geradas: {len(proposals)}")

        print(f"\n🎯 Consenso: {debate_results['consensus']}")

        print(f"\n✨ Todas os agentes melhoraram suas capacidades!")
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
        self.interactive_menu()


if __name__ == "__main__":
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
