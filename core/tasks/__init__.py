"""
Simple Task Management System
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """A simple task with clear objectives."""
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: str = ""  # Agent ID
    priority: int = 1  # 1-5, higher is more important
    subtasks: List['Task'] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]

    def assign_to(self, agent_id: str) -> None:
        """Assign task to an agent."""
        self.assigned_to = agent_id
        self.status = TaskStatus.ASSIGNED

    def start(self) -> None:
        """Mark task as started."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now().isoformat()

    def complete(self, result: str = "") -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
        self.result = result

    def fail(self, reason: str = "") -> None:
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now().isoformat()
        self.result = f"Failed: {reason}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'assigned_to': self.assigned_to,
            'priority': self.priority,
            'subtasks': [t.to_dict() for t in self.subtasks],
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'result': self.result,
        }


class TaskManager:
    """Manage tasks for a project."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_history: List[Task] = []

    def create_task(self, title: str, description: str, priority: int = 1) -> Task:
        """Create a new task."""
        task = Task(
            id="",
            title=title,
            description=description,
            priority=priority,
        )
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """List tasks, optionally filtered by status."""
        if status:
            return [t for t in self.tasks.values() if t.status == status]
        return list(self.tasks.values())

    def list_pending_tasks(self) -> List[Task]:
        """Get pending tasks."""
        return self.list_tasks(TaskStatus.PENDING)

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent."""
        task = self.get_task(task_id)
        if task:
            task.assign_to(agent_id)
            return True
        return False

    def get_tasks_for_agent(self, agent_id: str) -> List[Task]:
        """Get all tasks assigned to an agent."""
        return [t for t in self.tasks.values() if t.assigned_to == agent_id]

    def decompose_task(self, task_id: str, subtasks_desc: List[str]) -> bool:
        """Break a task into subtasks."""
        task = self.get_task(task_id)
        if not task:
            return False

        for desc in subtasks_desc:
            subtask = Task(id="", title=desc, description=desc)
            task.subtasks.append(subtask)

        return True

    def complete_task(self, task_id: str, result: str = "") -> bool:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.complete(result)
            self.task_history.append(task)
            return True
        return False

    def get_completion_stats(self) -> Dict[str, Any]:
        """Get task completion statistics."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        failed = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        in_progress = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])

        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'in_progress': in_progress,
            'pending': total - completed - failed - in_progress,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
        }
