"""
Reasoning Memory - Stores and retrieves MCTS reasoning paths.

Lightweight keyword-matching approach — no vector DB needed.
Designed for the 16GB M4 constraint: zero RAM overhead at retrieval time.

Storage layout:
    ~/.mcts_reasoning/
    ├── explored_paths.jsonl     # All reasoning paths (append-only log)
    └── node_scores.json         # Quick node_id → composite_score index

Retrieval:
    Keyword overlap between the current query and past `input_description` fields,
    boosted by matching `business_type`.  Filters out low-confidence records.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ReasoningMemory:
    """
    Stores successful MCTS reasoning paths and retrieves similar ones.

    Example — store after a completed analysis::

        memory.store_analysis_result(
            business_idea="AI Reddit analytics for crypto traders",
            business_type="SaaS",
            reasoning_path=[
                {"agent": "Lyra", "thought": "Generated 4 branches"},
                {"agent": "Will",  "verdict": "FEASIBLE"},
                {"agent": "Iorek", "roi_3y": 2.8, "confidence": 0.85},
            ],
            final_decision="GO",
            confidence=0.91,
        )

    Example — retrieve before a new analysis::

        similar = memory.retrieve_similar("crypto market analysis tool", "SaaS")
        past_context = memory.format_for_prompt(similar)
        # Inject `past_context` into Lyra's prompt.
    """

    def __init__(self, state_dir: str = None):
        if not state_dir:
            state_dir = str(Path.home() / ".mcts_reasoning")

        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self._paths_file = self.state_dir / "explored_paths.jsonl"
        self._scores_file = self.state_dir / "node_scores.json"
        self._scores_index: Dict[str, float] = self._load_scores()

    # -----------------------------------------------------------------------
    # Persistence helpers
    # -----------------------------------------------------------------------

    def _load_scores(self) -> Dict[str, float]:
        if self._scores_file.exists():
            try:
                return json.loads(self._scores_file.read_text())
            except Exception:
                pass
        return {}

    def _save_scores(self):
        self._scores_file.write_text(json.dumps(self._scores_index, indent=2))

    def _load_all_paths(self) -> List[Dict]:
        if not self._paths_file.exists():
            return []
        records = []
        with open(self._paths_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
        return records

    # -----------------------------------------------------------------------
    # Store
    # -----------------------------------------------------------------------

    def store_path(self, path_record: Dict[str, Any]):
        """Append a raw reasoning path record to the JSONL log."""
        record = {"stored_at": datetime.now().isoformat(), **path_record}
        with open(self._paths_file, "a") as f:
            f.write(json.dumps(record) + "\n")

        # Update scores index
        node_id = path_record.get("node_id")
        score = path_record.get("composite_score")
        if node_id and score is not None:
            self._scores_index[node_id] = score
            self._save_scores()

    def store_analysis_result(
        self,
        business_idea: str,
        business_type: str,
        reasoning_path: List[Dict],
        final_decision: str,
        confidence: float,
    ):
        """
        Store a complete analysis result for future retrieval.

        Args:
            business_idea:   The original business idea string.
            business_type:   e.g. "SaaS", "Marketplace", "B2B"
            reasoning_path:  List of {"agent": ..., "thought": ..., ...} dicts.
            final_decision:  "GO", "NO_GO", or "NEEDS_MORE_INFO"
            confidence:      0.0 – 1.0
        """
        record = {
            "step_id": f"mcts_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "business_type": business_type,
            "input_description": business_idea,
            "reasoning_path": reasoning_path,
            "final_decision": final_decision,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
        }
        self.store_path(record)
        logger.info("Stored analysis result: %s (confidence=%.2f)", final_decision, confidence)

    # -----------------------------------------------------------------------
    # Retrieve
    # -----------------------------------------------------------------------

    def retrieve_similar(
        self,
        query: str,
        business_type: str = "",
        min_confidence: float = 0.65,
        limit: int = 3,
    ) -> List[Dict]:
        """
        Retrieve past reasoning paths similar to the current query.

        Scoring:
            +2.0  exact business_type match
            +0.5  per overlapping word between query and past input_description
            Filter: records below min_confidence are ignored.

        Returns:
            Top `limit` records sorted by relevance score (highest first).
        """
        records = self._load_all_paths()
        if not records:
            return []

        query_words = set(query.lower().split())
        scored = []

        for rec in records:
            # Confidence gate
            if rec.get("confidence", 0.0) < min_confidence:
                continue

            relevance = 0.0

            # Business type match (strong signal)
            if business_type and rec.get("business_type", "").lower() == business_type.lower():
                relevance += 2.0

            # Keyword overlap
            desc_words = set(rec.get("input_description", "").lower().split())
            relevance += len(query_words & desc_words) * 0.5

            if relevance > 0:
                scored.append((relevance, rec))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored[:limit]]

    def format_for_prompt(self, similar_paths: List[Dict]) -> str:
        """
        Format retrieved paths as a concise prompt injection for Lyra.

        Keeps it short to avoid eating into Qwen3-4B's 4k context budget.
        """
        if not similar_paths:
            return ""

        lines = ["[Past analyses — use as reference, not strict rules]"]
        for i, rec in enumerate(similar_paths, 1):
            btype = rec.get("business_type", "?")
            decision = rec.get("final_decision", "?")
            conf = rec.get("confidence", 0.0)
            lines.append(f"\n[{i}] {btype} → {decision} (confidence {conf:.2f})")

            for step in rec.get("reasoning_path", [])[:3]:
                agent = step.get("agent", "?")
                thought = step.get("thought", step.get("verdict", ""))[:80]
                lines.append(f"    {agent}: {thought}")

        return "\n".join(lines)

    # -----------------------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """Return basic statistics about stored memory."""
        records = self._load_all_paths()
        decisions = [r.get("final_decision", "?") for r in records]
        return {
            "total_analyses": len(records),
            "decisions": {d: decisions.count(d) for d in set(decisions)},
            "node_scores_indexed": len(self._scores_index),
            "storage_path": str(self.state_dir),
        }
