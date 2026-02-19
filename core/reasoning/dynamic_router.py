"""
Dynamic Router - RAM-aware sequential routing for MCTS agent phases.

Design decision (16GB M4 + Qwen3-4B-4bit):
    Always sequential. With ~2.3GB for the model and OS overhead,
    there is no headroom to run two LLM calls concurrently.

    The router checks free RAM before each call and skips any task
    that would push the system below MIN_FREE_RAM_GB, logging a warning
    instead of crashing the process.

Future extension:
    When available_ram > PARALLEL_THRESHOLD_GB, switch to asyncio.gather
    for independent agent calls (Will + Mrs. Coulter can in theory be parallel).
"""

import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple

import psutil

logger = logging.getLogger(__name__)

# Minimum free RAM before executing a generation call
MIN_FREE_RAM_GB = 2.0

# Threshold above which parallel execution becomes possible (future use)
PARALLEL_THRESHOLD_GB = 8.0


def get_available_ram_gb() -> float:
    """Return current free RAM in GB."""
    return psutil.virtual_memory().available / (1024 ** 3)


class DynamicRouter:
    """
    Routes agent calls sequentially with RAM gating.

    Usage:
        router = DynamicRouter()
        results = await router.run_sequential([
            ("will",    lambda: agent.will_validate(branch, idea)),
            ("coulter", lambda: agent.coulter_assess_risks(branch, will_out)),
            ("iorek",   lambda: agent.iorek_model_financials(branch, idea, budget)),
        ])
        will_result    = results["will"]
        coulter_result = results["coulter"]
        iorek_result   = results["iorek"]
    """

    def check_ram(self) -> Tuple[bool, float]:
        """Return (ok, available_gb). ok=False means skip the call."""
        gb = get_available_ram_gb()
        return gb >= MIN_FREE_RAM_GB, gb

    async def run_sequential(
        self,
        tasks: List[Tuple[str, Callable[[], Coroutine]]],
    ) -> Dict[str, Optional[Any]]:
        """
        Run tasks one by one in the order given.

        Args:
            tasks: List of (name, async_callable). The callable is a zero-arg
                   coroutine factory (e.g. ``lambda: agent.will_validate(...)``).

        Returns:
            Dict mapping each name to its result (or None if skipped / errored).
        """
        results: Dict[str, Optional[Any]] = {}

        for name, coro_factory in tasks:
            ok, gb = self.check_ram()

            if not ok:
                logger.warning(
                    "Skipping '%s': only %.1fGB free (need %.1fGB).",
                    name, gb, MIN_FREE_RAM_GB,
                )
                print(f"   ⚠️  [{name}] skipped — low RAM ({gb:.1f}GB free).")
                results[name] = None
                continue

            logger.info("Running '%s' (%.1fGB free).", name, gb)
            print(f"   [{name}] running... ({gb:.1f}GB free)")

            try:
                results[name] = await coro_factory()
            except MemoryError as e:
                logger.error("MemoryError in '%s': %s", name, e)
                print(f"   ❌ [{name}] MemoryError — {e}")
                results[name] = None
            except Exception as e:
                logger.error("Error in '%s': %s", name, e)
                print(f"   ❌ [{name}] failed — {e}")
                results[name] = None

        return results
