"""
MLX LLM Loader - Loads and manages Qwen3-4B via MLX
Optimized for Apple Silicon with Portuguese + Reasoning
"""

import logging
from typing import Optional, Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Model paths
MLX_MODELS_DIR = Path.home() / "mlx-models"
# Using Qwen3-4B-4bit with reasoning capability + Portuguese
# This is the MLX-quantized version from mlx-community (auto-downloads from HuggingFace)
QWEN3_8B_MODEL_ID = "mlx-community/Qwen3-8B-4bit"
QWEN3_4B_MODEL_ID = "mlx-community/Qwen3-4B-4bit"
# Default — overridden at load time based on available RAM
QWEN3_MODEL_ID    = QWEN3_4B_MODEL_ID
QWEN3_MODEL_PATH  = MLX_MODELS_DIR / "Qwen3-4B-4bit"


class MLXLLMLoader:
    """Loads and manages Qwen3-4B via MLX framework."""

    def __init__(self, ram_manager: Any):
        self.ram_manager = ram_manager
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.model_name = "Qwen3-4B MLX"
        self.model_path = QWEN3_MODEL_PATH

    def model_exists(self) -> bool:
        """Check if model files exist locally or can be downloaded from HuggingFace."""
        # With HuggingFace models, mlx-lm will auto-download if not cached
        # So we always return True - the load() call will handle downloading
        return True

    def can_load(self) -> bool:
        """Check if model can be loaded (exists and RAM available)."""
        self.ram_manager.refresh()
        return self.model_exists() and self.ram_manager.can_run_qwen3_4b()

    def check_ram_availability(self) -> tuple[bool, str]:
        """
        Check RAM availability with detailed message.

        Returns:
            (can_load: bool, message: str)
        """
        self.ram_manager.refresh()

        available = self.ram_manager.available_ram
        minimum = self.ram_manager.QWEN3_4B_MIN
        ideal = self.ram_manager.QWEN3_4B_IDEAL

        if available >= ideal:
            return True, f"✅ Excellent: {available:.1f}GB available (ideal: {ideal}GB)"
        elif available >= minimum:
            return True, f"✅ Good: {available:.1f}GB available (minimum: {minimum}GB, may be slower)"
        else:
            deficit = minimum - available
            return False, (
                f"❌ CRITICAL: Insufficient RAM!\n"
                f"   Available: {available:.1f}GB\n"
                f"   Required: {minimum}GB minimum\n"
                f"   Deficit: {deficit:.1f}GB short!\n"
                f"\n   SOLUTIONS:\n"
                f"   1. Close all browser tabs\n"
                f"   2. Close Slack, Discord, email clients\n"
                f"   3. Close IDEs and text editors\n"
                f"   4. Restart your MacBook\n"
                f"   5. Try again in a minute or two"
            )

    async def load(self, force: bool = False) -> bool:
        """
        Load DeepSeek-R1-Distill-Qwen-8B model via MLX with RAM guardrails.

        Args:
            force: Force load even if RAM is low (NOT RECOMMENDED!)

        Returns:
            True if loaded successfully, False otherwise
        """

        if self.is_loaded:
            logger.info("✅ Qwen3-4B already loaded")
            return True

        # Note: Model will be auto-downloaded from HuggingFace if not cached locally
        # No need to pre-check existence - mlx-lm handles downloading

        # RAM Check with detailed guardrails
        self.ram_manager.refresh()

        # GUARDRAIL 1: Hard minimum check
        if self.ram_manager.available_ram < self.ram_manager.QWEN3_4B_MIN:
            logger.critical(
                f"❌ CRITICAL: Insufficient RAM!\n"
                f"   Available: {self.ram_manager.available_ram:.1f}GB\n"
                f"   Required: {self.ram_manager.QWEN3_4B_MIN}GB minimum\n"
                f"   Deficit: {self.ram_manager.QWEN3_4B_MIN - self.ram_manager.available_ram:.1f}GB short!\n"
                f"\n   Solutions:\n"
                f"   1. Close browser tabs, IDEs, Slack, etc.\n"
                f"   2. Restart your MacBook\n"
                f"   3. Close ALL other applications\n"
                f"   4. Try again in 1-2 minutes"
            )
            if not force:
                return False
            else:
                logger.warning("⚠️  Force loading with insufficient RAM - risk of crash!")

        # GUARDRAIL 2: Ideal RAM warning
        if self.ram_manager.available_ram < self.ram_manager.QWEN3_4B_IDEAL:
            logger.warning(
                f"⚠️  WARNING: RAM below ideal threshold!\n"
                f"   Available: {self.ram_manager.available_ram:.1f}GB\n"
                f"   Ideal: {self.ram_manager.QWEN3_4B_IDEAL}GB\n"
                f"   Model will work but may be slower or unstable\n"
                f"   Recommendation: Close other applications"
            )
            print(f"\n⚠️  WARNING: Running below ideal RAM conditions!")
            print(f"   Available: {self.ram_manager.available_ram:.1f}GB (ideal: {self.ram_manager.QWEN3_4B_IDEAL}GB)")
            print(f"   Close other apps for better performance\n")

        # GUARDRAIL 3: Normal operation
        self.ram_manager.warn_if_low("qwen3_4b")

        # Select best model based on RAM
        avail = self.ram_manager.available_ram
        active_model_id = QWEN3_8B_MODEL_ID if avail >= 5.5 else QWEN3_4B_MODEL_ID
        active_model_name = "Qwen3-8B-4bit" if avail >= 5.5 else "Qwen3-4B-4bit"
        size_hint = "~4.5GB" if avail >= 5.5 else "~2.3GB"
        self.model_name = active_model_name

        try:
            print("\n" + "=" * 70)
            print(f"🔄 Loading {active_model_name} MLX Model")
            print("=" * 70)
            print(f"Model: {active_model_name}")
            print(f"HuggingFace ID: {active_model_id}")
            print(f"Available RAM: {self.ram_manager.available_ram:.1f}GB")
            print(f"Required: {self.ram_manager.QWEN3_4B_MIN}GB minimum")
            print(f"\n⏳ Loading (first time takes ~30-60 seconds, auto-downloads {size_hint})...")

            # GUARDRAIL 4: Pre-load RAM check
            self.ram_manager.refresh()
            if self.ram_manager.available_ram < self.ram_manager.QWEN3_4B_MIN:
                raise MemoryError(
                    f"Insufficient RAM for model loading! "
                    f"Available: {self.ram_manager.available_ram:.1f}GB, "
                    f"Required: {self.ram_manager.QWEN3_4B_MIN}GB"
                )

            # Load using MLX
            self.model, self.tokenizer = await self._load_mlx(active_model_id)

            if self.model is not None and self.tokenizer is not None:
                self.is_loaded = True

                # GUARDRAIL 5: Post-load RAM verification
                self.ram_manager.refresh()
                logger.info(f"✅ Successfully loaded {self.model_name}")
                print(f"✅ Model loaded successfully!")
                print(f"   RAM used: ~2.3GB")
                print(f"   Available for other apps: ~{max(0, self.ram_manager.available_ram - 2.3):.1f}GB")

                # Warn if remaining RAM is too low
                if self.ram_manager.available_ram < 3:
                    logger.warning(
                        f"⚠️  Very low RAM remaining ({self.ram_manager.available_ram:.1f}GB)!\n"
                        f"   Generation may be slow or cause crashes.\n"
                        f"   Close other applications before using the model."
                    )

                return True
            else:
                logger.error("Failed to load model via MLX")
                return False

        except MemoryError as e:
            logger.critical(f"❌ MEMORY ERROR: {e}")
            print(f"\n❌ MEMORY ERROR: {e}")
            print(f"\nSolutions:")
            print(f"  1. Close all other applications (browsers, IDEs, Slack, etc.)")
            print(f"  2. Restart your MacBook and try again")
            print(f"  3. Wait a minute for other processes to complete")
            return False

        except Exception as e:
            logger.error(f"Error loading Qwen3-4B: {e}")
            print(f"\n❌ Failed to load model: {e}")
            if "out of memory" in str(e).lower() or "memory" in str(e).lower():
                print(f"\n💡 This appears to be a memory error. Try:")
                print(f"   1. Close other applications")
                print(f"   2. Restart your MacBook")
                print(f"   3. Check: python -c \"from core.llm import create_ram_manager; create_ram_manager().print_status()\"")
            return False

    async def _load_mlx(self, model_id: str = QWEN3_4B_MODEL_ID) -> Tuple[Any, Any]:
        """Load model using MLX framework."""
        try:
            from mlx_lm import load

            print("   Using MLX (Apple Silicon unified memory)...")
            print(f"   Model ID: {model_id}")
            print(f"   (Auto-downloading from HuggingFace if not cached locally)")

            # Load model and tokenizer from HuggingFace (mlx-lm auto-downloads and caches)
            model, tokenizer = load(model_id)

            logger.info("✅ Model loaded successfully via MLX")
            return model, tokenizer

        except ImportError as e:
            logger.error(f"MLX not installed: {e}")
            logger.info("Install with: pip install mlx-lm")
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
