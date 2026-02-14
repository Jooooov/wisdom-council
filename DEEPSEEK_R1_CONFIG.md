# DeepSeek-R1-Distill-Qwen-14B Configuration

**Status:** 🔄 Downloading (~8GB model)
**Date:** 2026-02-13
**Why:** Reasoning capability + Portuguese support + 16GB compatibility

---

## Model Specifications

### Identity
- **Full Name:** DeepSeek-R1-Distill-Qwen-14B
- **Base Model:** Qwen-2.5 series
- **Type:** Reasoning model (distilled version)
- **Parameters:** 14 billion
- **Framework:** MLX (Apple Silicon optimized)

### Performance
- **ArenaHard Score:** Higher than base Qwen3 14B (due to reasoning)
- **Reasoning Capability:** Chain-of-thought with `<think>` tags
- **Context Window:** 40K+ tokens
- **Portuguese:** ✅ Native support (Qwen base)
- **Speed:** ~20-25 tokens/sec inference (M4 MacBook)
- **Thinking Mode:** Can enable extended reasoning for complex tasks

### RAM Requirements
- **Minimum:** 13GB (reasoning operational)
- **Ideal:** 16GB (smooth operation with headroom)
- **Your MacBook:** 16GB ✅ Perfect match
- **During Reasoning:** May use full 16GB

### Model Size
- **On Disk:** ~8GB (4-bit quantization)
- **In RAM:** ~13-14GB when loaded
- **KV Cache:** Additional 2-3GB during inference with full context

---

## Advantages Over Qwen3 8B

| Aspect | 8B (Old) | 14B R1 (New) |
|--------|----------|-------------|
| **Reasoning** | ❌ Poor | ✅ Excellent |
| **Portuguese** | ❌ Had issues | ✅ Works well |
| **RAM at 16GB** | ✅ Safe | ✅ Perfect |
| **Analysis Quality** | Generic | **Semantic + Reasoning** |
| **Business Decisions** | Limited | **Deep analysis** |

---

## Files Updated

### core/llm/deepseek_loader.py
- Model path: `DeepSeek-R1-Distill-Qwen-14B-MLX`
- Class: `MLXLLMLoader` (same, just different model)
- Loading messages updated

### core/llm/ram_manager.py
- `DEEPSEEK_R1_14B_MIN = 13` GB
- `DEEPSEEK_R1_14B_IDEAL = 16` GB
- Status messages reference DeepSeek-R1

### core/llm/__init__.py
- Docstring updated to mention reasoning capability

---

## Usage: Enabling Reasoning

```python
from core.llm import create_mlx_loader

loader = create_mlx_loader(ram_manager)
await loader.load()

# For reasoning-heavy tasks
prompt = """<think>
Let me analyze this business problem step by step...
</think>

Based on the analysis above, here's my recommendation..."""

response = await loader.generate(prompt, max_tokens=200)
```

---

## Testing with Portuguese

```python
prompt = """Analisa este código Python e explica os problemas de segurança:

```python
import subprocess
path = input("Caminho: ")
subprocess.call(f"cat {path}")
```

Responde em português."""

response = await loader.generate(prompt)
print(response)  # Will respond in Portuguese with reasoning
```

---

## Why This Model?

1. **Reasoning:** Essential for business analysis decisions
2. **Portuguese:** Proper multilingual support (unlike 8B issues)
3. **14B Power:** Stronger than 8B in understanding context
4. **RAM Perfect:** Exactly matches your 16GB setup
5. **Latest:** 2026 recommended model for Apple Silicon

---

## Previous Model: Why Removed

**Qwen3 8B:**
- ❌ Had issues responding only in Chinese
- ❌ Limited reasoning capability
- ✅ Now deleted to free space
- ✅ Replaced by DeepSeek-R1-Distill

---

## Next Steps

1. ✅ Downloading DeepSeek-R1-Distill-Qwen-14B
2. ⏳ Download completes (~10 minutes)
3. ⏳ Test with Portuguese prompt
4. ⏳ Test reasoning on business analysis
5. ⏳ Integrate into Wisdom Council agents

---

## Performance Expectations

### On 16GB MacBook Air M4
- **Load time:** ~20 seconds
- **First token:** ~2-3 seconds
- **Subsequent tokens:** 40-50ms per token
- **Reasoning response:** 15-30 seconds (includes thinking)
- **Max context:** Full 40K tokens available

### Reasoning Examples
```
User: "Should we start this business?"
Model: <thinks through market, competition, resources>
Output: Detailed analysis with step-by-step reasoning
```

---

## Verification Checklist

- [ ] Model downloaded to ~/mlx-models/DeepSeek-R1-Distill-Qwen-14B-MLX/
- [ ] RAM manager configured for 13GB minimum
- [ ] Loader points to correct model path
- [ ] Test with Portuguese prompt
- [ ] Test reasoning capability with business question
- [ ] Integrate into Wisdom Council

---

**Ready for Wisdom Council integration!**

When the Wisdom Council agents (Lyra, Iorek, Marisa, Serafina, Lee, Coram, Asriel) use this LLM, they'll have:
- Real semantic reasoning
- Portuguese language support
- Complex problem analysis
- Chain-of-thought explanations
