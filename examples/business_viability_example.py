"""
End-to-End Example: Business Viability Analysis
================================================
His Dark Materials Advanced Reasoning System

Use case: "AI-powered Reddit analytics tool for crypto traders"
Constraints: $50k budget, 2-3 person team, 6-month MVP timeline

Run from project root:
    python examples/business_viability_example.py

What this demonstrates:
    1. Lyra generates 4 strategic approaches
    2. Each approach scored by Will (feasibility), Mrs. Coulter (risk), Iorek (ROI)
    3. Top-2 branches expanded 2 more levels deep
    4. Meta-Daemon synthesises → GO / NO_GO + next steps
    5. Full JSON output saved to outputs/business_viability_result.json
    6. Analysis stored in ~/.mcts_reasoning/ for future reference

Expected output (Qwen3-4B, ~30-60 min on M4 Air):
    {
      "meta_daemon": {
        "decision": "GO",
        "confidence": 0.88,
        "best_branch": "Branch C.Branch B",
        "recommended_next_steps": ["Validate with 20 beta traders", ...]
      },
      "best_path": ["ROOT", "Branch C", "Branch C.Branch B"],
      "confidence": 0.88,
      ...
    }
"""

import asyncio
import json
import sys
from pathlib import Path

# Make sure we can import from project root regardless of where the script runs
sys.path.insert(0, str(Path(__file__).parent.parent))

from advanced_reasoning import AdvancedReasoningSystem


# ---------------------------------------------------------------------------
# Business case definition
# ---------------------------------------------------------------------------

BUSINESS_IDEA = (
    "AI-powered tool for analyzing Reddit discussions in real-time, "
    "generating market insights for crypto traders. "
    "Monitors r/CryptoCurrency, r/Bitcoin, r/ethereum and other subreddits, "
    "detects sentiment shifts and emerging narratives, then delivers "
    "actionable signals via a web dashboard and Telegram bot."
)

BUSINESS_TYPE = "SaaS"

BUDGET = "$50,000"

OUTPUT_PATH = Path("outputs/business_viability_result.json")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def run_example():
    print("\n" + "=" * 70)
    print("📊  EXAMPLE: Business Viability Analysis")
    print("    His Dark Materials — Advanced Reasoning System")
    print("=" * 70)
    print(f"\nIdea:\n  {BUSINESS_IDEA[:120]}...")
    print(f"\nBusiness type: {BUSINESS_TYPE}")
    print(f"Budget:        {BUDGET}")

    # Initialise system (loads Qwen3-4B-4bit)
    system = AdvancedReasoningSystem(reset_tree=True)

    if not await system.initialize():
        print("\n❌ System failed to initialise.")
        print("   Check that mlx-lm is installed: pip install mlx-lm")
        print("   And that you have at least 3.5 GB of free RAM.")
        return

    # Run analysis
    result = await system.run_analysis(
        business_idea=BUSINESS_IDEA,
        business_type=BUSINESS_TYPE,
        budget=BUDGET,
        reset=True,
    )

    # ── Print human-readable summary ────────────────────────────────────────
    meta = result.get("meta_daemon", {})

    print("\n" + "=" * 70)
    print("📋  FINAL REPORT")
    print("=" * 70)

    decision = meta.get("decision", "?")
    confidence = meta.get("confidence", 0.0)
    decision_icon = {"GO": "✅", "NO_GO": "❌", "NEEDS_MORE_INFO": "⚠️"}.get(decision, "❓")

    print(f"\n{decision_icon}  Decision:    {decision}")
    print(f"    Confidence:  {confidence:.2f} / 1.00")
    print(f"    Best branch: {meta.get('best_branch', '?')}")
    print(f"    Best path:   {' → '.join(result.get('best_path', []))}")

    rationale = meta.get("rationale", "")
    if rationale:
        print(f"\n    Rationale:\n    {rationale[:300]}")

    success_factors = meta.get("key_success_factors", [])
    if success_factors:
        print("\n    Key success factors:")
        for f in success_factors:
            print(f"      • {f}")

    next_steps = meta.get("recommended_next_steps", [])
    if next_steps:
        print("\n    Recommended next steps:")
        for step in next_steps:
            print(f"      ➜ {step}")

    # Financial projection from best leaf
    fin = result.get("financial_projection", {})
    if fin:
        print("\n    Financial projection:")
        rev = fin.get("revenue_projection", {})
        if rev:
            for year, value in rev.items():
                print(f"      {year}: {value}")
        roi = fin.get("roi_estimate")
        if roi is not None:
            print(f"      ROI estimate: {roi:.1f}×")
        dev_cost = fin.get("dev_cost_estimate")
        if dev_cost:
            print(f"      Dev cost:     {dev_cost}")

    # Key risks from best leaf
    risks = result.get("key_risks", [])
    if risks:
        print("\n    Key risks:")
        for risk in risks[:3]:
            if isinstance(risk, dict):
                r = risk.get("risk", "")
                m = risk.get("mitigation", "")
                lh = risk.get("likelihood", "?")
                print(f"      ⚠️  {r}  (likelihood={lh}, mitigation: {m[:60]})")
            else:
                print(f"      ⚠️  {risk}")

    # ── Save JSON ────────────────────────────────────────────────────────────
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n💾  Full JSON saved → {OUTPUT_PATH}")

    # Print MCTS tree summary
    system.tree.print_summary()

    # Memory stats
    stats = system.memory.get_stats()
    print(f"\n📚  Memory: {stats['total_analyses']} analyses stored in {stats['storage_path']}")


if __name__ == "__main__":
    asyncio.run(run_example())
