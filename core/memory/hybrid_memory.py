"""
Hybrid Memory System - RAG + Graph Memory for Agent Learning

Combines:
- Vector/Semantic Search (RAG) - Find similar past analyses
- Graph Memory - Track relationships between concepts, risks, opportunities
- Pattern Learning - Recognize industry patterns and decision patterns
- Experience Memory - Learn from project type similarities
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class HybridMemory:
    """Advanced learning system combining RAG + Graph memory."""

    def __init__(self, memory_dir: str = None):
        """Initialize hybrid memory."""
        if not memory_dir:
            memory_dir = str(Path.home() / ".wisdom_council" / "hybrid_memory")

        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Store different types of memories
        self.rag_memories = []  # Vector-searchable analyses
        self.graph = {}  # Concept graph and relationships
        self.patterns = {}  # Learned patterns by industry/role
        self.experiences = {}  # Indexed by project type

        self._load_memories()

    def _load_memories(self):
        """Load persisted memories from disk."""
        try:
            # Load RAG memories
            rag_file = self.memory_dir / "rag_memories.json"
            if rag_file.exists():
                with open(rag_file, 'r') as f:
                    self.rag_memories = json.load(f)

            # Load graph memory
            graph_file = self.memory_dir / "graph.json"
            if graph_file.exists():
                with open(graph_file, 'r') as f:
                    self.graph = json.load(f)

            # Load patterns
            patterns_file = self.memory_dir / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    self.patterns = json.load(f)

        except Exception as e:
            print(f"   ⚠️  Erro ao carregar memória: {e}")

    def store_analysis(self, analysis: Dict[str, Any]):
        """Store a complete analysis for learning."""
        # Store in RAG memory
        rag_entry = {
            "timestamp": datetime.now().isoformat(),
            "project": analysis.get("project_name"),
            "type": analysis.get("project_type"),
            "summary": analysis.get("summary", ""),
            "perspectives": analysis.get("perspectives", {}),
            "conclusion": analysis.get("conclusion", ""),
            "embedding_keywords": self._extract_keywords(analysis)
        }
        self.rag_memories.append(rag_entry)

        # Store in graph memory - build relationships
        self._add_to_graph(analysis)

        # Learn patterns
        self._learn_patterns(analysis)

        # Persist
        self._save_memories()

    def _extract_keywords(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract key concepts from analysis."""
        keywords = set()

        # From project type
        if analysis.get("project_type"):
            keywords.add(analysis["project_type"].lower())

        # From perspectives
        perspectives = analysis.get("perspectives", {})
        for perspective in perspectives.values():
            if isinstance(perspective, dict):
                reasoning = perspective.get("reasoning", "")
                # Simple keyword extraction
                words = reasoning.split()
                important_words = [w.lower().strip('.,;:') for w in words
                                 if len(w) > 5 and w[0].isupper()]
                keywords.update(important_words[:5])

        return list(keywords)

    def _add_to_graph(self, analysis: Dict[str, Any]):
        """Add analysis insights to concept graph."""
        project_name = analysis.get("project_name", "unknown")

        if project_name not in self.graph:
            self.graph[project_name] = {
                "type": analysis.get("project_type"),
                "risks": [],
                "opportunities": [],
                "related_projects": [],
                "agent_insights": {}
            }

        # Extract risks and opportunities from agent perspectives
        perspectives = analysis.get("perspectives", {})
        for agent_name, perspective in perspectives.items():
            if isinstance(perspective, dict):
                reasoning = perspective.get("reasoning", "")

                # Simple pattern detection for risks/opportunities
                if any(word in reasoning.lower() for word in ["risk", "risco", "problem", "problema"]):
                    self.graph[project_name]["risks"].append({
                        "agent": agent_name,
                        "insight": reasoning[:200]
                    })

                if any(word in reasoning.lower() for word in ["opportunity", "oportunidade", "potential", "potencial"]):
                    self.graph[project_name]["opportunities"].append({
                        "agent": agent_name,
                        "insight": reasoning[:200]
                    })

    def _learn_patterns(self, analysis: Dict[str, Any]):
        """Learn patterns by project type and agent role."""
        project_type = analysis.get("project_type", "unknown").lower()

        if project_type not in self.patterns:
            self.patterns[project_type] = {
                "count": 0,
                "common_risks": [],
                "common_opportunities": [],
                "decision_patterns": [],
                "success_factors": []
            }

        pattern = self.patterns[project_type]
        pattern["count"] += 1

        # Learn decision patterns
        perspectives = analysis.get("perspectives", {})
        for agent_role, perspective in perspectives.items():
            if isinstance(perspective, dict):
                recommendation = perspective.get("recommendation", "")
                if recommendation:
                    pattern["decision_patterns"].append(recommendation)

    def _save_memories(self):
        """Persist memories to disk."""
        try:
            # Save RAG memories
            rag_file = self.memory_dir / "rag_memories.json"
            with open(rag_file, 'w') as f:
                json.dump(self.rag_memories, f, indent=2)

            # Save graph
            graph_file = self.memory_dir / "graph.json"
            with open(graph_file, 'w') as f:
                json.dump(self.graph, f, indent=2)

            # Save patterns
            patterns_file = self.memory_dir / "patterns.json"
            with open(patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)

        except Exception as e:
            print(f"   ⚠️  Erro ao salvar memória: {e}")

    def retrieve_similar_analyses(self, query: str, project_type: str = None, top_k: int = 3) -> List[Dict]:
        """Retrieve similar past analyses using semantic search."""
        if not self.rag_memories:
            return []

        results = []

        for memory in self.rag_memories:
            # Simple semantic matching on keywords
            score = 0

            # Match project type
            if project_type and memory.get("type", "").lower() == project_type.lower():
                score += 2

            # Match keywords
            query_words = set(query.lower().split())
            memory_keywords = set(kw.lower() for kw in memory.get("embedding_keywords", []))
            matching_words = query_words & memory_keywords
            score += len(matching_words)

            # Match on summary content
            if query.lower() in memory.get("summary", "").lower():
                score += 1

            if score > 0:
                results.append((score, memory))

        # Sort by score and return top-k
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:top_k]]

    def retrieve_pattern_insights(self, project_type: str) -> Optional[Dict]:
        """Get learned patterns for a project type."""
        project_type_lower = project_type.lower()
        return self.patterns.get(project_type_lower)

    def retrieve_graph_relationships(self, project_name: str) -> Optional[Dict]:
        """Get graph relationships and insights for a project."""
        return self.graph.get(project_name)

    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of what the system has learned."""
        return {
            "total_analyses": len(self.rag_memories),
            "known_project_types": list(self.patterns.keys()),
            "pattern_count": len(self.patterns),
            "graph_nodes": len(self.graph),
            "latest_analysis": self.rag_memories[-1] if self.rag_memories else None
        }


def create_hybrid_memory(memory_dir: str = None) -> HybridMemory:
    """Factory function to create hybrid memory."""
    return HybridMemory(memory_dir)
