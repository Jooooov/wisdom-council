"""
Reasoning Agent + Qwen3 Loader

Qwen3Loader  - Auto-selects best Qwen3 model based on available RAM.
               Models are loaded from ~/Desktop/apps/MLX/ (local only).

               • Qwen3-8B-4bit  (~4.5 GB)  if RAM ≥ 5.5 GB  — better reasoning
               • Qwen3-4B-4bit  (~2.3 GB)  if RAM < 5.5 GB  — always fits

ReasoningAgent - Drives long chain-of-thought reasoning for each themed agent:
    - Lyra (Exploradora)   : generates 4 creative branches
    - Will (Executor)      : validates practical feasibility
    - Mrs. Coulter (Crítica): adversarial risk analysis
    - Iorek (Analista)     : financial modeling
    - Meta-Daemon          : synthesizes all agents → final decision

Qwen3 CoT format:
    Uses <|im_start|>...<|im_end|> chat template.
    Qwen3 emits <think>...</think> blocks before the answer.
    We strip those and extract the first valid JSON object.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Local model store — all apps share this folder
MLX_STORE = Path.home() / "Desktop" / "apps" / "MLX"
QWEN3_8B_PATH = MLX_STORE / "Qwen3-8B-4bit"
QWEN3_4B_PATH = MLX_STORE / "Qwen3-4B-4bit"

# RAM thresholds (GB)
QWEN3_8B_MIN_RAM_GB = 5.5   # need this much free to load the 8B model
QWEN3_4B_MIN_RAM_GB = 3.5   # hard minimum for the 4B model


# ---------------------------------------------------------------------------
# Model loader
# ---------------------------------------------------------------------------

class Qwen3Loader:
    """
    MLX loader — loads Qwen3 models from ~/Desktop/apps/MLX/.

    Selection logic (based on free RAM at load time):
      RAM ≥ 5.5 GB → Qwen3-8B-4bit  (better reasoning quality)
      RAM < 5.5 GB → Qwen3-4B-4bit  (always fits, safe default)

    No internet download — models must exist in ~/Desktop/apps/MLX/.
    """

    def __init__(self, ram_manager: Any):
        self.ram_manager = ram_manager
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.model_name = "Qwen3-4B-4bit"  # updated after successful load
        self._model_path = QWEN3_4B_PATH   # updated after successful load

    def _select_model(self) -> tuple[Path, str]:
        """Return (local_path, display_name) based on current free RAM."""
        self.ram_manager.refresh()
        if self.ram_manager.available_ram >= QWEN3_8B_MIN_RAM_GB:
            return QWEN3_8B_PATH, "Qwen3-8B-4bit"
        return QWEN3_4B_PATH, "Qwen3-4B-4bit"

    def check_ram_availability(self) -> tuple[bool, str]:
        """Return (can_load, human-readable message)."""
        self.ram_manager.refresh()
        gb = self.ram_manager.available_ram
        if gb >= QWEN3_8B_MIN_RAM_GB:
            return True, f"✅ Excellent: {gb:.1f}GB free — will use Qwen3-8B-4bit"
        elif gb >= QWEN3_4B_MIN_RAM_GB:
            return True, f"✅ Good: {gb:.1f}GB free — will use Qwen3-4B-4bit"
        else:
            return False, (
                f"❌ Need {QWEN3_4B_MIN_RAM_GB}GB minimum, only {gb:.1f}GB free.\n"
                f"   Close browser tabs, IDEs, and other apps."
            )

    async def load(self, force: bool = False) -> bool:
        """Load the selected Qwen3 model from ~/Desktop/apps/MLX/."""
        if self.is_loaded:
            return True

        ok, msg = self.check_ram_availability()
        print(msg)
        if not ok and not force:
            return False

        path, name = self._select_model()

        # Guard: model must exist locally
        if not path.exists() or not (path / "config.json").exists():
            print(f"\n❌ Model not found: {path}")
            print(f"   Run the download script to fetch it:")
            print(f"   python3 ~/Desktop/apps/MLX/download_models.py")
            return False

        try:
            from mlx_lm import load

            print(f"\n⏳ Loading {name}")
            print(f"   Path: {path}")

            self.model, self.tokenizer = load(str(path))
            self.is_loaded = True
            self.model_name = name
            self._model_path = path

            self.ram_manager.refresh()
            print(f"✅ {name} loaded!")
            print(f"   RAM remaining: ~{self.ram_manager.available_ram:.1f}GB free\n")
            return True

        except ImportError:
            print("❌ mlx-lm not installed. Run: pip install mlx-lm")
            return False
        except Exception as e:
            print(f"❌ Load failed ({name}): {e}")
            return False

    async def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate text. Raises RuntimeError if model not loaded."""
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        self.ram_manager.refresh()
        if self.ram_manager.available_ram < 1.5:
            raise MemoryError(
                f"Only {self.ram_manager.available_ram:.1f}GB free - too little for generation."
            )

        from mlx_lm import generate

        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            verbose=False,
        )
        return response.strip()

    def unload(self):
        """Free RAM by unloading the model."""
        del self.model
        del self.tokenizer
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        logger.info("Qwen3-4B unloaded.")


# ---------------------------------------------------------------------------
# Prompt templates (one per agent persona)
# ---------------------------------------------------------------------------

_LYRA_SYSTEM = """You are Lyra, a creative explorer and analyst.
Your daemon Pantalaimon (a shape-shifting marten) helps you think from many angles.
Task: generate exactly 4 diverse, creative reasoning branches for the given business idea.
Each branch must represent a genuinely different approach or assumption set.
Be explicit about your assumptions. Rate confidence honestly (0.0–1.0).
Respond with valid JSON only (no markdown fences)."""

_WILL_SYSTEM = """You are Will, a pragmatic executor focused on real-world feasibility.
Task: evaluate whether a proposed approach is achievable with the given team and resources.
Think step by step. Check assumptions. Identify concrete blockers.
Give a feasibility_score between 0.0 (impossible) and 1.0 (trivially easy).
Respond with valid JSON only (no markdown fences)."""

_COULTER_SYSTEM = """You are Mrs. Coulter, a sharp-minded critic and risk analyst.
Your Golden Monkey daemon helps you see what others miss or wish to hide.
Task: find hidden risks, challenge assumptions, play devil's advocate ruthlessly.
Give a risk_score between 0.0 (catastrophic risk) and 1.0 (very low risk).
Respond with valid JSON only (no markdown fences)."""

_IOREK_SYSTEM = """You are Iorek Byrnison, a methodical financial analyst.
Like an armored bear, you are solid, precise, and impossible to deceive.
Task: calculate development costs, revenue projections, ROI, and scenario models.
Give a financial_score between 0.0 (terrible economics) and 1.0 (excellent ROI).
Respond with valid JSON only (no markdown fences)."""

_META_SYSTEM = """You are the Meta-Daemon, an orchestrator who synthesizes all agent analyses.
Task: weigh every perspective and produce a final GO / NO_GO / NEEDS_MORE_INFO decision.
Justify your decision clearly. Assign a confidence score (0.0–1.0).
Respond with valid JSON only (no markdown fences)."""


def _build_prompt(system_msg: str, user_content: str) -> str:
    """Build a Qwen3 chat-format prompt with CoT instruction."""
    return (
        f"<|im_start|>system\n{system_msg}<|im_end|>\n"
        f"<|im_start|>user\n{user_content}\n\n"
        f"Think carefully step by step before writing your JSON answer.\n"
        f"<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )


def _extract_json(raw: str) -> Optional[Dict]:
    """
    Extract the first valid JSON object from raw LLM output.
    Strips Qwen3's <think>...</think> chain-of-thought blocks first.
    """
    # Remove Qwen3 reasoning blocks
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
    # Strip markdown fences if model added them
    raw = re.sub(r"```(?:json)?", "", raw)

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        logger.warning("JSON parse failed. Raw (first 300 chars): %s", raw[:300])
        return None


# ---------------------------------------------------------------------------
# ReasoningAgent
# ---------------------------------------------------------------------------

class ReasoningAgent:
    """
    Provides role-specific reasoning calls backed by Qwen3-4B.

    Token budgets are tuned for the 4B model on a 16GB M4:
    - Keep each call under ~1200 tokens to avoid KV-cache bloat
    - Qwen3-4B-4bit comfortably handles 4k context
    """

    # Token budget per agent call (output tokens, not input)
    LYRA_TOKENS = 1200    # 4 branches + reasoning
    WILL_TOKENS = 800     # Feasibility check
    COULTER_TOKENS = 800  # Risk analysis
    IOREK_TOKENS = 1000   # Financial modeling
    META_TOKENS = 700     # Final synthesis

    def __init__(self, llm_loader: Any):
        """
        Args:
            llm_loader: Any object with an async generate(prompt, max_tokens) method.
                        Compatible with Qwen3Loader and MLXLLMLoader.
        """
        self.llm = llm_loader

    async def _call(
        self, system_msg: str, user_content: str, max_tokens: int
    ) -> Optional[Dict]:
        """Internal: build prompt, call LLM, extract JSON."""
        prompt = _build_prompt(system_msg, user_content)
        try:
            raw = await self.llm.generate(prompt, max_tokens=max_tokens)
            result = _extract_json(raw)
            if result is None:
                logger.warning("No JSON found in LLM output (first 200 chars): %s", raw[:200])
            return result
        except Exception as e:
            logger.error("LLM call failed: %s", e)
            return None

    # -----------------------------------------------------------------------
    # Agent calls
    # -----------------------------------------------------------------------

    async def lyra_generate_branches(
        self,
        business_idea: str,
        depth: int = 1,
        past_context: str = "",
    ) -> Optional[Dict]:
        """
        Lyra generates 4 diverse reasoning branches.

        Returns:
            {
              "branches": [
                {"label": "Branch A", "description": "...", "key_assumption": "...", "confidence": 0.75},
                ...
              ],
              "reasoning_summary": "..."
            }
        """
        past_section = (
            f"\nContext from similar past analyses:\n{past_context}\n"
            if past_context else ""
        )
        user_content = f"""Business idea: {business_idea}
Current tree depth: {depth}{past_section}
Generate exactly 4 diverse reasoning branches. Each must represent a DIFFERENT approach.

Return this JSON structure:
{{
  "branches": [
    {{"label": "Branch A", "description": "...", "key_assumption": "...", "confidence": 0.0}},
    {{"label": "Branch B", "description": "...", "key_assumption": "...", "confidence": 0.0}},
    {{"label": "Branch C", "description": "...", "key_assumption": "...", "confidence": 0.0}},
    {{"label": "Branch D", "description": "...", "key_assumption": "...", "confidence": 0.0}}
  ],
  "reasoning_summary": "Brief explanation of why these 4 branches cover the solution space"
}}"""
        return await self._call(_LYRA_SYSTEM, user_content, self.LYRA_TOKENS)

    async def will_validate(
        self, branch_description: str, business_idea: str
    ) -> Optional[Dict]:
        """
        Will validates practical feasibility.

        Returns:
            {
              "verdict": "FEASIBLE" | "PARTIALLY_FEASIBLE" | "NOT_FEASIBLE",
              "feasibility_score": 0.0,
              "blockers": [...],
              "requirements": [...],
              "timeline_estimate": "...",
              "reasoning": "..."
            }
        """
        user_content = f"""Business idea: {business_idea}

Proposed approach: {branch_description}

Assess practical feasibility. Consider: required team size, technical complexity,
timeline realism, external dependencies, and resource availability.

Return this JSON:
{{
  "verdict": "FEASIBLE",
  "feasibility_score": 0.0,
  "blockers": ["list any hard blockers here"],
  "requirements": ["what is needed to execute this"],
  "timeline_estimate": "e.g. 8 weeks for MVP",
  "reasoning": "step-by-step feasibility reasoning"
}}"""
        return await self._call(_WILL_SYSTEM, user_content, self.WILL_TOKENS)

    async def coulter_assess_risks(
        self, branch_description: str, will_output: Dict
    ) -> Optional[Dict]:
        """
        Mrs. Coulter performs adversarial risk analysis.

        Returns:
            {
              "risk_score": 0.0,   (1.0 = very safe, 0.0 = catastrophic)
              "risks": [{"risk": "...", "likelihood": 0.0, "impact": "HIGH|MED|LOW", "mitigation": "..."}],
              "challenged_assumptions": [...],
              "counter_arguments": [...],
              "overall_assessment": "..."
            }
        """
        user_content = f"""Proposed approach: {branch_description}

Will's feasibility assessment:
{json.dumps(will_output, indent=2)}

Challenge this approach ruthlessly. Find hidden risks, weak assumptions, and failure modes.

Return this JSON:
{{
  "risk_score": 0.0,
  "risks": [
    {{"risk": "description", "likelihood": 0.0, "impact": "HIGH", "mitigation": "how to address it"}}
  ],
  "challenged_assumptions": ["assumptions that may be wrong"],
  "counter_arguments": ["devil's advocate arguments against this approach"],
  "overall_assessment": "one-sentence summary of risk level"
}}"""
        return await self._call(_COULTER_SYSTEM, user_content, self.COULTER_TOKENS)

    async def iorek_model_financials(
        self,
        branch_description: str,
        business_idea: str,
        budget: str = "Unknown",
    ) -> Optional[Dict]:
        """
        Iorek models the financial outlook.

        Returns:
            {
              "financial_score": 0.0,
              "dev_cost_estimate": "...",
              "revenue_projection": {"year_1": "...", "year_2": "...", "year_3": "..."},
              "roi_estimate": 0.0,
              "scenarios": {"best_case": {...}, "mid_case": {...}, "worst_case": {...}},
              "confidence": 0.0,
              "key_assumptions": [...]
            }
        """
        user_content = f"""Business idea: {business_idea}
Proposed approach: {branch_description}
Available budget: {budget}

Model the financial outlook. Show your reasoning. Be conservative but realistic.

Return this JSON:
{{
  "financial_score": 0.0,
  "dev_cost_estimate": "e.g. $25,000",
  "revenue_projection": {{"year_1": "$0 (dev)", "year_2": "$60k", "year_3": "$200k"}},
  "roi_estimate": 0.0,
  "scenarios": {{
    "best_case":  {{"roi": 0.0, "timeline": "..."}},
    "mid_case":   {{"roi": 0.0, "timeline": "..."}},
    "worst_case": {{"roi": 0.0, "timeline": "..."}}
  }},
  "confidence": 0.0,
  "key_assumptions": ["list major financial assumptions"]
}}"""
        return await self._call(_IOREK_SYSTEM, user_content, self.IOREK_TOKENS)

    async def meta_daemon_decide(
        self, business_idea: str, evaluated_branches: List[Dict]
    ) -> Optional[Dict]:
        """
        Meta-Daemon synthesizes all agent outputs into a final recommendation.

        Returns:
            {
              "decision": "GO" | "NO_GO" | "NEEDS_MORE_INFO",
              "confidence": 0.0,
              "best_branch": "Branch C",
              "rationale": "...",
              "key_success_factors": [...],
              "recommended_next_steps": [...]
            }
        """
        # Limit summary to keep prompt short (Qwen3-4B has 4k context)
        summary_str = json.dumps(evaluated_branches[:8], indent=2)

        user_content = f"""Business idea: {business_idea}

Evaluated branches (sorted by composite score):
{summary_str}

Synthesize all perspectives. Give a clear recommendation.

Return this JSON:
{{
  "decision": "GO",
  "confidence": 0.0,
  "best_branch": "branch label here",
  "rationale": "why this decision was reached",
  "key_success_factors": ["factor 1", "factor 2"],
  "recommended_next_steps": ["step 1", "step 2", "step 3"]
}}"""
        return await self._call(_META_SYSTEM, user_content, self.META_TOKENS)
