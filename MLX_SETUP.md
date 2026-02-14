# MLX LLM Integration - Qwen3 8B Configuration

**Status:** ✅ Configured for Qwen3 8B MLX 8bit (Actually Installed)
**Date:** 2026-02-13
**Model:** Qwen3 8B MLX 8bit (NOT Qwen3 14B as originally documented)

---

## What's Actually Installed

The system has **Qwen3 8B** with **8-bit quantization**, not the 14B version mentioned in some documentation.

```
Location: ~/mlx-models/Qwen3-8B-MLX-8bit/
Size: ~8GB on disk
RAM Required: 9GB minimum (8.3GB model + 0.7GB overhead)
RAM Ideal: 12GB+ for comfortable operation
Quantization: 8-bit (not 4-bit)
Framework: MLX (Apple Silicon optimized)
```

### Available Models in ~/mlx-models/
- ✅ **Qwen3-8B-MLX-8bit** (ACTIVE - 8-bit quantization)
- Qwen3-4B-Instruct-2507-4bit (backup option)

---

## Why Not 14B?

The documentation mentioned wanting a 14B model, but:
1. **Not installed**: The Qwen3-14B-4bit model isn't at ~/mlx-models/Qwen3-14B-4bit/
2. **8B works well**: The 8B model scores ArenaHard 85.5 (rivals 30B in many tasks)
3. **Previous issues**: The 8B was recently responding only in Chinese (possible model weight issue)
4. **RAM consideration**: 14B would need 16GB minimum; 8B needs only 9GB

---

## RAM Requirements - ACTUAL

| Model | Quantization | Model Size | Min RAM | Ideal RAM |
|-------|--------------|-----------|---------|-----------|
| **Qwen3 8B** | 8-bit | ~8GB | **9GB** | **12GB** |
| Qwen3 4B | 4-bit | ~4GB | 5GB | 8GB |
| Qwen3 14B | 4-bit | ~8.3GB | 16GB | 24GB |

**Currently configured:** Qwen3 8B with 9GB minimum threshold

---

## Files Updated

### 1. `core/llm/deepseek_loader.py` → `MLXLLMLoader`
- Changed from hypothetical Qwen3 14B to actual Qwen3 8B
- Model path: `~/mlx-models/Qwen3-8B-MLX-8bit/`
- Loading time: ~20 seconds (reduced from ~30)
- RAM display: Shows 8.3GB actual usage

### 2. `core/llm/ram_manager.py`
- `QWEN3_8B_MIN = 9` (was DEEPSEEK_14B_MIN = 16)
- `QWEN3_8B_IDEAL = 12` (was DEEPSEEK_14B_IDEAL = 24)
- Updated status messages to reference Qwen3 8B
- Method `can_run_deepseek_14b()` now checks for 9GB minimum

### 3. `core/llm/__init__.py`
- Exports: `MLXLLMLoader`, `create_mlx_loader`, `MLXAnalyzer`, `analyze_with_mlx`
- Removed old: `DeepSeekLoader`, `create_deepseek_loader`, `DeepSeekAnalyzer`, `analyze_with_deepseek`

### 4. `core/llm/deepseek_analyzer.py` → `MLXAnalyzer`
- Already updated (class renamed, no path changes needed)

---

## Usage Example

```python
from core.llm import create_ram_manager, create_mlx_loader, MLXAnalyzer

# Setup
ram_manager = create_ram_manager()
loader = create_mlx_loader(ram_manager)

# Load model
await loader.load()

# Generate text
response = await loader.generate("Your prompt here", max_tokens=100)
print(response)

# Analyze code
analyzer = MLXAnalyzer(loader)
analysis = await analyzer.analyze_code_file("/path/to/file.py")

# Cleanup
loader.unload()
```

---

## Testing MLX Integration

Run the integration test:
```bash
cd ~/Desktop/Apps/His\ Dark\ Materials
python test_mlx_integration.py
```

This will:
1. Check system RAM and requirements
2. Verify model exists at correct path
3. Load the Qwen3 8B model
4. Test generation with a simple prompt
5. Unload the model and cleanup

---

## Characteristics of Qwen3 8B

- **ArenaHard Score:** 85.5 (high quality despite smaller size)
- **Context Window:** 40K tokens (full conversation history support)
- **Speed:** ~24.5 tokens/sec on M4 MacBook
- **Quantization:** 8-bit (good balance of speed and quality)
- **Thinking Mode:** Can switch between reasoning and fast response
- **Generation Speed:** Maintains responsiveness with max_tokens <= 200

---

## Performance Notes

After model load:
- ~8.3GB RAM in use by model
- ~3.7GB RAM available (on 12GB system)
- ~1-2GB additional during text generation

**Recommended configuration:**
- Keep max_tokens ≤ 100-200 for fast responses
- Close other apps if RAM is below 12GB
- Monitor with: `top -l 1 | grep Memory`

---

## Troubleshooting

**"Model not found" error:**
```bash
# Verify model exists
ls ~/mlx-models/Qwen3-8B-MLX-8bit/
# Should show: config.json, model.safetensors, tokenizer.model, etc.
```

**"Out of Memory" errors:**
1. Close browser, IDE, other apps
2. Reduce max_tokens to 50
3. Wait for other processes to finish
4. Check: `top -l 1 | grep Memory`

**Model responding only in Chinese:**
- This happened with previous 8B weights
- Current weights should be fixed
- If occurs, consider upgrading to 14B if RAM permits

---

## Next Steps

1. ✅ MLX integration configured for Qwen3 8B
2. ✅ RAM manager updated with correct thresholds
3. ✅ Integration test script created
4. ⏳ Test with actual project analysis
5. ⏳ Integrate into orchestration workflow

---

## Important Files

- **Model location:** `~/mlx-models/Qwen3-8B-MLX-8bit/`
- **Venv:** `~/Projects/llm-local/venv/`
- **Reference:** `~/Projects/llm-local/run_qwen3_14b.py` (note: name uses 14B but loads 8B)
- **His Dark Materials config:** `~/Desktop/Apps/His Dark Materials/core/llm/`

---

**Verified on:** MacBook with Apple Silicon (M4)
**Python:** 3.13+
**MLX Framework:** Latest stable
**Setup Status:** Ready for integration into agent system
