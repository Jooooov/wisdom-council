"""
MLX LLM Loader - Loads and manages Qwen3-4B via MLX
Optimized for Apple Silicon with Portuguese + Reasoning
"""

import logging
from typing import Optional, Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Local model store — shared across all apps
MLX_STORE     = Path.home() / "Desktop" / "apps" / "MLX"
QWEN3_8B_PATH = MLX_STORE / "Qwen3-8B-4bit"
QWEN3_4B_PATH = MLX_STORE / "Qwen3-4B-4bit"

# RAM thresholds
QWEN3_8B_MIN_RAM_GB = 5.5
QWEN3_4B_MIN_RAM_GB = 3.5


class MLXLLMLoader:
    """Loads Qwen3-8B-4bit or Qwen3-4B-4bit from ~/Desktop/apps/MLX/."""

    def __init__(self, ram_manager: Any):
        self.ram_manager = ram_manager
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.model_name = "Qwen3-4B-4bit"  # updated at load time
        self.model_path = QWEN3_4B_PATH    # updated at load time

    def _select_model(self) -> tuple[Path, str]:
        """Return (local_path, display_name) based on free RAM."""
        self.ram_manager.refresh()
        if self.ram_manager.available_ram >= QWEN3_8B_MIN_RAM_GB:
            return QWEN3_8B_PATH, "Qwen3-8B-4bit"
        return QWEN3_4B_PATH, "Qwen3-4B-4bit"

    def model_exists(self) -> bool:
        """Check if selected model exists locally."""
        path, _ = self._select_model()
        return path.exists() and (path / "config.json").exists()

    def can_load(self) -> bool:
        """Check if model can be loaded (exists locally and RAM available)."""
        self.ram_manager.refresh()
        return self.model_exists() and self.ram_manager.can_run_qwen3_4b()

    def check_ram_availability(self) -> tuple[bool, str]:
        """Return (can_load, human-readable message)."""
        self.ram_manager.refresh()
        gb = self.ram_manager.available_ram
        if gb >= QWEN3_8B_MIN_RAM_GB:
            return True, f"✅ Excellent: {gb:.1f}GB free — will use Qwen3-8B-4bit"
        elif gb >= QWEN3_4B_MIN_RAM_GB:
            return True, f"✅ Good: {gb:.1f}GB free — will use Qwen3-4B-4bit"
        else:
            return False, (
                f"❌ Insufficient RAM: {gb:.1f}GB free (need {QWEN3_4B_MIN_RAM_GB}GB).\n"
                f"   Close browser tabs, IDEs, Slack, and other apps."
            )

    async def load(self, force: bool = False) -> bool:
        """Load the selected Qwen3 model from ~/Desktop/apps/MLX/."""
        if self.is_loaded:
            return True

        ok, msg = self.check_ram_availability()
        print(msg)
        if not ok and not force:
            return False

        path, name = self._select_model()
        self.model_name = name
        self.model_path = path

        # Guard: model must exist locally — no downloads
        if not path.exists() or not (path / "config.json").exists():
            print(f"\n❌ Model not found: {path}")
            print(f"   Run the download script:")
            print(f"   python3 ~/Desktop/apps/MLX/download_models.py")
            return False

        try:
            print("\n" + "=" * 70)
            print(f"🔄 Loading {name}")
            print("=" * 70)
            print(f"   Path:  {path}")
            print(f"   RAM:   {self.ram_manager.available_ram:.1f}GB free")
            print(f"\n⏳ Loading model (may take ~30 seconds)...")

            self.model, self.tokenizer = await self._load_mlx(path)

            if self.model is not None and self.tokenizer is not None:
                self.is_loaded = True
                self.ram_manager.refresh()
                logger.info(f"✅ Successfully loaded {name}")
                print(f"✅ {name} loaded!")
                print(f"   RAM remaining: ~{self.ram_manager.available_ram:.1f}GB free")
                return True
            else:
                logger.error("Failed to load model via MLX")
                return False

        except MemoryError as e:
            print(f"\n❌ Out of RAM: {e}")
            print(f"   Close other applications and try again.")
            return False

        except Exception as e:
            logger.error(f"Error loading {name}: {e}")
            print(f"\n❌ Failed to load {name}: {e}")
            return False

    async def _load_mlx(self, model_path: Path) -> Tuple[Any, Any]:
        """Load model from local path using MLX."""
        try:
            from mlx_lm import load
            print(f"   Using MLX (Apple Silicon unified memory)...")
            model, tokenizer = load(str(model_path))
            logger.info("✅ Model loaded via MLX")
            return model, tokenizer
        except ImportError as e:
            logger.error(f"MLX not installed: {e}")
            raise
        except Exception as e:
            logger.error(f"MLX load failed: {e}")
            raise

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 200,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using Qwen3-4B MLX with RAM protection.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate (keep <= 200 for performance)
            temperature: Sampling temperature

        Returns:
            Generated text

        Raises:
            RuntimeError: If model not loaded or not enough RAM
            MemoryError: If system runs out of RAM during generation
        """

        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model or tokenizer is None")

        # GUARDRAIL 6: Pre-generation RAM check
        self.ram_manager.refresh()
        if self.ram_manager.available_ram < 2:  # Need at least 2GB for generation
            raise MemoryError(
                f"Insufficient RAM for generation! "
                f"Available: {self.ram_manager.available_ram:.1f}GB (need 2GB minimum). "
                f"Close other applications."
            )

        # Warn if RAM is low but usable
        if self.ram_manager.available_ram < 3:
            logger.warning(
                f"⚠️  Low RAM for generation: {self.ram_manager.available_ram:.1f}GB available. "
                f"Generation may be slow or unstable."
            )

        try:
            from mlx_lm import generate

            logger.info(f"Generating with max_tokens={max_tokens}")

            # Generate using MLX - temperature not supported in current version
            # Use default sampling parameters
            response = generate(
                self.model,
                self.tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                verbose=False
            )

            return response.strip()

        except MemoryError as e:
            logger.critical(f"❌ OUT OF MEMORY during generation: {e}")
            raise MemoryError(
                f"System ran out of RAM during generation!\n"
                f"Current available: {self.ram_manager.available_ram:.1f}GB\n"
                f"Try:\n"
                f"  1. Reduce max_tokens (e.g., 50 instead of 200)\n"
                f"  2. Close other applications\n"
                f"  3. Restart and try again"
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            if "memory" in str(e).lower() or "out of" in str(e).lower():
                logger.critical("This appears to be a memory-related error!")
            raise

    def unload(self):
        """Unload model to free RAM."""
        if self.model is not None:
            del self.model
            self.model = None

        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        self.is_loaded = False
        logger.info("Model unloaded, RAM freed")

    def get_status(self) -> dict:
        """Get model loading status."""
        return {
            "is_loaded": self.is_loaded,
            "model_name": self.model_name,
            "model_path": str(self.model_path),
            "model_exists": self.model_exists(),
            "model_available": self.model is not None,
            "tokenizer_available": self.tokenizer is not None,
            "can_load": self.can_load(),
            "framework": "MLX (Apple Silicon)",
            "quantization": "4-bit"
        }


def create_mlx_loader(ram_manager: Any) -> MLXLLMLoader:
    """Factory function for MLX loader."""
    return MLXLLMLoader(ram_manager)
