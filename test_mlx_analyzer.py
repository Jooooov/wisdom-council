#!/usr/bin/env python3
"""
Test MLX Analyzer Integration
Verify semantic code analysis works with Qwen3 8B
"""
import asyncio
import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).parent))

from core.llm import create_ram_manager, create_mlx_loader, MLXAnalyzer


async def main():
    """Test MLX analyzer with sample code."""
    print("=" * 70)
    print("🔬 MLX Analyzer Test - Semantic Code Analysis")
    print("=" * 70)

    # Check system
    ram_manager = create_ram_manager()
    loader = create_mlx_loader(ram_manager)

    print(f"\n📋 System Status:")
    print(f"  Available RAM: {ram_manager.available_ram:.1f}GB")
    print(f"  Model exists: {loader.model_exists()}")
    print(f"  Can load: {loader.can_load()}")

    if not loader.can_load():
        print(f"\n❌ Cannot load model - insufficient resources")
        return False

    # Create sample Python code file
    sample_code = '''"""
Sample module for testing analysis
"""
import os
import subprocess

def analyze_file(path):
    """Analyze a file."""
    with open(path, 'r') as f:
        content = f.read()

    # TODO: Add error handling
    result = subprocess.call(f"cat {path}")  # Security issue: command injection

    # Hardcoded path
    db_path = "/usr/local/db/data.sqlite"

    return result

class DataProcessor:
    def __init__(self):
        self.data = []

    def process(self, items):
        try:
            for item in items:
                self.data.append(item)
        except:  # Bare exception - bad practice
            pass
'''

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(sample_code)
        temp_file = f.name

    try:
        print(f"\n🚀 Loading Qwen3 8B model...")
        success = await loader.load()

        if not success:
            print(f"❌ Failed to load model")
            return False

        print(f"✅ Model loaded successfully!")

        # Analyze code
        print(f"\n🔍 Analyzing code file...")
        analyzer = MLXAnalyzer(loader)
        analysis = await analyzer.analyze_code_file(temp_file)

        if "error" in analysis:
            print(f"❌ Analysis error: {analysis['error']}")
            return False

        print(f"\n📊 Analysis Results:")
        print(f"  File: {analysis['file_name']}")
        print(f"  Size: {analysis['size']} bytes")
        print(f"\n  Analysis:")
        print(f"  {analysis['analysis']}")

        # Test project analysis
        print(f"\n📁 Testing project analysis...")

        # Create temp project
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create sample files
            (project_dir / "main.py").write_text(sample_code)
            (project_dir / "utils.py").write_text("""
def helper():
    pass

class Utility:
    def method(self):
        return None
""")
            (project_dir / "README.md").write_text("# Test Project\nA test project for analysis")

            print(f"  Analyzing project at {project_dir}")
            project_analysis = await analyzer.analyze_project(str(project_dir), "test-project")

            print(f"\n  Project Analysis Results:")
            print(f"  Files analyzed: {len(project_analysis['files_analyzed'])}")
            for file_analysis in project_analysis['files_analyzed']:
                if "error" not in file_analysis:
                    print(f"    • {file_analysis['file_name']}: {file_analysis['analysis'][:60]}...")

            if project_analysis['analysis_summary']:
                print(f"\n  Summary:")
                print(f"  {project_analysis['analysis_summary']}")

        print(f"\n✅ Analysis test completed successfully!")
        return True

    finally:
        # Cleanup
        loader.unload()
        Path(temp_file).unlink(missing_ok=True)
        print(f"\n✅ Cleanup completed")


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
