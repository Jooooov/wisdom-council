#!/usr/bin/env python3
"""
Examples of how to use Mary Malone for tool research
"""

from run import WisdomCouncil
import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))


def example_1_show_context():
    """Example 1: Show Mary's research context."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Show Mary's Research Context")
    print("="*70)

    council = WisdomCouncil()
    council.mary_show_context()


def example_2_start_research():
    """Example 2: Start a research session."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Start a Research Session")
    print("="*70)

    council = WisdomCouncil()
    session = council.mary_research("Python web frameworks 2026")
    print(f"Session started: {session['id']}")


def example_3_add_tools():
    """Example 3: Add discovered tools."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Add Discovered Tools")
    print("="*70)

    council = WisdomCouncil()

    # FastAPI
    council.mary_add_tool(
        name="FastAPI",
        category="APIs",
        summary="Modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard type hints",
        relevant_agents=["Marisa", "Iorek", "Coram"],
        source="https://fastapi.tiangolo.com"
    )

    # Django
    council.mary_add_tool(
        name="Django 5.1",
        category="Frameworks",
        summary="The web framework for perfectionists with deadlines. Batteries-included framework for web development.",
        relevant_agents=["Marisa", "Iorek", "Serafina"],
        source="https://www.djangoproject.com"
    )

    # Pydantic
    council.mary_add_tool(
        name="Pydantic V2",
        category="Libraries",
        summary="Data validation using Python type annotations. Rewritten in Rust for better performance.",
        relevant_agents=["Lyra", "Marisa", "Coram"],
        source="https://docs.pydantic.dev/latest/"
    )

    # Langchain
    council.mary_add_tool(
        name="LangChain",
        category="AI/ML",
        summary="Framework for developing applications powered by large language models. Integrates with multiple LLM providers.",
        relevant_agents=["Serafina", "Lyra", "Marisa"],
        source="https://python.langchain.com/docs/get_started/introduction"
    )

    print("\n✅ Tools added to Mary's database")


def example_4_show_tools():
    """Example 4: Show discovered tools."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Show Discovered Tools")
    print("="*70)

    council = WisdomCouncil()

    # First add some tools
    council.mary_add_tool(
        name="FastAPI",
        category="APIs",
        summary="Modern Python web framework",
        relevant_agents=["Marisa", "Iorek"],
        source="https://fastapi.tiangolo.com"
    )

    # Then show them
    council.mary_show_tools()


def example_5_update_agents_md():
    """Example 5: Update agents.md file."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Update agents.md")
    print("="*70)

    council = WisdomCouncil()

    # Add a tool first
    council.mary_add_tool(
        name="Test Tool",
        category="Testing",
        summary="Example tool for documentation",
        relevant_agents=["Coram"],
        source="https://example.com"
    )

    # Update agents.md
    council.mary_update_agents_md()


def example_6_full_workflow():
    """Example 6: Full Mary workflow."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Full Mary Workflow")
    print("="*70)

    council = WisdomCouncil()

    # Step 1: Show context
    print("\n📅 Step 1: Mary's Current Context")
    print("-" * 70)
    council.mary_show_context()

    # Step 2: Start research
    print("\n🔍 Step 2: Start Research Session")
    print("-" * 70)
    session = council.mary_research("Python async frameworks 2026")

    # Step 3: Add discovered tools
    print("\n🔧 Step 3: Add Discovered Tools")
    print("-" * 70)
    council.mary_add_tool(
        name="FastAPI",
        category="APIs",
        summary="Modern async Python web framework",
        relevant_agents=["Marisa", "Iorek", "Lyra"],
        source="https://fastapi.tiangolo.com"
    )

    council.mary_add_tool(
        name="asyncio",
        category="Libraries",
        summary="Python's built-in async framework",
        relevant_agents=["Marisa", "Coram"],
        source="https://docs.python.org/3/library/asyncio.html"
    )

    # Step 4: Show tools
    print("\n📚 Step 4: Mary's Tool Database")
    print("-" * 70)
    council.mary_show_tools()

    # Step 5: Update agents.md
    print("\n📝 Step 5: Update agents.md")
    print("-" * 70)
    council.mary_update_agents_md()

    # Step 6: Sync to Obsidian
    print("\n🔗 Step 6: Sync to Obsidian Vault")
    print("-" * 70)
    council.mary_sync_obsidian()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mary Malone Research Examples")
    parser.add_argument(
        "--example",
        type=int,
        default=6,
        help="Which example to run (1-6, default: 6 - full workflow)"
    )

    args = parser.parse_args()

    examples = {
        1: example_1_show_context,
        2: example_2_start_research,
        3: example_3_add_tools,
        4: example_4_show_tools,
        5: example_5_update_agents_md,
        6: example_6_full_workflow,
    }

    if args.example in examples:
        examples[args.example]()
    else:
        print(f"❌ Invalid example: {args.example}")
        print("Available examples: 1-6")
        print("\nUsage:")
        print("  python mary_research_examples.py --example 1")
        print("  python mary_research_examples.py --example 6  # Full workflow")
