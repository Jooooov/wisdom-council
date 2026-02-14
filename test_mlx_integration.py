#!/usr/bin/env python3
"""
Test MLX Integration - Verify Qwen3 8B model loads and works
"""
import asyncio
import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.llm import RAMManager, create_mlx_loader


async def main():
    """Test MLX integration."""
    print("=" * 70)
    print("🔬 MLX Integration Test - Qwen3 8B MLX 8bit")
    print("=" * 70)

    # Check RAM
    ram_manager = create_ram_manager()
    print("\n📊 System Memory Check:")
    ram_manager.print_status()

    # Check if model exists
    loader = create_mlx_loader(ram_manager)
    print(f"\n🔍 Model Status:")
    print(f"  Model: {loader.model_name}")
    print(f"  Path: {loader.model_path}")
    print(f"  Exists: {loader.model_exists()}")
    print(f"  Can Load: {loader.can_load()}")

    if not loader.model_exists():
        print(f"\n❌ Model not found at {loader.model_path}")
        print(f"   Available models:")
        mlx_dir = Path.home() / "mlx-models"
        for model_dir in mlx_dir.glob("*"):
            if model_dir.is_dir():
                print(f"   • {model_dir.name}")
        return False

    # Try to load model
    if loader.can_load():
        print(f"\n🚀 Loading model (this takes ~20 seconds)...")
        success = await loader.load()

        if success:
            print(f"✅ Model loaded successfully!")
            print(f"   Status: {loader.get_status()}")

            # Test generation
            print(f"\n💬 Testing generation...")
            prompt = "What is 2+2?"
            response = await loader.generate(prompt, max_tokens=50)
            print(f"   Prompt: {prompt}")
            print(f"   Response: {response}")

            # Cleanup
            loader.unload()
            print(f"\n✅ Test completed successfully!")
            return True
        else:
            print(f"❌ Failed to load model")
            return False
    else:
        print(f"\n⚠️  Insufficient RAM to load model")
        print(f"   Available: {ram_manager.available_ram:.1f}GB")
        print(f"   Required: {ram_manager.QWEN3_8B_MIN}GB")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
