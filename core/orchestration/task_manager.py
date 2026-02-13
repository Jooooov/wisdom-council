"""
Task Manager - Manages workflow of agent tasks
- Creates and schedules tasks
- Tracks task status
- Manages dependencies
- Prioritizes work
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task lifecycle states."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Task:
    """Represents a single task for an agent."""

    def __init__(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.MEDIUM
    ):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.assigned_agent = assigned_agent
        self.priority = priority
        self.status = TaskStatus.PENDING

        # Metadata
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None

        # Dependencies
        self.depends_on = []  # Task IDs this depends on
        self.blocks = []  # Task IDs this blocks

    def start(self):
        """Mark task as started."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def complete(self, result: Any = None):
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def fail(self, error: str):
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assigned_agent": self.assigned_agent,
            "priority": self.priority.name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "dependencies": self.depends_on
        }


class TaskManager:
    """Manages all agent tasks and workflow."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []  # IDs in priority order
        self.agent_workload: Dict[str, int] = {}  # Tasks per agent
        self.completed_tasks: List[str] = []
        self.failed_tasks: List[str] = []

    def create_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        depends_on: Optional[List[str]] = None
    ) -> Task:
        """Create a new task."""

        task = Task(title, description, assigned_agent, priority)

        if depends_on:
            task.depends_on = depends_on

        self.tasks[task.id] = task
        self._enqueue_task(task)

        logger.info(f"Task created: {task.id} - {task.title}")

        return task

    def _enqueue_task(self, task: Task):
        """Add task to queue in priority order."""

        # Find insert position based on priority
        insert_pos = 0
        for i, task_id in enumerate(self.task_queue):
            queued_task = self.tasks[task_id]
            if task.priority.value < queued_task.priority.value:
                insert_pos = i
                break
            insert_pos = i + 1

        self.task_queue.insert(insert_pos, task.id)

    def get_next_task(self, agent_name: str) -> Optional[Task]:
        """Get next available task for an agent."""

        for task_id in self.task_queue:
            task = self.tasks[task_id]

            # Check if assigned to this agent
            if task.assigned_agent != agent_name:
                continue

            # Check if dependencies are met
            if not self._dependencies_met(task):
                continue

            # Check if already started
            if task.status != TaskStatus.PENDING:
                continue

            return task

        return None

    def _dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies are completed."""

        for dep_id in task.depends_on:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False

        return True

    def start_task(self, task_id: str):
        """Mark task as started."""

        task = self.tasks.get(task_id)
        if task:
            task.start()
            task.status = TaskStatus.IN_PROGRESS
            logger.info(f"Task started: {task_id}")

    def complete_task(self, task_id: str, result: Any = None):
        """Mark task as completed."""

        task = self.tasks.get(task_id)
        if task:
            task.complete(result)
            self.completed_tasks.append(task_id)
            self.task_queue.remove(task_id)
            logger.info(f"Task completed: {task_id}")

    def fail_task(self, task_id: str, error: str):
        """Mark task as failed."""

        task = self.tasks.get(task_id)
        if task:
            task.fail(error)
            self.failed_tasks.append(task_id)
            self.task_queue.remove(task_id)
            logger.error(f"Task failed: {task_id} - {error}")

    def get_agent_workload(self, agent_name: str) -> int:
        """Get number of active tasks for agent."""

        count = 0
        for task in self.tasks.values():
            if task.assigned_agent == agent_name and task.status in [
                TaskStatus.PENDING,
                TaskStatus.IN_PROGRESS
            ]:
                count += 1

        return count

    def get_status_summary(self) -> Dict[str, Any]:
        """Get overall task status summary."""

        total = len(self.tasks)
        completed = len(self.completed_tasks)
        failed = len(self.failed_tasks)
        pending = total - completed - failed

        return {
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "completion_percentage": int((completed / total * 100) if total > 0 else 0),
            "queue_length": len(self.task_queue),
            "failed_tasks": self.failed_tasks
        }

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents and their workload."""

        agent_status = {}

        for agent_name in set(t.assigned_agent for t in self.tasks.values()):
            tasks = [t for t in self.tasks.values() if t.assigned_agent == agent_name]
            completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]

            agent_status[agent_name] = {
                "total_assigned": len(tasks),
                "completed": len(completed),
                "active": self.get_agent_workload(agent_name),
                "success_rate": int((len(completed) / len(tasks) * 100) if tasks else 0)
            }

        return agent_status

    def list_tasks(self, status: Optional[TaskStatus] = None, agent: Optional[str] = None) -> List[Task]:
        """List tasks with optional filters."""

        result = []

        for task in self.tasks.values():
            if status and task.status != status:
                continue
            if agent and task.assigned_agent != agent:
                continue

            result.append(task)

        return result

    def export_tasks(self) -> List[Dict[str, Any]]:
        """Export all tasks as dictionaries."""

        return [task.to_dict() for task in self.tasks.values()]


def create_task_manager() -> TaskManager:
    """Factory function for task manager."""
    return TaskManager()
