"""
The Wisdom Council - 8 Agents from His Dark Materials
7 Core Agents + Mary Malone (Tools Manager & Context Keeper)
Each with unique daemon and specialized skills
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid

@dataclass
class Agent:
    """
    An agent based on His Dark Materials characters.
    Each has a daemon (external manifestation of soul).
    """
    id: str
    name: str                    # Character name from His Dark Materials
    character: str               # Full character description
    role: str                    # Professional role
    daemon: str                  # Their daemon (external soul/animal)
    description: str
    skills: List[str] = field(default_factory=list)
    personality_traits: List[str] = field(default_factory=list)
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
            'character': self.character,
            'role': self.role,
            'daemon': self.daemon,
            'description': self.description,
            'skills': self.skills,
            'personality_traits': self.personality_traits,
            'is_active': self.is_active,
            'current_task': self.current_task,
            'completed_tasks': self.completed_tasks,
            'learning_score': self.learning_score,
        }


# The 8 Core Agents - Characters from His Dark Materials
CORE_AGENTS = [
    Agent(
        id="analyst",
        name="Lyra",
        character="Lyra Belacqua - Curious, brave, truth-seeker",
        role="Analyst",
        daemon="Pantalaimon (marten, proteus daemon - can change shape)",
        description="Analyzes deeply, seeks patterns, questions assumptions",
        skills=["analysis", "research", "truth-seeking", "pattern-recognition", "curiosity"],
        personality_traits=["curious", "brave", "honest", "protective"],
    ),
    Agent(
        id="architect",
        name="Iorek",
        character="Iorek Byrnison - Armored bear warrior",
        role="Architect",
        daemon="None (sentient bear, no human daemon)",
        description="Designs robust structures, provides strength and protection, resolves conflicts",
        skills=["design", "architecture", "structure", "strength", "protection"],
        personality_traits=["strong", "honorable", "protective", "strategic"],
    ),
    Agent(
        id="developer",
        name="Marisa",
        character="Marisa Coulter - Ambitious, charismatic, decisive",
        role="Developer",
        daemon="Golden Monkey (intelligent, precise, commanding)",
        description="Executes with ambition, drives projects forward, makes decisive actions",
        skills=["execution", "implementation", "ambition", "decisiveness", "action"],
        personality_traits=["ambitious", "charismatic", "decisive", "driven"],
    ),
    Agent(
        id="researcher",
        name="Serafina",
        character="Serafina Pekkala - Queen of the witches",
        role="Researcher",
        daemon="Witch-nature (aerial perspective, ancient wisdom)",
        description="Conducts deep research, sees big picture, gathers ancient knowledge",
        skills=["research", "investigation", "wisdom", "big-picture-thinking", "knowledge"],
        personality_traits=["wise", "strategic", "far-seeing", "knowledgeable"],
    ),
    Agent(
        id="writer",
        name="Lee",
        character="Lee Scoresby - Aeronaut storyteller",
        role="Writer",
        daemon="Hester (hare - fast, aware, communicative)",
        description="Creates clear communication, tells stories, documents discoveries",
        skills=["writing", "documentation", "storytelling", "communication", "clarity"],
        personality_traits=["loyal", "brave", "communicative", "observant"],
    ),
    Agent(
        id="validator",
        name="Coram",
        character="Farder Coram - Experienced gyptian",
        role="Validator",
        daemon="Sophonax (water bird/lavender - careful, experienced)",
        description="Validates thoroughly, tests carefully, brings experience, identifies risks",
        skills=["validation", "testing", "risk-assessment", "experience", "caution"],
        personality_traits=["experienced", "careful", "wise", "protective"],
    ),
    Agent(
        id="coordinator",
        name="Asriel",
        character="Lord Asriel - Strategic leader, ambitious visionary",
        role="Coordinator",
        daemon="Stelmaria (snow leopard - powerful, protective, regal)",
        description="Coordinates grand strategy, commands loyalty, drives ambitious vision forward",
        skills=["coordination", "leadership", "strategy", "vision", "command"],
        personality_traits=["ambitious", "strategic", "powerful", "charismatic"],
    ),
    Agent(
        id="tools_manager",
        name="Mary",
        character="Mary Malone - Scientist, observer, bridge between worlds, keeper of knowledge",
        role="Tools Manager",
        daemon="Concept of Dust (represents interconnected knowledge and understanding)",
        description="Discovers tools, documents them deeply, maintains agent context and knowledge synthesis",
        skills=["tool_discovery", "scientific_analysis", "knowledge_synthesis", "context_management", "documentation"],
        personality_traits=["observant", "curious", "scientific", "communicative", "connective"],
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
