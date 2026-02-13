"""
The Wisdom Council v2 - Simplified Multi-Agent System

A leaner, more practical approach to autonomous agents working on real projects.
"""

__version__ = "2.0.0"
__author__ = "João Vicente"

from .agents import create_agent, list_agents
from .tasks import Task, TaskManager
from .memory import Memory

__all__ = [
    'create_agent',
    'list_agents',
    'Task',
    'TaskManager',
    'Memory',
]
