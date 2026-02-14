#!/usr/bin/env python3
"""
RAM Guardian - Check RAM before using DeepSeek-R1
Run this script BEFORE doing any analysis!
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.llm import create_ram_manager, create_mlx_loader


def main():
    """Check RAM status and model readiness."""
    print("=" * 70)
    print("🛡️  RAM GUARDIAN - DeepSeek-R1 Pre-Check")
    print("=" * 70)

    ram = create_ram_manager()
    loader = create_mlx_loader(ram)

    # Check 1: Model exists
    print("\n📋 Check 1: Model Files")
    if loader.model_exists():
        print("✅ Model files exist")
    else:
        print("❌ Model files NOT found!")
        print(f"   Expected at: {loader.model_path}")
        return False

    # Check 2: RAM availability
    print("\n📊 Check 2: RAM Availability")
    can_load, message = loader.check_ram_availability()
    print(message)

    if not can_load:
        print("\n" + "!" * 70)
        print("🚫 CANNOT PROCEED - INSUFFICIENT RAM")
        print("!" * 70)
        print("\n⚠️  Please close other applications:")
        print("   • Browser tabs (especially YouTube, etc.)")
        print("   • Slack, Discord, Teams")
        print("   • Email clients")
        print("   • IDEs, text editors, Dev tools")
        print("   • Streaming apps (Netflix, Spotify)")
        print("   • Video conferencing apps")
        print("\nThen restart and try again.")
        return False

    # Check 3: Detailed RAM status
    print("\n📈 Detailed RAM Status")
    ram.print_status()

    # Check 4: Model loading simulation
    print("\n🔧 Check 3: Model Loading Test")
    status = loader.get_status()
    print(f"✅ Model: {status['model_name']}")
    print(f"✅ Path exists: {status['model_exists']}")
    print(f"✅ Can load: {status['can_load']}")

    # Final verdict
    print("\n" + "=" * 70)
    if can_load and status['can_load']:
        print("✅ ALL CHECKS PASSED - Ready to use DeepSeek-R1!")
        print("=" * 70)
        print("\nYou can now:")
        print("  1. Run your analysis scripts")
        print("  2. Use Wisdom Council agents")
        print("  3. Call loader.load() and loader.generate()")
        print("\n⚠️  Keep monitoring RAM during use:")
        print("     If it drops below 2GB, generation may fail")
        return True
    else:
        print("❌ SOME CHECKS FAILED - Do NOT proceed!")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
