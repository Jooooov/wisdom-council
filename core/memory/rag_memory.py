"""
RAG Memory System - Agents learn from past analyses

Stores and retrieves past experiences using semantic search.
Improves agent decision-making through pattern recognition.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import hashlib


class RAGMemory:
    """Retrieval-Augmented Generation memory for agent learning."""

    def __init__(self, storage_path: str = None):
        """Initialize RAG memory system."""
        if storage_path is None:
            storage_path = str(Path.home() / ".wisdom_council" / "memory")

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.memories_file = self.storage_path / "collective_memory.jsonl"
        self.patterns_file = self.storage_path / "learned_patterns.json"
        self.agent_profiles = self.storage_path / "agent_profiles.json"

        self.memories = self._load_memories()
        self.patterns = self._load_patterns()
        self.profiles = self._load_profiles()

    def _load_memories(self) -> List[Dict]:
        """Load memories from storage."""
        if not self.memories_file.exists():
            return []

        memories = []
        try:
            with open(self.memories_file, 'r') as f:
                for line in f:
                    if line.strip():
                        memories.append(json.loads(line))
        except Exception as e:
            print(f"⚠️  Could not load memories: {e}")

        return memories

    def _load_patterns(self) -> Dict[str, Any]:
        """Load learned patterns from storage."""
        if not self.patterns_file.exists():
            return {
                "market_patterns": [],
                "architectural_patterns": [],
                "risk_patterns": [],
                "success_indicators": []
            }

        try:
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load patterns: {e}")
            return {}

    def _load_profiles(self) -> Dict[str, Any]:
        """Load agent profiles and learning progress."""
        if not self.agent_profiles.exists():
            return {}

        try:
            with open(self.agent_profiles, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load profiles: {e}")
            return {}

    def store_analysis(self, agent_name: str, project_name: str, analysis: Dict[str, Any]):
        """Store a completed analysis for future reference."""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "project": project_name,
            "analysis": analysis,
            "memory_id": hashlib.md5(
                f"{agent_name}{project_name}{datetime.now()}".encode()
            ).hexdigest()[:8]
        }

        # Append to memories file
        try:
            with open(self.memories_file, 'a') as f:
                f.write(json.dumps(memory) + '\n')
        except Exception as e:
            print(f"⚠️  Could not store memory: {e}")

        # Update agent profile
        self._update_agent_profile(agent_name, analysis)

    def store_pattern(self, pattern_type: str, pattern: Dict[str, Any]):
        """Store a discovered pattern in the system."""
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = []

        self.patterns[pattern_type].append({
            "pattern": pattern,
            "discovered_at": datetime.now().isoformat(),
            "confidence": pattern.get("confidence", 0.7)
        })

        # Save patterns
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save pattern: {e}")

    def _update_agent_profile(self, agent_name: str, analysis: Dict[str, Any]):
        """Update agent's learning profile."""
        if agent_name not in self.profiles:
            self.profiles[agent_name] = {
                "analyses_conducted": 0,
                "success_rate": 0.0,
                "specializations": [],
                "learning_score": 0.0,
                "last_updated": None
            }

        profile = self.profiles[agent_name]
        profile["analyses_conducted"] += 1
        profile["last_updated"] = datetime.now().isoformat()

        # Update learning score based on analysis complexity
        complexity = len(str(analysis))
        profile["learning_score"] += min(0.5, complexity / 10000)

        # Save profiles
        try:
            with open(self.agent_profiles, 'w') as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save profile: {e}")

    def retrieve_relevant_memories(self, query: str, agent_name: str = None, limit: int = 5) -> List[Dict]:
        """Retrieve relevant past memories using simple semantic matching."""
        relevant = []

        query_words = set(query.lower().split())

        for memory in self.memories:
            if agent_name and memory.get("agent") != agent_name:
                continue

            # Simple keyword matching
            memory_text = json.dumps(memory).lower()
            matching_words = len(query_words & set(memory_text.split()))

            if matching_words > 0:
                relevant.append({
                    "memory": memory,
                    "relevance_score": matching_words / len(query_words)
                })

        # Sort by relevance
        relevant.sort(key=lambda x: x["relevance_score"], reverse=True)
        return [r["memory"] for r in relevant[:limit]]

    def get_agent_insights(self, agent_name: str) -> Dict[str, Any]:
        """Get agent's accumulated insights and learning."""
        profile = self.profiles.get(agent_name, {})
        memories = [m for m in self.memories if m.get("agent") == agent_name]

        # Analyze patterns in agent's memories
        successful_patterns = []
        common_recommendations = []

        for memory in memories[-10:]:  # Look at last 10 analyses
            analysis = memory.get("analysis", {})
            if analysis.get("recommendation"):
                common_recommendations.append(analysis["recommendation"])

        return {
            "agent": agent_name,
            "profile": profile,
            "recent_analyses": len(memories),
            "common_recommendations": common_recommendations[-3:],
            "learning_trajectory": self._calculate_learning_trajectory(agent_name)
        }

    def _calculate_learning_trajectory(self, agent_name: str) -> str:
        """Calculate agent's learning progress."""
        profile = self.profiles.get(agent_name, {})
        score = profile.get("learning_score", 0)

        if score >= 10:
            return "Expert level - Deep mastery"
        elif score >= 5:
            return "Advanced - Strong expertise"
        elif score >= 2:
            return "Intermediate - Growing expertise"
        elif score > 0:
            return "Beginner - Learning"
        else:
            return "No learning recorded yet"

    def get_system_insights(self) -> Dict[str, Any]:
        """Get overall system insights and trends."""
        total_analyses = len(self.memories)
        total_patterns = sum(len(v) for v in self.patterns.values())

        # Most common project types analyzed
        project_types = {}
        for memory in self.memories:
            project = memory.get("project", "unknown")
            project_types[project] = project_types.get(project, 0) + 1

        top_projects = sorted(project_types.items(), key=lambda x: x[1], reverse=True)[:5]

        # Agent performance
        agent_performance = {}
        for agent_name, profile in self.profiles.items():
            agent_performance[agent_name] = {
                "analyses": profile.get("analyses_conducted", 0),
                "learning_score": profile.get("learning_score", 0),
                "trajectory": self._calculate_learning_trajectory(agent_name)
            }

        return {
            "total_analyses": total_analyses,
            "total_patterns_learned": total_patterns,
            "most_analyzed_projects": top_projects,
            "agent_performance": agent_performance,
            "memory_health": "🟢 Healthy" if total_analyses > 0 else "🟡 Building"
        }

    def print_memory_status(self):
        """Print memory system status."""
        insights = self.get_system_insights()

        print("\n" + "=" * 70)
        print("🧠 COLLECTIVE MEMORY STATUS")
        print("=" * 70)

        print(f"\n📊 System Insights:")
        print(f"   Total analyses: {insights['total_analyses']}")
        print(f"   Patterns learned: {insights['total_patterns_learned']}")
        print(f"   Memory status: {insights['memory_health']}")

        if insights['most_analyzed_projects']:
            print(f"\n📈 Most Analyzed Projects:")
            for project, count in insights['most_analyzed_projects']:
                print(f"   • {project}: {count} analyses")

        print(f"\n🧙 Agent Learning Progress:")
        for agent, performance in insights['agent_performance'].items():
            print(f"   • {agent}:")
            print(f"     - Analyses: {performance['analyses']}")
            print(f"     - Learning Score: {performance['learning_score']:.2f}")
            print(f"     - Trajectory: {performance['trajectory']}")

        print()


def create_rag_memory(storage_path: str = None) -> RAGMemory:
    """Factory function for RAG memory."""
    return RAGMemory(storage_path)
