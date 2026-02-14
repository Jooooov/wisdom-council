#!/usr/bin/env python3
"""
Verify DeepSeek-R1 setup is complete and ready
"""
from pathlib import Path
import sys

def verify():
    """Check if everything is set up correctly."""
    print("=" * 70)
    print("🔍 Verifying DeepSeek-R1 Setup")
    print("=" * 70)

    checks = []

    # 1. Model exists
    model_path = Path.home() / "mlx-models" / "DeepSeek-R1-Distill-Qwen-14B-MLX"
    model_exists = model_path.exists()
    checks.append(("Model directory exists", model_exists, str(model_path)))

    if model_exists:
        # Check files
        files = list(model_path.glob("*.safetensors"))
        config_exists = (model_path / "config.json").exists()
        tokenizer_exists = (model_path / "tokenizer.model").exists()

        checks.append(("Model weights (.safetensors)", len(files) > 0, f"{len(files)} weight files"))
        checks.append(("Config file (config.json)", config_exists, "config.json"))
        checks.append(("Tokenizer model", tokenizer_exists, "tokenizer.model"))

    # 2. Code updated
    loader_path = Path.home() / "Desktop" / "Apps" / "His Dark Materials" / "core" / "llm" / "deepseek_loader.py"
    if loader_path.exists():
        loader_code = loader_path.read_text()
        has_deepseek_r1 = "DeepSeek-R1-Distill-Qwen-14B" in loader_code
        checks.append(("deepseek_loader.py updated", has_deepseek_r1, "References new model"))

    ram_path = Path.home() / "Desktop" / "Apps" / "His Dark Materials" / "core" / "llm" / "ram_manager.py"
    if ram_path.exists():
        ram_code = ram_path.read_text()
        has_new_min = "DEEPSEEK_R1_14B_MIN = 13" in ram_code
        checks.append(("ram_manager.py updated", has_new_min, "13GB minimum set"))

    # 3. Tests exist
    test_pt = Path.home() / "Desktop" / "Apps" / "His Dark Materials" / "test_deepseek_portuguese.py"
    checks.append(("Portuguese test script exists", test_pt.exists(), str(test_pt.name)))

    # 4. Old models deleted
    old_8b = Path.home() / "mlx-models" / "Qwen3-8B-MLX-8bit"
    old_4b = Path.home() / "mlx-models" / "Qwen3-4B-Instruct-2507-4bit"
    checks.append(("Old Qwen3 8B deleted", not old_8b.exists(), "Space freed"))
    checks.append(("Old Qwen3 4B deleted", not old_4b.exists(), "Space freed"))

    # Print results
    print("\n📋 Verification Results:\n")
    all_pass = True
    for check_name, passed, detail in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        print(f"   → {detail}")
        if not passed:
            all_pass = False

    print("\n" + "=" * 70)
    if all_pass:
        print("✅ All checks passed! Ready to use DeepSeek-R1")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run: python test_deepseek_portuguese.py")
        print("2. Verify Portuguese language support")
        print("3. Verify reasoning capability")
        print("4. Integrate into Wisdom Council agents")
        return True
    else:
        print("❌ Some checks failed. See details above.")
        print("=" * 70)
        print("\nCommon issues:")
        print("• Model still downloading? Check: ls ~/mlx-models/DeepSeek-R1-Distill-Qwen-14B-MLX/")
        print("• Code not updated? Run download scripts again")
        print("• Space issues? Check: df -h ~/mlx-models/")
        return False

if __name__ == "__main__":
    result = verify()
    sys.exit(0 if result else 1)
