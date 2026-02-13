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
        """Have agents work on a project."""
        print(f"\n🚀 STARTING WORK ON: {project['title']}")
        print("-" * 70)

        # Create initial analysis task
        task = self.task_manager.create_task(
            title=f"Analyze {project['title']}",
            description=f"Initial analysis of project: {project['description']}",
            priority=5,
        )

        # Find best agent for this project
        best_agent = find_best_agent_for_task(project['title'])
        self.task_manager.assign_task(task.id, best_agent.id)

        print(f"\n📋 Created task: {task.title}")
        print(f"👤 Assigned to: {best_agent.name} ({best_agent.role})")
        print(f"🎯 Priority: {task.priority}/5")

        # Simulate some work
        print(f"\n⚙️  Work in progress...")

        # Mark as started
        task.start()

        # Simulate completion
        result = f"Analysis of '{project['title']}' completed. Key insights:\n"
        result += f"  • Source: {project['source']}\n"
        result += f"  • Path: {project['path']}\n"

        if project.get('has_outputs'):
            result += f"  • Resources found: {len(project.get('resources', []))} files\n"

        task.complete(result)

        # Record experience
        self.memory.add_experience(
            agent_id=best_agent.id,
            task=task.title,
            approach="systematic analysis",
            result=result[:100],
            success=True,
            learned=f"Improved at analyzing {project['source']} projects",
        )

        # Update agent learning
        best_agent.complete_task(success=True)

        print(f"\n✅ COMPLETED!")
        print(f"\n📝 Result:\n{result}")

        # Show what other agents could do
        print(f"\n💡 Next possible tasks:")
        other_roles = ["Architect", "Developer", "Researcher", "Writer", "Tester"]
        for i, role in enumerate(other_roles[:3], 1):
            print(f"   {i}. Have {role} work on this project")

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
