"""
War Room - Real Agent Collaboration using DeepSeek-R1 LLM

Each agent discusses the business case with their personality/daemon influence.
Uses DeepSeek-R1-0528-Qwen3-8B-8bit for reasoning-based analysis.
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.llm import create_ram_manager, create_mlx_loader
from core.research.manual_inputs import get_context_for_agent
from core.research.context_enricher import ContextEnricher


class WarRoom:
    """Real-time agent collaboration with LLM reasoning."""

    def __init__(self, business_case: Dict[str, Any], agents: List[Any], project_path: str = None):
        """Initialize war room with business case and agents."""
        self.business_case = business_case
        self.agents = agents
        self.project_path = project_path
        self.llm_loader = None
        self.ram_manager = None
        self.discussion_log = []
        self.agent_perspectives = {}
        self.manual_inputs_context = ""

    async def prepare(self) -> bool:
        """Prepare LLM and check RAM."""
        print("\n" + "=" * 70)
        print("🧠 INICIALIZAÇÃO DA SALA DE GUERRA")
        print("=" * 70)

        # Read project context and enrich with file analysis
        if self.project_path:
            print("\n📂 Lendo contexto do projeto...")
            try:
                # Extract additional paths from business case if it's a merged project
                additional_paths = []
                if isinstance(self.business_case, dict) and self.business_case.get('paths'):
                    # Get the Obsidian path if this is a merged project
                    obsidian_path = self.business_case['paths'].get('obsidian')
                    if obsidian_path and obsidian_path != self.project_path:
                        additional_paths.append(obsidian_path)

                self.manual_inputs_context = get_context_for_agent(self.project_path, additional_paths)
                if self.manual_inputs_context:
                    print("   ✅ Contexto do projeto carregado")

                # Enrich with file analysis
                print("\n📊 Enriquecendo contexto com análise de ficheiros...")
                enricher = ContextEnricher(self.project_path)
                enricher.analyze_project_files()
                enriched = enricher.get_enriched_context()
                self.manual_inputs_context += "\n\n" + enriched
                print("   ✅ Contexto enriquecido com ficheiros do projeto")

            except Exception as e:
                print(f"   ⚠️  Erro ao processar contexto: {e}")

        # Check RAM
        self.ram_manager = create_ram_manager()
        self.llm_loader = create_mlx_loader(self.ram_manager)

        can_load, message = self.llm_loader.check_ram_availability()
        print(f"\n{message}")

        if not can_load:
            print("\n❌ RAM insuficiente para executar Sala de Guerra com raciocínio LLM")
            return False

        # Load LLM
        print("\n⏳ Carregando DeepSeek-R1 LLM para raciocínio de agentes...")
        success = await self.llm_loader.load()

        if success:
            print("✅ LLM carregado - Sala de Guerra pronta\n")
            return True
        else:
            print("❌ Falha ao carregar LLM")
            return False

    async def conduct_discussion(self) -> Dict[str, Any]:
        """Conduct full war room discussion with LLM-based agent reasoning."""
        print("\n" + "=" * 70)
        print("⚔️  DISCUSSÃO NA SALA DE GUERRA - COLABORAÇÃO REAL DE AGENTES")
        print("=" * 70)
        print(f"\nProjeto: {self.business_case.get('project_name')}")
        print(f"Índice de Viabilidade: {self.business_case.get('viability_score', 0)}/100")

        try:
            # Phase 1: Individual Agent Analysis
            print("\n" + "-" * 70)
            print("📍 FASE 1: Análise Individual dos Agentes (com Raciocínio LLM)")
            print("-" * 70)

            for agent in self.agents:
                print(f"\n🧙 {agent.name} ({agent.role}) está analisando...")
                perspective = await self._get_agent_reasoning(agent)
                self.agent_perspectives[agent.name] = perspective

            # Phase 2: Open Discussion
            print("\n" + "-" * 70)
            print("💬 FASE 2: Discussão Aberta Entre Agentes")
            print("-" * 70)

            discussion = await self._facilitate_discussion()

            # Phase 3: Consensus Building
            print("\n" + "-" * 70)
            print("🤝 FASE 3: Construção do Consenso")
            print("-" * 70)

            consensus = await self._build_consensus()

            # Phase 4: Final Recommendation
            print("\n" + "-" * 70)
            print("🎯 FASE 4: Recomendação Final (SIM / NÃO)")
            print("-" * 70)

            recommendation = await self._generate_final_recommendation()

            return {
                "perspectives": self.agent_perspectives,
                "discussion": discussion,
                "consensus": consensus,
                "recommendation": recommendation,
                "status": "COMPLETE"
            }

        except Exception as e:
            print(f"\n❌ Discussão da Sala de Guerra falhou: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "FAILED", "error": str(e)}

    async def _get_agent_reasoning(self, agent) -> Dict[str, Any]:
        """Get LLM-based reasoning from specific agent with their personality."""
        # Build context for the agent
        business_summary = self._build_business_summary_for_agent(agent)

        # Create personality-specific prompt
        prompt = self._create_agent_prompt(agent, business_summary)

        # Get LLM reasoning
        try:
            # Use higher max_tokens for deep reasoning with chain-of-thought
            reasoning = await self.llm_loader.generate(
                prompt=prompt,
                max_tokens=800  # Allow space for thinking + detailed analysis
            )

            perspective = {
                "agent": agent.name,
                "role": agent.role,
                "daemon": getattr(agent, 'daemon', 'Unknown'),
                "reasoning": reasoning,
                "key_points": self._extract_key_points(reasoning),
                "recommendation": self._extract_recommendation(reasoning),
                "confidence": self._extract_confidence(reasoning)
            }

            # Print detailed agent thinking
            self._display_agent_thinking(agent, perspective)

            self.discussion_log.append({
                "speaker": agent.name,
                "phase": "individual_analysis",
                "content": reasoning
            })

            return perspective

        except Exception as e:
            print(f"   ⚠️  Erro ao obter raciocínio: {e}")
            return {
                "agent": agent.name,
                "role": agent.role,
                "reasoning": "Análise indisponível",
                "error": str(e)
            }

    async def _facilitate_discussion(self) -> str:
        """Facilitate discussion between agents based on their perspectives."""
        print("\n🎤 Os agentes estão discutindo suas perspectivas...\n")

        discussion_prompt = self._build_discussion_prompt()

        try:
            discussion = await self.llm_loader.generate(
                prompt=discussion_prompt,
                max_tokens=400
            )

            self.discussion_log.append({
                "speaker": "COLLECTIVE_DISCUSSION",
                "phase": "open_discussion",
                "content": discussion
            })

            print(discussion)
            return discussion

        except Exception as e:
            print(f"⚠️  Falha ao gerar discussão: {e}")
            return "Discussão não pôde ser gerada"

    async def _build_consensus(self) -> Dict[str, Any]:
        """Build consensus from all agent perspectives."""
        consensus_prompt = self._build_consensus_prompt()

        try:
            consensus_text = await self.llm_loader.generate(
                prompt=consensus_prompt,
                max_tokens=300
            )

            go_count = sum(1 for p in self.agent_perspectives.values()
                          if "SIM" in p.get("recommendation", "").upper() or "GO" in p.get("recommendation", "").upper())
            total = len(self.agent_perspectives)
            agreement = (go_count / total * 100) if total > 0 else 0

            consensus = {
                "summary": consensus_text,
                "agreement_percentage": int(agreement),
                "agents_favoring_go": go_count,
                "agents_favoring_nogo": total - go_count
            }

            print(f"\n✅ Consenso: {int(agreement)}% dos agentes favorecem SIM")
            print(f"   ({go_count}/{total})")

            return consensus

        except Exception as e:
            print(f"⚠️  Falha ao gerar consenso: {e}")
            return {
                "summary": "Consenso não pôde ser determinado",
                "error": str(e)
            }

    async def _generate_final_recommendation(self) -> Dict[str, Any]:
        """Generate final GO/NO-GO recommendation with reasoning."""
        recommendation_prompt = self._build_recommendation_prompt()

        try:
            recommendation_text = await self.llm_loader.generate(
                prompt=recommendation_prompt,
                max_tokens=350
            )

            # Determine GO/NO-GO
            is_go = "SIM" in recommendation_text.upper() or "GO" in recommendation_text.upper()

            recommendation = {
                "decision": "🟢 SIM - PROCEDER COM O PROJETO" if is_go else "🔴 NÃO - NÃO PROCEDER",
                "reasoning": recommendation_text,
                "viability_score": self.business_case.get("viability_score", 0),
                "confidence": 8 if is_go else 7  # Based on LLM reasoning
            }

            print(f"\n{'🟢' if is_go else '🔴'} DECISÃO FINAL:")
            print(f"   {recommendation['decision']}")
            print(f"\n📋 Raciocínio (da análise LLM):")
            for line in recommendation_text.split('\n')[:3]:
                if line.strip():
                    print(f"   • {line.strip()}")

            return recommendation

        except Exception as e:
            print(f"⚠️  Falha ao gerar recomendação: {e}")
            return {
                "decision": "NÃO DETERMINADO",
                "error": str(e)
            }

    # ========== Helper Methods ==========

    def _build_business_summary_for_agent(self, agent) -> str:
        """Build business case summary tailored for specific agent."""
        case = self.business_case
        summary = f"""
PROJETO: {case.get('project_name')}
TIPO: {case.get('project_type', 'Desconhecido')}

DADOS DE MERCADO:
- Índice de Viabilidade: {case.get('viability_score', 0)}/100
- Concorrentes: {len(case.get('competitive_analysis', {}).get('competitors', []))}
- Lacunas de Mercado: {len(case.get('market_research', {}).get('gaps', []))}

DESCOBERTAS-CHAVE:
Vantagens: {', '.join(case.get('competitive_analysis', {}).get('competitive_advantages', [])[:2])}
Ameaças: {', '.join(case.get('competitive_analysis', {}).get('threats', [])[:2])}
"""
        return summary.strip()

    def _create_agent_prompt(self, agent, business_summary: str) -> str:
        """Create personality-specific analysis prompt for agent."""
        # Include manual inputs context if available
        manual_context = ""
        if self.manual_inputs_context:
            manual_context = f"\n{self.manual_inputs_context}\n"

        role_prompts = {
            "analyst": f"""{manual_context}
Você é {agent.name}, um analista perspicaz com excelente capacidade de ver padrões nos dados.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em MÉTRICAS, DADOS e TENDÊNCIAS DE MERCADO:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Primeiro, explique seu processo de pensamento
2. 📊 ANÁLISE: Detalhe a interpretação dos dados
3. 🎯 CONCLUSÃO: Síntese e recomendação

Seja profundo, questione pressupostos, encontre padrões ocultos.
O que os números te dizem? Isto é viável? Responda em português.""",

            "architect": f"""{manual_context}
Você é {agent.name}, um arquiteto estratégico focado em estrutura e escalabilidade.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em ESTRUTURA, ESCALABILIDADE e VIABILIDADE:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo de pensamento arquitetônico
2. 🏗️  ANÁLISE: Avaliação de estrutura e escalabilidade
3. 🎯 CONCLUSÃO: Pontos fracos fundamentais e viabilidade

Como esse negócio está estruturado? Pode escalar? Responda em português.""",

            "developer": f"""{manual_context}
Você é {agent.name}, um operador decisivo focado em EXECUÇÃO e VIABILIDADE TÉCNICA.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em EXECUÇÃO, RECURSOS e VIABILIDADE TÉCNICA:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo de pensamento técnico
2. ⚙️  ANÁLISE: Avaliação de execução e recursos
3. 🎯 CONCLUSÃO: Riscos e viabilidade de implementação

Isso pode realmente ser construído? Temos recursos? Responda em português.""",

            "researcher": f"""{manual_context}
Você é {agent.name}, um pesquisador estratégico com profundo conhecimento de mercado.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em PROFUNDIDADE DE MERCADO, INTELIGÊNCIA COMPETITIVA e OPORTUNIDADES:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo investigativo
2. 🔍 ANÁLISE: Inteligência de mercado e competição
3. 🎯 CONCLUSÃO: Oportunidades e lacunas identificadas

Qual é a história profunda do mercado? Quem são os concorrentes reais? Responda em português.""",

            "writer": f"""{manual_context}
Você é {agent.name}, um comunicador estratégico focado em POSICIONAMENTO e ENTRADA NO MERCADO.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em POSICIONAMENTO, MENSAGEM e ENTRADA NO MERCADO:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo de pensamento estratégico
2. 💬 ANÁLISE: Posicionamento, narrativa e GTM
3. 🎯 CONCLUSÃO: Estratégia de comunicação recomendada

Como posicionamos? Qual é nossa história? Responda em português.""",

            "validator": f"""{manual_context}
Você é {agent.name}, um validador cuidadoso focado em RISCOS e PRESSUPOSTOS.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio focando em RISCOS, PRESSUPOSTOS e VALIDAÇÃO:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo crítico de pensamento
2. ⚠️  ANÁLISE: Riscos, pressupostos e pontos fracos
3. 🎯 CONCLUSÃO: O que precisa validação crítica

O que poderia dar errado? O que estamos assumindo? Responda em português.""",

            "coordinator": f"""{manual_context}
Você é {agent.name}, um coordenador visionário focado em ESTRATÉGIA e ALINHAMENTO.

IMPORTANTE: Mostre seu raciocínio profundo passo-a-passo.

Analise este caso de negócio como um LÍDER ESTRATÉGICO:
{business_summary}

Forneça sua análise como {agent.name} faria:
1. 🧠 RACIOCÍNIO: Seu processo estratégico de pensamento
2. 🎯 ANÁLISE: Alinhamento, viabilidade estratégica e fit
3. 🎯 CONCLUSÃO: Recomendação executiva final

Isto está alinhado com nossa visão? Vale o tempo e recursos? Responda em português.""",
        }

        # Match role to prompt
        for key, prompt in role_prompts.items():
            if key in agent.role.lower() or key in agent.name.lower():
                return prompt

        # Default
        return f"{manual_context}Analise este caso de negócio: {business_summary}\n\nQual é sua opinião profissional? Responda em português."

    def _build_discussion_prompt(self) -> str:
        """Build prompt for agents to discuss together."""
        perspectives_summary = "\n".join([
            f"- {name}: {p.get('recommendation', 'Indisponível')}"
            for name, p in self.agent_perspectives.items()
        ])

        return f"""Os agentes estão agora tendo uma discussão aberta sobre o caso de negócio:
{self.business_case.get('project_name')}

Posições atuais:
{perspectives_summary}

Tenha uma discussão realista e profissional entre os agentes. Inclua:
- Áreas de concordância
- Pontos de discordância
- Perguntas que precisam resposta
- Preocupações levantadas
- Possíveis compromissos

Escreva a discussão como uma conversa natural com insights de cada perspectiva. Responda em português."""

    def _build_consensus_prompt(self) -> str:
        """Build prompt for consensus building."""
        return f"""Com base na análise de {len(self.agent_perspectives)} especialistas,
determine o consenso sobre o caso de negócio: {self.business_case.get('project_name')}

A equipe consiste em especialistas em:
{', '.join([f"{name} ({p.get('role')})" for name, p in self.agent_perspectives.items()])}

Resuma a posição do consenso. Os especialistas concordam? Onde eles divergem?
Há uma inclinação clara para SIM ou NÃO? Responda em português."""

    def _build_recommendation_prompt(self) -> str:
        """Build prompt for final recommendation."""
        return f"""Como síntese da análise de especialistas, forneça uma recomendação final SIM/NÃO para:
{self.business_case.get('project_name')}

Índice de Viabilidade: {self.business_case.get('viability_score', 0)}/100

Com base em:
- Análise de mercado
- Posição competitiva
- Experiência da equipe
- Avaliação de risco
- Viabilidade financeira

Devemos proceder (SIM) ou pivotar/cancelar (NÃO)?
Forneça raciocínio claro para sua recomendação. Responda em português."""

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from reasoning text."""
        lines = text.split('\n')
        points = [l.strip() for l in lines if l.strip() and len(l.strip()) > 20]
        return points[:3]

    def _extract_recommendation(self, text: str) -> str:
        """Extract GO/NO-GO recommendation from reasoning."""
        text_upper = text.upper()
        if "GO" in text_upper and "NO-GO" not in text_upper:
            return "GO"
        elif "NO-GO" in text_upper or ("NO" in text_upper and "GO" in text_upper and text_upper.index("NO") < text_upper.index("GO")):
            return "NO-GO"
        else:
            return "UNCLEAR"

    def _extract_confidence(self, text: str) -> int:
        """Extract confidence level from reasoning."""
        # Simple heuristic: longer, more detailed reasoning = higher confidence
        confidence = min(9, max(4, len(text.split()) // 30))
        return confidence

    def _display_agent_thinking(self, agent, perspective: Dict[str, Any]):
        """Display agent's thinking process in a visual format."""
        daemon = perspective.get('daemon', 'Desconhecido')
        reasoning = perspective.get('reasoning', '')
        recommendation = perspective.get('recommendation', 'INDISPONÍVEL')
        confidence = perspective.get('confidence', 0)
        key_points = perspective.get('key_points', [])

        # Visual header with agent info
        print(f"\n   {'╭' + '─' * 66 + '╮'}")
        print(f"   │ 🧠 PENSAMENTO DE {agent.name.upper():<54}│")
        print(f"   │    Papel: {agent.role:<58}│")
        print(f"   │    Daemon: {daemon:<57}│")
        print(f"   {'├' + '─' * 66 + '┤'}")

        # Show reasoning with word wrap
        reasoning_lines = reasoning.split('\n')
        print(f"   │ 💭 RACIOCÍNIO:                                          │")
        for line in reasoning_lines[:5]:  # Show first 5 lines
            wrapped_line = line[:62] if len(line) > 62 else line
            print(f"   │    {wrapped_line:<62}│")
        if len(reasoning_lines) > 5:
            print(f"   │    ... ({len(reasoning_lines)-5} mais linhas de raciocínio) │")

        # Show key points
        if key_points:
            print(f"   │                                                        │")
            print(f"   │ 🎯 PONTOS-CHAVE:                                       │")
            for point in key_points[:3]:
                wrapped_point = point[:58] if len(point) > 58 else point
                print(f"   │    • {wrapped_point:<60}│")

        # Show recommendation and confidence
        print(f"   │                                                        │")
        confidence_bar = "█" * (confidence // 2) + "░" * (5 - confidence // 2)
        print(f"   │ ✓ RECOMENDAÇÃO: {recommendation:<45}│")
        print(f"   │   Confiança: {confidence_bar} ({confidence}/10)            │")
        print(f"   {'╰' + '─' * 66 + '╯'}")

    async def cleanup(self):
        """Clean up and unload LLM."""
        if self.llm_loader:
            self.llm_loader.unload()
            print("\n✅ LLM descarregado, recursos libertados")


async def run_war_room(business_case: Dict[str, Any], agents: List[Any], project_path: str = None) -> Dict[str, Any]:
    """Factory function to run war room discussion."""
    war_room = WarRoom(business_case, agents, project_path)

    # Prepare
    ready = await war_room.prepare()
    if not ready:
        return {"status": "FAILED", "error": "Não foi possível preparar a Sala de Guerra"}

    # Conduct discussion
    result = await war_room.conduct_discussion()

    # Cleanup
    await war_room.cleanup()

    return result
