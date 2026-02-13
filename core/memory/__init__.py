"""
Simple Memory System - Agents learn from experience
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path


@dataclass
class Experience:
    """An agent's experience from completing a task."""
    agent_id: str
    task_description: str
    approach: str
    result: str
    success: bool
    learned: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'task_description': self.task_description,
            'approach': self.approach,
            'result': self.result,
            'success': self.success,
            'learned': self.learned,
            'timestamp': self.timestamp,
        }


class Memory:
    """Stores agent experiences and learning."""

    def __init__(self, memory_file: Path = None):
        self.experiences: List[Experience] = []
        self.memory_file = memory_file or Path.home() / ".wisdom_council" / "memory.json"
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.load()

    def add_experience(self, agent_id: str, task: str, approach: str, result: str, success: bool, learned: str = "") -> None:
        """Record an agent's experience."""
        exp = Experience(
            agent_id=agent_id,
            task_description=task,
            approach=approach,
            result=result,
            success=success,
            learned=learned,
        )
        self.experiences.append(exp)
        self.save()

    def get_agent_experiences(self, agent_id: str) -> List[Experience]:
        """Get all experiences for an agent."""
        return [e for e in self.experiences if e.agent_id == agent_id]

    def get_agent_success_rate(self, agent_id: str) -> float:
        """Calculate agent's success rate (0-1)."""
        exps = self.get_agent_experiences(agent_id)
        if not exps:
            return 0.0
        successful = sum(1 for e in exps if e.success)
        return successful / len(exps)

    def get_agent_learning(self, agent_id: str) -> List[str]:
        """Get what an agent has learned."""
        exps = self.get_agent_experiences(agent_id)
        return [e.learned for e in exps if e.learned]

    def get_similar_experiences(self, task_description: str, agent_id: str = None, limit: int = 3) -> List[Experience]:
        """Find similar past experiences."""
        # Simple keyword matching
        keywords = set(task_description.lower().split())

        candidates = self.experiences
        if agent_id:
            candidates = [e for e in candidates if e.agent_id == agent_id]

        scored = []
        for exp in candidates:
            exp_keywords = set(exp.task_description.lower().split())
            overlap = len(keywords & exp_keywords)
            if overlap > 0:
                scored.append((exp, overlap))

        # Sort by score and return top N
        scored.sort(key=lambda x: x[1], reverse=True)
        return [e[0] for e in scored[:limit]]

    def save(self) -> None:
        """Save memory to file."""
        data = {
            'experiences': [e.to_dict() for e in self.experiences],
            'saved_at': datetime.now().isoformat(),
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    for exp_dict in data.get('experiences', []):
                        exp = Experience(
                            agent_id=exp_dict['agent_id'],
                            task_description=exp_dict['task_description'],
                            approach=exp_dict['approach'],
                            result=exp_dict['result'],
                            success=exp_dict['success'],
                            learned=exp_dict.get('learned', ''),
                            timestamp=exp_dict['timestamp'],
                        )
                        self.experiences.append(exp)
            except Exception as e:
                print(f"Error loading memory: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        if not self.experiences:
            return {'total_experiences': 0, 'agents': 0}

        agents = set(e.agent_id for e in self.experiences)
        total_success = sum(1 for e in self.experiences if e.success)

        return {
            'total_experiences': len(self.experiences),
            'agents': len(agents),
            'overall_success_rate': total_success / len(self.experiences),
            'agents_stats': {
                agent_id: {
                    'experiences': len(self.get_agent_experiences(agent_id)),
                    'success_rate': self.get_agent_success_rate(agent_id),
                }
                for agent_id in agents
            }
        }
