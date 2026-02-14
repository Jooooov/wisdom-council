#!/usr/bin/env python3
"""
Download DeepSeek-R1-0528-Qwen3-8B MLX model from HuggingFace

This script uses mlx-lm to auto-download and cache the model.
The model will be cached in ~/.cache/huggingface/hub/
"""
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from core.llm import create_ram_manager, create_mlx_loader


async def main():
    """Download DeepSeek-R1-0528-Qwen3-8B-8bit model."""
    print("=" * 70)
    print("📥 DeepSeek-R1-0528-Qwen3-8B-8bit Model Downloader")
    print("=" * 70)
    print("\nℹ️  Model Details:")
    print("   Name:     DeepSeek-R1-0528-Qwen3-8B-8bit")
    print("   Size:     ~4GB (8-bit quantized)")
    print("   Language: Portuguese ✅ + English ✅")
    print("   Reasoning: Chain-of-thought ✅")
    print("   Framework: MLX (Apple Silicon optimized)")

    print("\n" + "=" * 70)
    print("System Check")
    print("=" * 70)

    # Check RAM
    ram = create_ram_manager()
    ram.print_status()

    loader = create_mlx_loader(ram)
    can_load, message = loader.check_ram_availability()
    print(f"\n{message}\n")

    if not can_load:
        print("❌ Insufficient RAM to download model")
        return False

    print("=" * 70)
    print("🚀 Starting Download")
    print("=" * 70)
    print("\nℹ️  First time loading may take 30-60 seconds")
    print("   The model will be cached for future use")
    print("   Cache location: ~/.cache/huggingface/hub/\n")

    try:
        # This will trigger the download via mlx-lm
        print("⏳ Loading model (auto-downloads ~4GB from HuggingFace)...")
        success = await loader.load()

        if success:
            print("\n" + "=" * 70)
            print("✅ SUCCESS! Model downloaded and loaded")
            print("=" * 70)
            print("\n🎉 DeepSeek-R1-0528-Qwen3-8B-8bit is ready!")
            print("\nNext steps:")
            print("   1. Run: python test_portuguese_8b.py")
            print("   2. Verify Portuguese + reasoning works")
            print("   3. Launch: python run.py")

            loader.unload()
            return True
        else:
            print("\n❌ Failed to load model")
            return False

    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
