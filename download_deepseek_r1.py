#!/usr/bin/env python3
"""
Download DeepSeek-R1-Distill-Qwen-14B MLX Model
For MacBook Air 16GB M4 with reasoning and Portuguese support
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run command with status reporting."""
    print(f"\n{'='*70}")
    print(f"🔄 {description}")
    print(f"{'='*70}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Completed: {description}")
    return True

def main():
    print("\n" + "="*70)
    print("📥 DeepSeek-R1-Distill-Qwen-14B MLX Download")
    print("="*70)

    mlx_models_dir = Path.home() / "mlx-models"
    model_dir = mlx_models_dir / "DeepSeek-R1-Distill-Qwen-14B-MLX"

    print(f"\n📍 Target directory: {model_dir}")
    print(f"📊 Space needed: ~8GB")

    # Check if model already exists
    if model_dir.exists():
        print(f"\n✅ Model already exists at {model_dir}")
        return True

    print(f"\n🚀 Starting download...")
    print(f"This may take several minutes depending on your internet connection")

    # Download using huggingface-hub CLI (if available)
    cmd = f"""
    python3 << 'EOF'
from huggingface_hub import snapshot_download
from pathlib import Path

print("🔍 Initializing download...")
target_dir = Path.home() / "mlx-models" / "DeepSeek-R1-Distill-Qwen-14B-MLX"

try:
    print(f"⏳ Downloading DeepSeek-R1-Distill-Qwen-14B from HuggingFace...")
    print(f"   This model is ~8GB, please be patient...")

    repo_id = "mlx-community/DeepSeek-R1-Distill-Qwen-14B"

    snapshot_download(
        repo_id=repo_id,
        local_dir=str(target_dir),
        repo_type="model",
        allow_patterns=["*.json", "*.safetensors", "*.tokenizer*", "*.model"]
    )

    print(f"✅ Download complete!")
    print(f"📁 Model saved at: {target_dir}")

except Exception as e:
    print(f"❌ Download failed: {e}")
    print(f"\\nTrying alternative method...")
    sys.exit(1)
EOF
"""

    if not run_command(cmd, "Download model from HuggingFace"):
        print("\n⚠️  HuggingFace download failed, trying Git LFS method...")

        # Fallback: use git lfs clone
        git_cmd = f"""
        cd "{mlx_models_dir}" && \\
        git clone https://huggingface.co/mlx-community/DeepSeek-R1-Distill-Qwen-14B DeepSeek-R1-Distill-Qwen-14B-MLX
        """

        if not run_command(git_cmd, "Clone via Git (requires git-lfs)"):
            print("\n❌ Both download methods failed")
            print("\nManual download:")
            print(f"1. Visit: https://huggingface.co/mlx-community/DeepSeek-R1-Distill-Qwen-14B")
            print(f"2. Download files to: ~/mlx-models/DeepSeek-R1-Distill-Qwen-14B-MLX/")
            return False

    # Verify download
    print(f"\n🔍 Verifying download...")
    if model_dir.exists():
        files = list(model_dir.glob("*"))
        print(f"✅ Model directory created with {len(files)} files")
        return True
    else:
        print(f"❌ Model directory not found")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
