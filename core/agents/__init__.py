"""
Simple Agent System - 7 core agents for the Wisdom Council
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid

@dataclass
class Agent:
    """A simple agent with clear role and capabilities."""
    id: str
    name: str
    role: str  # e.g., "Analyst", "Developer", "Researcher"
    description: str
    skills: List[str] = field(default_factory=list)
    is_active: bool = True
    current_task: str = ""
    completed_tasks: int = 0
    learning_score: float = 0.0  # 0-1, improves with experience

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]

    def start_task(self, task_id: str) -> bool:
        """Mark agent as working on a task."""
        self.current_task = task_id
        return True

    def complete_task(self, success: bool = True) -> None:
        """Mark task as complete and improve learning score."""
        if success:
            self.completed_tasks += 1
            # Increase learning score gradually (0.01 per task, capped at 1.0)
            self.learning_score = min(1.0, self.completed_tasks * 0.01)
        self.current_task = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'description': self.description,
            'skills': self.skills,
            'is_active': self.is_active,
            'current_task': self.current_task,
            'completed_tasks': self.completed_tasks,
            'learning_score': self.learning_score,
        }


# Define the 7 Core Agents
CORE_AGENTS = [
    Agent(
        id="analyst",
        name="Lyra",
        role="Analyst",
        description="Analyzes projects, identifies patterns, extracts insights",
        skills=["analysis", "research", "data-extraction", "pattern-recognition"],
    ),
    Agent(
        id="architect",
        name="Iorek",
        role="Architect",
        description="Designs system architecture, proposes solutions, structures complexity",
        skills=["design", "architecture", "planning", "problem-solving"],
    ),
    Agent(
        id="developer",
        name="Marisa",
        role="Developer",
        description="Writes and implements code, creates features, maintains quality",
        skills=["coding", "implementation", "debugging", "optimization"],
    ),
    Agent(
        id="researcher",
        name="Serafina",
        role="Researcher",
        description="Conducts research, gathers information, explores solutions",
        skills=["research", "investigation", "exploration", "knowledge-gathering"],
    ),
    Agent(
        id="writer",
        name="Lee",
        role="Writer",
        description="Creates documentation, writes content, communicates ideas",
        skills=["writing", "documentation", "communication", "content-creation"],
    ),
    Agent(
        id="tester",
        name="Pantalaimon",
        role="Tester",
        description="Tests functionality, validates quality, finds issues",
        skills=["testing", "quality-assurance", "validation", "bug-detection"],
    ),
    Agent(
        id="coordinator",
        name="Philip",
        role="Coordinator",
        description="Coordinates between agents, manages tasks, ensures progress",
        skills=["coordination", "management", "communication", "decision-making"],
    ),
]


def create_agent(agent_id: str) -> Agent:
    """Get or create an agent by ID."""
    for agent in CORE_AGENTS:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"Agent {agent_id} not found")


def list_agents() -> List[Agent]:
    """Get all available agents."""
    return CORE_AGENTS.copy()


def get_agent_by_role(role: str) -> List[Agent]:
    """Get agents by their role."""
    return [a for a in CORE_AGENTS if a.role.lower() == role.lower()]


def find_best_agent_for_task(task_description: str) -> Agent:
    """Find the best agent for a task based on keywords."""
    keywords = task_description.lower().split()

    # Simple scoring system
    scores = {}

    for agent in CORE_AGENTS:
        score = 0
        agent_skills = " ".join(agent.skills).lower()

        for keyword in keywords:
            if keyword in agent_skills or keyword in agent.role.lower():
                score += 1

        scores[agent.id] = score

    # Return agent with highest score (or Coordinator as default)
    best_id = max(scores, key=scores.get)
    return create_agent(best_id) if scores[best_id] > 0 else create_agent("coordinator")
