#!/usr/bin/env python3
"""
Test DeepSeek-R1-Distill-Qwen-14B with Portuguese
Verify reasoning and language support
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.llm import create_ram_manager, create_mlx_loader


async def main():
    """Test DeepSeek-R1 with Portuguese prompts."""
    print("=" * 70)
    print("🇵🇹 DeepSeek-R1-Distill-Qwen-14B - Portuguese Test")
    print("=" * 70)

    # Check system
    ram_manager = create_ram_manager()
    loader = create_mlx_loader(ram_manager)

    print(f"\n📊 System Status:")
    ram_manager.print_status()

    if not loader.model_exists():
        print(f"\n❌ Model not found at {loader.model_path}")
        return False

    if not loader.can_load():
        print(f"\n❌ Insufficient RAM")
        return False

    print(f"\n🚀 Loading DeepSeek-R1-Distill-Qwen-14B...")
    success = await loader.load()

    if not success:
        print(f"❌ Failed to load model")
        return False

    print(f"✅ Model loaded!")

    # Test 1: Simple Portuguese response
    print(f"\n{'='*70}")
    print("Test 1: Simple Portuguese Question")
    print(f"{'='*70}")

    prompt1 = "Qual é a capital de Portugal?"
    print(f"Q: {prompt1}")
    response1 = await loader.generate(prompt1, max_tokens=50)
    print(f"A: {response1}\n")

    # Test 2: Code analysis in Portuguese
    print(f"{'='*70}")
    print("Test 2: Code Analysis (Portuguese)")
    print(f"{'='*70}")

    prompt2 = """Analisa este código Python e explica o problema de segurança:

```python
import subprocess
user_input = input("Digite um comando: ")
subprocess.call(user_input, shell=True)
```

Responde em português."""

    print(f"Q: Análise de segurança de código\n")
    response2 = await loader.generate(prompt2, max_tokens=100)
    print(f"A:\n{response2}\n")

    # Test 3: Reasoning - Business decision
    print(f"{'='*70}")
    print("Test 3: Reasoning - Business Decision")
    print(f"{'='*70}")

    prompt3 = """Você é um consultor de negócios. Analise este cenário:

Tenho uma ideia para um software SaaS de análise de dados para PMEs.
O mercado é competitivo (Tableau, Power BI), mas tenho diferencial em
preço baixo e interface para português.

Responda em português, pensando através do problema:
- Quais são os riscos?
- Qual é o tamanho do mercado?
- É viável?"""

    print(f"Q: Análise de viabilidade de negócio\n")
    response3 = await loader.generate(prompt3, max_tokens=150)
    print(f"A:\n{response3}\n")

    # Test 4: Reasoning with thinking tags
    print(f"{'='*70}")
    print("Test 4: Reasoning with Extended Thinking")
    print(f"{'='*70}")

    prompt4 = """<think>
Vou pensar sobre este problema passo a passo...
</think>

Um cliente quer saber se deve investir em IA para o seu negócio de comércio.
O que devo considerar? Responde em português com um raciocínio estruturado."""

    print(f"Q: Decisão com raciocínio estruturado\n")
    response4 = await loader.generate(prompt4, max_tokens=120)
    print(f"A:\n{response4}\n")

    # Cleanup
    loader.unload()

    print(f"{'='*70}")
    print("✅ All tests completed successfully!")
    print(f"{'='*70}\n")

    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
