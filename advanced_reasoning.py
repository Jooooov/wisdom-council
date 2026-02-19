"""
Advanced Reasoning System - His Dark Materials Wisdom Council v3
================================================================
Phase 1: MCTS tree search (4 branches → score → expand top-2)
Phase 2: 4 themed agents (Lyra, Will, Mrs. Coulter, Iorek) + Meta-Daemon

Model: Qwen3-4B-4bit  (~2.3 GB, sequential CoT reasoning)
Target: MacBook Air M4, 16 GB RAM  (peak usage < 6 GB)

Run:
    python advanced_reasoning.py
    python advanced_reasoning.py --idea "your business idea" --type SaaS --budget "$50k"
    python advanced_reasoning.py --reset      (clear previous tree state)

Architecture:
    ┌──────────────────────────────────────────────┐
    │  MCTS Tree (MCTSTree)                        │
    │  ├─ Level 0: ROOT (business idea)            │
    │  ├─ Level 1: Lyra → 4 branches              │
    │  │           Will / Coulter / Iorek → score  │
    │  │           Prune weak → keep top-2         │
    │  ├─ Level 2: Expand top-2 → 4 sub-branches  │
    │  │           Score → prune → keep top-2      │
    │  └─ Level 3: (optional) deep expansion       │
    │                                              │
    │  Meta-Daemon: synthesises → GO / NO_GO       │
    └──────────────────────────────────────────────┘
    State persisted to ~/.mcts_reasoning/ between runs.
"""

import os
# Fix OpenMP duplicate lib conflict (numpy + mlx on macOS)
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.llm.ram_manager import RAMManager
from core.reasoning.mcts_tree import MCTSNode, MCTSTree
from core.reasoning.reasoning_agent import Qwen3Loader, ReasoningAgent
from core.reasoning.dynamic_router import DynamicRouter
from core.reasoning.reasoning_memory import ReasoningMemory


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------

class AdvancedReasoningSystem:
    """
    Orchestrates the full MCTS + agent reasoning pipeline.

    Designed to run entirely sequentially on a 16 GB M4 with Qwen3-4B-4bit.
    Tree state is saved to disk after each node so interrupted runs can resume.
    """

    def __init__(self, reset_tree: bool = False):
        self.ram_manager = RAMManager()
        self.llm_loader = Qwen3Loader(self.ram_manager)
        self.tree = MCTSTree()
        self.agent: Optional[ReasoningAgent] = None
        self.router = DynamicRouter()
        self.memory = ReasoningMemory()
        self.init_error: Optional[str] = None  # set when initialize() fails

        if reset_tree:
            self.tree.reset()

    # -----------------------------------------------------------------------
    # Initialisation
    # -----------------------------------------------------------------------

    async def initialize(self) -> bool:
        """Load Qwen3-4B and verify system readiness."""
        print("\n" + "=" * 70)
        print("🧭  ADVANCED REASONING SYSTEM")
        print("    His Dark Materials — Wisdom Council v3")
        print("    MCTS + Qwen3 (8B or 4B auto-selected) + Multi-Agent")
        print("=" * 70)

        # Show RAM status focused on Qwen3-4B requirements (not DeepSeek)
        self.ram_manager.refresh()
        avail = self.ram_manager.available_ram
        total = self.ram_manager.system_ram
        used  = total - avail
        print(f"\n  RAM:  {avail:.1f} GB free  /  {total:.0f} GB total  ({used:.1f} GB used)")
        selected_id, selected_name = self.llm_loader._select_model()
        print(f"  Model: {selected_name}  (auto-selected based on free RAM)")

        ok, msg = self.llm_loader.check_ram_availability()
        print(f"  {msg}")
        if not ok:
            self.init_error = "ram"
            print("\n  Tip: close browser tabs, IDEs, Slack, and other apps, then retry.")
            return False

        success = await self.llm_loader.load()
        if not success:
            self.init_error = "load"
            return False

        self.agent = ReasoningAgent(self.llm_loader)
        return True

    # -----------------------------------------------------------------------
    # Public entry point
    # -----------------------------------------------------------------------

    async def run_analysis(
        self,
        business_idea: str,
        business_type: str = "general",
        budget: str = "Unknown",
        reset: bool = False,
    ) -> Dict[str, Any]:
        """
        Run a full MCTS analysis and return structured JSON output.

        Args:
            business_idea:  The idea to analyse (free text).
            business_type:  Category e.g. "SaaS", "Marketplace", "B2B".
            budget:         Available budget string e.g. "$50k".
            reset:          If True, clear any previous tree state first.

        Returns:
            Dict with recommendation, confidence, best_path, financial_projection,
            key_risks, meta_daemon output, and the full MCTS tree.
        """
        if reset:
            self.tree.reset()

        print(f"\n{'='*70}")
        print(f"🎯  MCTS ANALYSIS")
        print(f"    Idea: {business_idea[:80]}")
        print(f"    Type: {business_type}  |  Budget: {budget}")
        print(f"{'='*70}\n")

        # Retrieve similar past analyses to inject as Lyra's context
        similar = self.memory.retrieve_similar(business_idea, business_type)
        past_context = self.memory.format_for_prompt(similar)
        if past_context:
            print(f"📚  Found {len(similar)} similar past analyse(s) — injecting as context.\n")

        # ── Root node ───────────────────────────────────────────────────────
        root = self.tree.create_root(business_idea)
        print(f"🌱  Root node created ({root.id})\n")

        # ── Level 1: Lyra generates branches ───────────────────────────────
        print("─" * 50)
        print("LEVEL 1 — Lyra: generating 4 reasoning branches")
        print("─" * 50)

        lyra_output = await self.agent.lyra_generate_branches(
            business_idea, depth=1, past_context=past_context
        )
        if not lyra_output or "branches" not in lyra_output:
            print("⚠️   Lyra returned no output — using fallback branches.")
            lyra_output = self._fallback_branches(business_idea)

        branches = lyra_output["branches"][: MCTSTree.BRANCHES_PER_NODE]
        print(f"\n  Generated {len(branches)} branch(es):\n")
        for b in branches:
            print(f"  [{b['label']}] {b['description'][:70]}")
        if lyra_output.get("reasoning_summary"):
            print(f"\n  Lyra's summary: {lyra_output['reasoning_summary'][:120]}")

        # Create Level-1 nodes
        level1_nodes: List[MCTSNode] = []
        for b in branches:
            node = self.tree.add_child(root, b["label"], b["description"])
            level1_nodes.append(node)

        # Simulate (score) every Level-1 node
        await self._simulate_nodes(level1_nodes, business_idea, budget)

        # Prune weak branches — keep top-2
        self.tree.prune_weak_branches(level1_nodes)
        top2_l1 = self.tree.select_top_k(level1_nodes)

        print(f"\n🏆  Top-2 after Level 1:")
        for n in top2_l1:
            print(f"   [{n.branch_label}] score={n.composite_score:.3f}  {n.description[:60]}")

        # ── Level 2: Expand top-2 ───────────────────────────────────────────
        if MCTSTree.MAX_DEPTH >= 2 and top2_l1:
            print(f"\n{'─'*50}")
            print("LEVEL 2 — Expanding top-2 branches")
            print("─" * 50)

            for parent in top2_l1:
                await self._expand_node(parent, business_idea, budget, depth=2)
                parent.is_expanded = True

            self.tree.save_state()

        # ── Level 3: Optional deep expansion ───────────────────────────────
        if MCTSTree.MAX_DEPTH >= 3 and top2_l1:
            for parent in top2_l1:
                l2_children = [
                    c for c in self.tree.get_children(parent)
                    if not c.is_pruned and c.is_evaluated
                ]
                best_l2 = self.tree.select_top_k(l2_children, k=1)
                if best_l2:
                    print(f"\n{'─'*50}")
                    print(f"LEVEL 3 — Deep expansion of [{best_l2[0].branch_label}]")
                    print("─" * 50)
                    await self._expand_node(best_l2[0], business_idea, budget, depth=3)

        # ── Meta-Daemon: final synthesis ────────────────────────────────────
        print(f"\n{'─'*50}")
        print("META-DAEMON — Synthesising all agent outputs")
        print("─" * 50)

        evaluated_summary = self._build_evaluated_summary()
        # Meta-Daemon already has the full branch analysis — it doesn't need the
        # manual-context preamble.  Extract only the core topic to save tokens.
        if "[Analysis topic]" in business_idea:
            meta_idea = business_idea.split("[Analysis topic]")[-1].strip()[:200]
        else:
            meta_idea = business_idea[:200]
        meta_output = await self.agent.meta_daemon_decide(meta_idea, evaluated_summary)

        if not meta_output:
            meta_output = {
                "decision": "NEEDS_MORE_INFO",
                "confidence": 0.5,
                "best_branch": "Unknown",
                "rationale": "Meta-Daemon LLM call returned no output.",
                "key_success_factors": [],
                "recommended_next_steps": [],
            }

        print(f"\n🔮  Decision:   {meta_output.get('decision')}")
        print(f"    Confidence: {meta_output.get('confidence', 0):.2f}")
        print(f"    Rationale:  {str(meta_output.get('rationale', ''))[:120]}")

        # ── Build output JSON ───────────────────────────────────────────────
        result = self.tree.build_json_output(business_idea)
        result["meta_daemon"] = meta_output

        # Store this analysis in memory for future runs
        best_path_nodes = self.tree.get_best_path()
        path_records = [
            {"agent": "MCTS", "thought": n.description, "score": n.composite_score}
            for n in best_path_nodes
        ]
        self.memory.store_analysis_result(
            business_idea=business_idea,
            business_type=business_type,
            reasoning_path=path_records,
            final_decision=meta_output.get("decision", "UNKNOWN"),
            confidence=meta_output.get("confidence", 0.0),
        )

        return result

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    async def _simulate_nodes(
        self, nodes: List[MCTSNode], business_idea: str, budget: str
    ):
        """Run Iorek → Marisa → Coram on each node, then score it."""
        for node in nodes:
            print(f"\n  ┌─ Simulating [{node.branch_label}]")
            print(f"  │  {node.description[:70]}")

            # Use DynamicRouter for RAM gating
            will_result = None
            coulter_result = None
            iorek_result = None

            tasks1 = [
                (
                    "Iorek",
                    lambda n=node: self.agent.iorek_model_financials(
                        n.description, business_idea, budget
                    ),
                ),
            ]
            step1 = await self.router.run_sequential(tasks1)
            iorek_result = step1.get("Iorek")
            node.iorek_financials = iorek_result or {}

            tasks2 = [
                (
                    "Marisa",
                    lambda n=node, i=node.iorek_financials: self.agent.marisa_assess_risks(
                        n.description, i
                    ),
                ),
            ]
            step2 = await self.router.run_sequential(tasks2)
            marisa_result = step2.get("Marisa")
            node.coulter_risks = marisa_result or {}

            tasks3 = [
                (
                    "Coram",
                    lambda n=node: self.agent.coram_validate(n.description, business_idea),
                ),
            ]
            step3 = await self.router.run_sequential(tasks3)
            coram_result = step3.get("Coram")
            node.will_assessment = coram_result or {}

            # Extract scores (default 0.5 if agent returned None)
            feasibility = float((coram_result or {}).get("feasibility_score", 0.5))
            risk = float((marisa_result or {}).get("risk_score", 0.5))
            financial = float((iorek_result or {}).get("financial_score", 0.5))

            self.tree.mark_evaluated(node, feasibility, risk, financial)

            verdict = (coram_result or {}).get("verdict", "?")
            print(
                f"  └─ Scores: feasibility={feasibility:.2f} | "
                f"risk={risk:.2f} | financial={financial:.2f} "
                f"→ composite={node.composite_score:.3f}  [{verdict}]"
            )

    async def _expand_node(
        self,
        parent: MCTSNode,
        business_idea: str,
        budget: str,
        depth: int,
    ):
        """Expand a node: Lyra generates sub-branches, then simulate each."""
        focused_idea = f"{business_idea} [focusing on: {parent.description[:100]}]"

        lyra_output = await self.agent.lyra_generate_branches(focused_idea, depth)
        if not lyra_output or "branches" not in lyra_output:
            print(f"  ⚠️   Lyra returned nothing for [{parent.branch_label}] expansion.")
            return

        sub_branches = lyra_output["branches"][: MCTSTree.BRANCHES_PER_NODE]
        child_nodes: List[MCTSNode] = []

        for b in sub_branches:
            label = f"{parent.branch_label}.{b['label']}"
            child = self.tree.add_child(parent, label, b["description"])
            child_nodes.append(child)
            print(f"    + [{label}] {b['description'][:60]}")

        await self._simulate_nodes(child_nodes, business_idea, budget)
        self.tree.prune_weak_branches(child_nodes)

        best = self.tree.select_top_k(child_nodes, k=1)
        if best:
            print(f"\n  🏆  Best sub-branch: [{best[0].branch_label}] score={best[0].composite_score:.3f}")

    def _build_evaluated_summary(self) -> List[Dict]:
        """Compact summary of all evaluated, non-pruned nodes for Meta-Daemon."""
        result = []
        for node in self.tree.nodes.values():
            if not node.is_evaluated or node.is_pruned or node.depth == 0:
                continue
            result.append(
                {
                    "branch": node.branch_label,
                    "description": node.description[:80],
                    "composite_score": node.composite_score,
                    "will_verdict": node.will_assessment.get("verdict", "?"),
                    "top_risk": (
                        (node.coulter_risks.get("risks") or [{}])[0].get("risk", "?")
                    ),
                    "roi_estimate": node.iorek_financials.get("roi_estimate", "?"),
                    "dev_cost": node.iorek_financials.get("dev_cost_estimate", "?"),
                }
            )
        return sorted(result, key=lambda x: x["composite_score"], reverse=True)

    @staticmethod
    def _fallback_branches(idea: str) -> Dict:
        """Fallback branches when Lyra's LLM call returns nothing."""
        return {
            "branches": [
                {
                    "label": "Branch A",
                    "description": f"Direct implementation — {idea}",
                    "key_assumption": "Straightforward path to MVP",
                    "confidence": 0.5,
                },
                {
                    "label": "Branch B",
                    "description": f"Phased rollout — {idea}",
                    "key_assumption": "Reduces initial investment risk",
                    "confidence": 0.5,
                },
                {
                    "label": "Branch C",
                    "description": f"Partnership / white-label — {idea}",
                    "key_assumption": "Leverage existing distribution",
                    "confidence": 0.5,
                },
                {
                    "label": "Branch D",
                    "description": f"B2B SaaS model — {idea}",
                    "key_assumption": "Enterprise contracts provide predictable revenue",
                    "confidence": 0.5,
                },
            ],
            "reasoning_summary": "Fallback branches (LLM call failed).",
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advanced MCTS Reasoning — His Dark Materials Wisdom Council v3"
    )
    parser.add_argument(
        "--idea",
        default=(
            "AI-powered tool for analyzing Reddit discussions in real-time, "
            "generating market insights for crypto traders"
        ),
        help="Business idea to analyse",
    )
    parser.add_argument("--type", default="SaaS", help="Business type (SaaS, Marketplace, B2B…)")
    parser.add_argument("--budget", default="$50,000", help="Available budget")
    parser.add_argument("--reset", action="store_true", help="Clear previous tree state")
    parser.add_argument("--output", default="outputs/mcts_analysis_result.json", help="Output file")
    return parser.parse_args()


async def main():
    args = _parse_args()

    system = AdvancedReasoningSystem(reset_tree=args.reset)

    if not await system.initialize():
        print("\n❌ System failed to initialise. Exiting.")
        sys.exit(1)

    result = await system.run_analysis(
        business_idea=args.idea,
        business_type=args.type,
        budget=args.budget,
        reset=args.reset,
    )

    # Print final summary
    meta = result.get("meta_daemon", {})
    print(f"\n{'='*70}")
    print("✅  ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"   Decision:    {meta.get('decision')}")
    print(f"   Confidence:  {meta.get('confidence', 0):.2f}")
    print(f"   Best path:   {' → '.join(result.get('best_path', []))}")

    if meta.get("recommended_next_steps"):
        print("\n   Next steps:")
        for step in meta["recommended_next_steps"]:
            print(f"     ➜ {step}")

    # Save JSON output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n   Full JSON saved → {out_path}")
    print(f"{'='*70}\n")

    system.tree.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
