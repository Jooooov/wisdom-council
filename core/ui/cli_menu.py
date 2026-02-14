"""
Professional CLI Menu System - Terminal UI for Wisdom Council

Provides interactive menus with:
- War Room access
- Agent collaboration
- Project management
- Memory browser
- DevOps controls
"""

import sys
from typing import Callable, List, Dict, Any
from pathlib import Path


class CLIMenu:
    """Professional terminal menu system."""

    def __init__(self, council):
        """Initialize CLI menu with council reference."""
        self.council = council
        self.current_menu = "main"
        self.running = True

    def run(self):
        """Start interactive menu."""
        self._print_welcome()

        while self.running:
            self._show_main_menu()

    def _print_welcome(self):
        """Print welcome banner."""
        print("\n" + "=" * 80)
        print("  " + "🧙‍♂️  THE WISDOM COUNCIL - Agent Collaboration & Business Analysis".center(76))
        print("  " + "DeepSeek-R1-8B Powered | Portuguese + Reasoning".center(76))
        print("=" * 80)
        print()

    def _show_main_menu(self):
        """Show main menu."""
        print("\n" + "-" * 80)
        print("MAIN MENU".center(80))
        print("-" * 80)

        options = [
            ("📊 System Status", self._show_system_status),
            ("📁 Projects & Analysis", self._show_projects_menu),
            ("⚔️  War Room", self._show_war_room_menu),
            ("🧠 Memory & Learning", self._show_memory_menu),
            ("🚀 DevOps & Deployment", self._show_devops_menu),
            ("🧙 Agent Profiles", self._show_agent_profiles),
            ("📚 Knowledge Base", self._show_knowledge_menu),
            ("⚙️  Settings", self._show_settings),
            ("❌ Exit", self._exit_menu)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_projects_menu(self):
        """Show projects and analysis menu."""
        print("\n" + "-" * 80)
        print("PROJECTS & ANALYSIS".center(80))
        print("-" * 80)

        projects = self.council.list_projects()

        if not projects:
            print("\n❌ No projects found")
            input("\nPress ENTER to continue...")
            return

        print(f"\n📁 Found {len(projects)} projects:\n")

        options = []
        for i, project in enumerate(projects, 1):
            display_name = f"{i}. {project['title'][:50]}"
            options.append((display_name, lambda p=project: self._analyze_project(p)))

        options.append(("↩️  Back to main menu", lambda: None))

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_war_room_menu(self):
        """Show War Room menu."""
        print("\n" + "-" * 80)
        print("⚔️  WAR ROOM - Agent Collaboration Center".center(80))
        print("-" * 80)

        options = [
            ("🎯 Start New Discussion", self._start_war_room),
            ("📋 View Past Discussions", self._view_discussions),
            ("💬 Agent Perspectives", self._show_agent_perspectives),
            ("🤝 Consensus Builder", self._show_consensus),
            ("↩️  Back to main menu", lambda: None)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_memory_menu(self):
        """Show Memory and Learning menu."""
        print("\n" + "-" * 80)
        print("🧠 COLLECTIVE MEMORY & LEARNING".center(80))
        print("-" * 80)

        options = [
            ("📊 Memory Status", self._show_memory_status),
            ("🔍 Search Memories", self._search_memories),
            ("📈 Agent Learning Progress", self._show_agent_learning),
            ("🎓 Discovered Patterns", self._show_patterns),
            ("↩️  Back to main menu", lambda: None)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_devops_menu(self):
        """Show DevOps and Deployment menu."""
        print("\n" + "-" * 80)
        print("🚀 DEVOPS & DEPLOYMENT".center(80))
        print("-" * 80)

        options = [
            ("🔍 Analyze Workflow", self._analyze_devops),
            ("🌳 Branch Management", self._manage_branches),
            ("📦 Release Readiness", self._check_release_readiness),
            ("✅ Code Quality Report", self._show_code_quality),
            ("↩️  Back to main menu", lambda: None)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_agent_profiles(self):
        """Show detailed agent profiles."""
        print("\n" + "-" * 80)
        print("🧙 AGENT PROFILES & ROLES".center(80))
        print("-" * 80)

        agents = self.council.agents
        print(f"\n📖 The Wisdom Council has {len(agents)} members:\n")

        for i, agent in enumerate(agents, 1):
            daemon = getattr(agent, 'daemon', 'Unknown')
            print(f"{i}. {agent.name:15s} | Role: {agent.role:12s} | Daemon: {daemon}")
            print(f"   Learning Score: {getattr(agent, 'learning_score', 0):.2f}")
            print()

        input("Press ENTER to continue...")

    def _show_knowledge_menu(self):
        """Show knowledge base menu."""
        print("\n" + "-" * 80)
        print("📚 KNOWLEDGE BASE".center(80))
        print("-" * 80)

        options = [
            ("🔎 Research Findings", self._browse_research),
            ("📖 Project Analysis Reports", self._browse_analyses),
            ("🎯 Best Practices", self._show_best_practices),
            ("↩️  Back to main menu", lambda: None)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    def _show_settings(self):
        """Show settings menu."""
        print("\n" + "-" * 80)
        print("⚙️  SETTINGS".center(80))
        print("-" * 80)

        options = [
            ("🔧 LLM Configuration", self._configure_llm),
            ("💾 Memory Settings", self._configure_memory),
            ("🌐 Research Settings", self._configure_research),
            ("🎨 Display Preferences", self._configure_display),
            ("↩️  Back to main menu", lambda: None)
        ]

        self._print_options(options)
        self._handle_menu_choice(options)

    # ===== Menu Actions =====

    def _analyze_project(self, project: Dict[str, Any]):
        """Analyze selected project."""
        print(f"\n🚀 Analyzing: {project['title']}")
        print("-" * 80)
        self.council.work_on_project(project)
        input("\nPress ENTER to continue...")

    def _start_war_room(self):
        """Start war room discussion."""
        print("\n⚔️  STARTING WAR ROOM")
        print("-" * 80)
        print("Select a project to analyze:")
        projects = self.council.list_projects()
        if projects:
            for i, p in enumerate(projects, 1):
                print(f"{i}. {p['title']}")
            try:
                choice = int(input("\nSelect project (number): ")) - 1
                if 0 <= choice < len(projects):
                    self.council.work_on_project(projects[choice])
            except ValueError:
                print("❌ Invalid choice")
        input("\nPress ENTER to continue...")

    def _show_agent_perspectives(self):
        """Show individual agent perspectives."""
        print("\n💬 AGENT PERSPECTIVES")
        print("-" * 80)
        print("Each agent provides unique insights based on their role:\n")

        for agent in self.council.agents:
            daemon = getattr(agent, 'daemon', 'Unknown')
            print(f"🧙 {agent.name} ({agent.role})")
            print(f"   Daemon: {daemon}")
            print(f"   Specialty: Analyzes from {agent.role.lower()} perspective")
            print()

        input("Press ENTER to continue...")

    def _show_memory_status(self):
        """Show memory system status."""
        from core.memory.rag_memory import create_rag_memory
        memory = create_rag_memory()
        memory.print_memory_status()
        input("\nPress ENTER to continue...")

    def _search_memories(self):
        """Search in collective memory."""
        from core.memory.rag_memory import create_rag_memory
        memory = create_rag_memory()

        query = input("\n🔍 Search memories for: ").strip()
        results = memory.retrieve_relevant_memories(query, limit=10)

        if results:
            print(f"\n📖 Found {len(results)} relevant memories:\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.get('project')} analyzed by {result.get('agent')}")
                print(f"   Time: {result.get('timestamp', 'Unknown')}\n")
        else:
            print("\n❌ No memories found")

        input("\nPress ENTER to continue...")

    def _show_agent_learning(self):
        """Show agent learning progress."""
        from core.memory.rag_memory import create_rag_memory
        memory = create_rag_memory()

        print("\n📈 AGENT LEARNING PROGRESS\n")

        for agent in self.council.agents:
            insights = memory.get_agent_insights(agent.name)
            print(f"🧙 {agent.name}")
            print(f"   Learning Trajectory: {insights['learning_trajectory']}")
            print(f"   Recent Analyses: {insights['recent_analyses']}")
            if insights['common_recommendations']:
                print(f"   Common Recommendations: {', '.join(insights['common_recommendations'][:2])}")
            print()

        input("Press ENTER to continue...")

    def _analyze_devops(self):
        """Analyze DevOps workflow."""
        from core.agents.devops_agent import DevOpsAgent

        projects = self.council.list_projects()
        if not projects:
            print("\n❌ No projects found")
            return

        print("\nSelect project to analyze workflow:")
        for i, p in enumerate(projects, 1):
            print(f"{i}. {p['title']}")

        try:
            choice = int(input("\nSelect project (number): ")) - 1
            if 0 <= choice < len(projects):
                project_path = projects[choice]['path']
                devops = DevOpsAgent(project_path)
                devops.analyze_workflow()
        except ValueError:
            print("❌ Invalid choice")

        input("\nPress ENTER to continue...")

    def _check_release_readiness(self):
        """Check if project is ready for release."""
        from core.agents.devops_agent import DevOpsAgent

        projects = self.council.list_projects()
        if not projects:
            print("\n❌ No projects found")
            return

        print("\nSelect project to check release readiness:")
        for i, p in enumerate(projects, 1):
            print(f"{i}. {p['title']}")

        try:
            choice = int(input("\nSelect project (number): ")) - 1
            if 0 <= choice < len(projects):
                project_path = projects[choice]['path']
                devops = DevOpsAgent(project_path)
                devops.suggest_release_readiness()
        except ValueError:
            print("❌ Invalid choice")

        input("\nPress ENTER to continue...")

    def _exit_menu(self):
        """Exit the menu."""
        print("\n👋 Goodbye!\n")
        self.running = False
        sys.exit(0)

    # ===== Stub Methods for Unimplemented Features =====

    def _show_system_status(self):
        """Show system status."""
        self.council.show_status()
        input("\nPress ENTER to continue...")

    def _view_discussions(self):
        print("\n📋 Past discussions will be listed here")
        input("\nPress ENTER to continue...")

    def _show_consensus(self):
        print("\n🤝 Consensus analysis will be shown here")
        input("\nPress ENTER to continue...")

    def _show_patterns(self):
        print("\n🎓 Discovered patterns will be shown here")
        input("\nPress ENTER to continue...")

    def _browse_research(self):
        print("\n🔎 Research findings will be browsable here")
        input("\nPress ENTER to continue...")

    def _browse_analyses(self):
        print("\n📖 Analysis reports will be browsable here")
        input("\nPress ENTER to continue...")

    def _show_best_practices(self):
        print("\n🎯 Best practices will be shown here")
        input("\nPress ENTER to continue...")

    def _configure_llm(self):
        print("\n🔧 LLM configuration options will be here")
        input("\nPress ENTER to continue...")

    def _configure_memory(self):
        print("\n💾 Memory settings will be configurable here")
        input("\nPress ENTER to continue...")

    def _configure_research(self):
        print("\n🌐 Research settings will be configurable here")
        input("\nPress ENTER to continue...")

    def _configure_display(self):
        print("\n🎨 Display preferences will be configurable here")
        input("\nPress ENTER to continue...")

    def _manage_branches(self):
        print("\n🌳 Branch management will be available here")
        input("\nPress ENTER to continue...")

    def _show_code_quality(self):
        print("\n✅ Code quality report will be shown here")
        input("\nPress ENTER to continue...")

    # ===== Helper Methods =====

    def _print_options(self, options: List[tuple]):
        """Print menu options."""
        print()
        for i, (label, _) in enumerate(options, 1):
            print(f"  {i}️⃣  {label}")
        print()

    def _handle_menu_choice(self, options: List[tuple]):
        """Handle menu choice input."""
        try:
            choice = int(input("Choose option (number): ").strip()) - 1
            if 0 <= choice < len(options):
                action = options[choice][1]
                if action:
                    action()
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
