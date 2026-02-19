"""
RAM Manager - Monitors and manages system memory
Critical for running Qwen3-4B with reasoning on Apple Silicon
"""

import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RAMManager:
    """Manages RAM for LLM operations."""

    # Memory requirements (in GB)
    # Using Qwen3-4B-MLX-4bit with reasoning + Portuguese
    # 4-bit quantized MLX model: ~2.3GB model + ~1.2GB overhead + buffer
    QWEN3_4B_MIN = 3.5    # Minimum for Qwen3-4B (with reasoning + safety buffer)
    QWEN3_4B_IDEAL = 5.5  # Ideal for smooth operation
    # Keep old names as aliases for backward compatibility
    DEEPSEEK_R1_8B_MIN = 3.5
    DEEPSEEK_R1_8B_IDEAL = 5.5
    FALLBACK_MIN = 4

    def __init__(self):
        self.system_ram = self._get_total_ram()
        self.available_ram = self._get_available_ram()

    def _get_total_ram(self) -> float:
        """Get total system RAM in GB."""
        try:
            total_bytes = psutil.virtual_memory().total
            return total_bytes / (1024 ** 3)
        except Exception as e:
            logger.error(f"Could not get total RAM: {e}")
            return 0

    def _get_available_ram(self) -> float:
        """Get available system RAM in GB."""
        try:
            available_bytes = psutil.virtual_memory().available
            return available_bytes / (1024 ** 3)
        except Exception as e:
            logger.error(f"Could not get available RAM: {e}")
            return 0

    def refresh(self):
        """Refresh RAM information."""
        self.available_ram = self._get_available_ram()

    def can_run_qwen3_4b(self) -> bool:
        """Check if system can run Qwen3-4B."""
        self.refresh()
        return self.available_ram >= self.QWEN3_4B_MIN

    # Backward-compatibility alias
    def can_run_deepseek_14b(self) -> bool:
        return self.can_run_qwen3_4b()

    def get_status(self) -> Dict[str, Any]:
        """Get detailed RAM status."""
        self.refresh()

        total_percent = (self.available_ram / self.system_ram * 100) if self.system_ram > 0 else 0

        status = {
            "total_ram_gb": round(self.system_ram, 2),
            "available_ram_gb": round(self.available_ram, 2),
            "used_ram_gb": round(self.system_ram - self.available_ram, 2),
            "available_percentage": round(total_percent, 1),
            "qwen3_4b_can_run": self.can_run_qwen3_4b(),
            "qwen3_4b_min_gb": self.QWEN3_4B_MIN,
            "qwen3_4b_ideal_gb": self.QWEN3_4B_IDEAL,
            "status_message": self._get_status_message()
        }

        return status

    def _get_status_message(self) -> str:
        """Generate human-readable status message."""
        if self.available_ram >= self.QWEN3_4B_IDEAL:
            return "✅ Excellent - Qwen3-4B will run smoothly"
        elif self.available_ram >= self.QWEN3_4B_MIN:
            return "✅ Good - Qwen3-4B can run (reasoning may be slower)"
        elif self.available_ram >= self.FALLBACK_MIN:
            return "⚠️  Limited - Only small models recommended"
        else:
            return "❌ Critical - Not enough RAM for LLM"

    def warn_if_low(self, model: str = "qwen3_4b"):
        """Emit warning if RAM is too low for model."""
        self.refresh()

        if model in ["qwen3_4b", "qwen3", "deepseek_r1", "deepseek-r1", "deepseek_r1_14b"]:
            min_ram = self.QWEN3_4B_MIN
            ideal_ram = self.QWEN3_4B_IDEAL
            model_name = "Qwen3-4B"
        else:
            min_ram = self.FALLBACK_MIN
            ideal_ram = self.FALLBACK_MIN
            model_name = model

        if self.available_ram < min_ram:
            logger.critical(
                f"❌ CRITICAL: Insufficient RAM for {model_name}\n"
                f"   Available: {self.available_ram:.1f}GB\n"
                f"   Required: {min_ram}GB\n"
                f"   Please close other applications!"
            )
            return False

        if self.available_ram < ideal_ram:
            logger.warning(
                f"⚠️  WARNING: {model_name} may run slowly\n"
                f"   Available: {self.available_ram:.1f}GB\n"
                f"   Ideal: {ideal_ram}GB\n"
                f"   Consider closing other applications for better performance"
            )

        return True

    def print_status(self):
        """Print formatted RAM status."""
        status = self.get_status()

        print("\n" + "=" * 70)
        print("💾 SYSTEM MEMORY STATUS")
        print("=" * 70)
        print(f"\nTotal RAM:        {status['total_ram_gb']} GB")
        print(f"Available RAM:    {status['available_ram_gb']} GB ({status['available_percentage']}%)")
        print(f"Used RAM:         {status['used_ram_gb']} GB")

        print(f"\nQwen3-4B-MLX-4bit Requirements:")
        print(f"  Minimum:  {status['qwen3_4b_min_gb']} GB")
        print(f"  Ideal:    {status['qwen3_4b_ideal_gb']} GB")
        print(f"  Status:   {status['status_message']}")

        if not status['qwen3_4b_can_run']:
            print("\n⚠️  RECOMMENDATION:")
            print("   Close other applications to free up RAM:")
            print("   • Browser tabs")
            print("   • Email clients")
            print("   • IDEs/Text editors")
            print("   • Streaming apps")

        print()


def create_ram_manager() -> RAMManager:
    """Factory function for RAM manager."""
    return RAMManager()
