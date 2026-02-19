"""
Advanced Reasoning Layer - MCTS + Agent Integration
His Dark Materials Wisdom Council v3

Exports:
    MCTSTree, MCTSNode         - Tree search structure
    ReasoningAgent, Qwen3Loader - LLM reasoning + model loader
    DynamicRouter              - RAM-aware sequential routing
    ReasoningMemory            - Persist / retrieve reasoning paths
"""

from .mcts_tree import MCTSTree, MCTSNode
from .reasoning_agent import ReasoningAgent, Qwen3Loader
from .dynamic_router import DynamicRouter
from .reasoning_memory import ReasoningMemory

__all__ = [
    "MCTSTree",
    "MCTSNode",
    "ReasoningAgent",
    "Qwen3Loader",
    "DynamicRouter",
    "ReasoningMemory",
]
