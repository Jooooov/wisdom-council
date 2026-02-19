"""
LLM Module - Local Language Model Integration
- RAM monitoring for safe model loading
- Qwen3-4B-MLX-4bit loader with reasoning capability
- Deep code analysis with semantic understanding and Portuguese support
"""

from .ram_manager import RAMManager, create_ram_manager
from .deepseek_loader import MLXLLMLoader, create_mlx_loader
from .deepseek_analyzer import MLXAnalyzer, analyze_with_mlx

__all__ = [
    "RAMManager",
    "create_ram_manager",
    "MLXLLMLoader",
    "create_mlx_loader",
    "MLXAnalyzer",
    "analyze_with_mlx",
]
