"""
MCTS Tree - Monte Carlo Tree Search for reasoning exploration.

Algorithm:
    1. ROOT: business idea
    2. EXPAND: Lyra generates 4 branches per node
    3. SIMULATE: Will + Mrs. Coulter + Iorek score each branch (0-1)
    4. BACKPROPAGATE: top-2 branches kept, rest pruned
    5. REPEAT up to max_depth levels

State is saved to disk between iterations so long runs don't bloat RAM.
Directory: ~/.mcts_reasoning/
"""

import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

@dataclass
class MCTSNode:
    """A single node in the MCTS reasoning tree."""

    id: str
    depth: int
    parent_id: Optional[str]
    branch_label: str       # e.g. "Branch A", "Branch A.Branch B"
    description: str        # The reasoning approach for this branch

    # Agent scores (0.0 - 1.0)
    feasibility_score: float = 0.0
    risk_score: float = 0.0          # 1.0 = low risk (good), 0.0 = high risk
    financial_score: float = 0.0
    composite_score: float = 0.0     # (feasibility + risk + financial) / 3

    # Status flags
    is_evaluated: bool = False
    is_pruned: bool = False
    is_expanded: bool = False

    # Filled during simulation phase
    will_assessment: Dict[str, Any] = field(default_factory=dict)
    coulter_risks: Dict[str, Any] = field(default_factory=dict)
    iorek_financials: Dict[str, Any] = field(default_factory=dict)

    # Children node IDs
    children_ids: List[str] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    evaluated_at: Optional[str] = None

    def compute_composite_score(self) -> float:
        """Recompute and store composite score from the three agent scores."""
        self.composite_score = round(
            (self.feasibility_score + self.risk_score + self.financial_score) / 3, 3
        )
        return self.composite_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "depth": self.depth,
            "parent_id": self.parent_id,
            "branch_label": self.branch_label,
            "description": self.description,
            "scores": {
                "feasibility": self.feasibility_score,
                "risk_mitigation": self.risk_score,
                "financial": self.financial_score,
                "composite": self.composite_score,
            },
            "status": {
                "is_evaluated": self.is_evaluated,
                "is_pruned": self.is_pruned,
                "is_expanded": self.is_expanded,
            },
            "agent_outputs": {
                "will_assessment": self.will_assessment,
                "coulter_risks": self.coulter_risks,
                "iorek_financials": self.iorek_financials,
            },
            "children_ids": self.children_ids,
            "created_at": self.created_at,
            "evaluated_at": self.evaluated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MCTSNode":
        node = cls(
            id=d["id"],
            depth=d["depth"],
            parent_id=d.get("parent_id"),
            branch_label=d["branch_label"],
            description=d["description"],
        )
        scores = d.get("scores", {})
        node.feasibility_score = scores.get("feasibility", 0.0)
        node.risk_score = scores.get("risk_mitigation", 0.0)
        node.financial_score = scores.get("financial", 0.0)
        node.composite_score = scores.get("composite", 0.0)

        status = d.get("status", {})
        node.is_evaluated = status.get("is_evaluated", False)
        node.is_pruned = status.get("is_pruned", False)
        node.is_expanded = status.get("is_expanded", False)

        outputs = d.get("agent_outputs", {})
        node.will_assessment = outputs.get("will_assessment", {})
        node.coulter_risks = outputs.get("coulter_risks", {})
        node.iorek_financials = outputs.get("iorek_financials", {})

        node.children_ids = d.get("children_ids", [])
        node.created_at = d.get("created_at", "")
        node.evaluated_at = d.get("evaluated_at")
        return node


# ---------------------------------------------------------------------------
# Tree
# ---------------------------------------------------------------------------

class MCTSTree:
    """
    Monte Carlo Tree Search for multi-agent reasoning.

    Configuration:
        BRANCHES_PER_NODE = 4   Lyra generates 4 approaches
        TOP_K_EXPAND      = 2   Expand only the 2 highest-scoring branches
        MAX_DEPTH         = 3   Tree depth (root = 0)

    Disk persistence:
        ~/.mcts_reasoning/tree_structure.json
    """

    BRANCHES_PER_NODE = 4
    TOP_K_EXPAND = 2
    MAX_DEPTH = 3

    def __init__(self, state_dir: str = None):
        if not state_dir:
            state_dir = str(Path.home() / ".mcts_reasoning")

        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.nodes: Dict[str, MCTSNode] = {}
        self.root_id: Optional[str] = None
        self._load_state()

    # -----------------------------------------------------------------------
    # Persistence
    # -----------------------------------------------------------------------

    @property
    def _tree_file(self) -> Path:
        return self.state_dir / "tree_structure.json"

    def _load_state(self):
        """Load tree from disk (resumes interrupted runs)."""
        if not self._tree_file.exists():
            return
        try:
            data = json.loads(self._tree_file.read_text())
            self.root_id = data.get("root_id")
            for node_dict in data.get("nodes", []):
                node = MCTSNode.from_dict(node_dict)
                self.nodes[node.id] = node
        except Exception:
            pass  # Start fresh if file is corrupted

    def save_state(self):
        """Write current tree to disk."""
        data = {
            "root_id": self.root_id,
            "saved_at": datetime.now().isoformat(),
            "nodes": [n.to_dict() for n in self.nodes.values()],
        }
        self._tree_file.write_text(json.dumps(data, indent=2))

    def reset(self):
        """Clear tree and remove disk state."""
        self.nodes.clear()
        self.root_id = None
        if self._tree_file.exists():
            self._tree_file.unlink()

    # -----------------------------------------------------------------------
    # Node management
    # -----------------------------------------------------------------------

    def _new_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def create_root(self, idea: str) -> MCTSNode:
        """Create the root node from the business idea."""
        node = MCTSNode(
            id=self._new_id(),
            depth=0,
            parent_id=None,
            branch_label="ROOT",
            description=idea,
        )
        self.nodes[node.id] = node
        self.root_id = node.id
        self.save_state()
        return node

    def add_child(self, parent: MCTSNode, branch_label: str, description: str) -> MCTSNode:
        """Add a child node to an existing parent."""
        node = MCTSNode(
            id=self._new_id(),
            depth=parent.depth + 1,
            parent_id=parent.id,
            branch_label=branch_label,
            description=description,
        )
        parent.children_ids.append(node.id)
        self.nodes[node.id] = node
        self.save_state()
        return node

    def get_node(self, node_id: str) -> Optional[MCTSNode]:
        return self.nodes.get(node_id)

    def get_children(self, node: MCTSNode) -> List[MCTSNode]:
        return [self.nodes[cid] for cid in node.children_ids if cid in self.nodes]

    # -----------------------------------------------------------------------
    # MCTS logic
    # -----------------------------------------------------------------------

    def mark_evaluated(
        self,
        node: MCTSNode,
        feasibility: float,
        risk: float,
        financial: float,
    ):
        """Record agent scores and recompute composite."""
        node.feasibility_score = round(max(0.0, min(1.0, feasibility)), 3)
        node.risk_score = round(max(0.0, min(1.0, risk)), 3)
        node.financial_score = round(max(0.0, min(1.0, financial)), 3)
        node.is_evaluated = True
        node.evaluated_at = datetime.now().isoformat()
        node.compute_composite_score()
        self.save_state()

    def select_top_k(self, nodes: List[MCTSNode], k: int = TOP_K_EXPAND) -> List[MCTSNode]:
        """Return top-k evaluated, non-pruned nodes by composite score."""
        evaluated = [n for n in nodes if n.is_evaluated and not n.is_pruned]
        return sorted(evaluated, key=lambda n: n.composite_score, reverse=True)[:k]

    def prune_weak_branches(self, siblings: List[MCTSNode]):
        """Mark all but the top-k siblings as pruned to save RAM."""
        top_ids = {n.id for n in self.select_top_k(siblings, self.TOP_K_EXPAND)}
        for node in siblings:
            if node.id not in top_ids:
                node.is_pruned = True
        self.save_state()

    def get_best_path(self) -> List[MCTSNode]:
        """Trace the highest-scoring path from root to deepest active leaf."""
        if not self.root_id:
            return []
        path = []
        current = self.nodes.get(self.root_id)
        while current:
            path.append(current)
            active_children = [
                c for c in self.get_children(current)
                if not c.is_pruned and c.is_evaluated
            ]
            if not active_children:
                break
            current = max(active_children, key=lambda n: n.composite_score)
        return path

    # -----------------------------------------------------------------------
    # Output
    # -----------------------------------------------------------------------

    def build_json_output(self, business_idea: str) -> Dict[str, Any]:
        """Build the final structured JSON report."""
        best_path = self.get_best_path()
        best_leaf = best_path[-1] if len(best_path) > 1 else None

        return {
            "business_idea": business_idea,
            "generated_at": datetime.now().isoformat(),
            "mcts_config": {
                "max_depth": self.MAX_DEPTH,
                "branches_per_node": self.BRANCHES_PER_NODE,
                "top_k_expanded": self.TOP_K_EXPAND,
            },
            "confidence": best_leaf.composite_score if best_leaf else 0.0,
            "best_path": [n.branch_label for n in best_path],
            "financial_projection": best_leaf.iorek_financials if best_leaf else {},
            "key_risks": (
                best_leaf.coulter_risks.get("risks", []) if best_leaf else []
            ),
            "full_tree": [n.to_dict() for n in self.nodes.values()],
        }

    def print_summary(self):
        """Print a human-readable tree summary."""
        print("\n📊 MCTS TREE SUMMARY")
        print("=" * 60)
        for node in self.nodes.values():
            indent = "  " * node.depth
            status = "✂️ pruned" if node.is_pruned else (
                f"score={node.composite_score:.3f}" if node.is_evaluated else "pending"
            )
            print(f"{indent}[{node.branch_label}] {node.description[:50]}... | {status}")
