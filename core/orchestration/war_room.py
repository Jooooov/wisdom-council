"""
War Room - Real Agent Collaboration using Qwen3-4B LLM

Each agent discusses the business case with their personality/daemon influence.
Uses Qwen3-4B-4bit for reasoning-based analysis.
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
from core.memory.hybrid_memory import create_hybrid_memory

# Strategic order for agent analysis — mirrors a real consulting pipeline
# Each agent builds on the previous one's insights:
#   1. Research first (context)  →  2. Analyse data  →  3. Design structure
#   4. Evaluate execution  →  5. Validate assumptions  →  6. Communicate
#   7. Strategic alignment  →  8. Tool recommendations
AGENT_ANALYSIS_ORDER = [
    "researcher",    # Serafina — gather context and research first
    "analyst",       # Lyra — analyse the data gathered
    "architect",     # Iorek — design structure based on analysis
    "developer",     # Marisa — evaluate execution feasibility
    "validator",     # Coram — validate and test assumptions
    "writer",        # Lee — synthesise and communicate findings
    "coordinator",   # Asriel — strategic alignment and direction
    "tools_manager", # Mary — tool recommendations and holistic view
]


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
        self.hybrid_memory = create_hybrid_memory()  # RAG + Graph learning

    async def prepare(self) -> bool:
        """Prepare LLM and check RAM."""
        print("\n" + "=" * 70)
        print("🧠 INICIALIZAÇÃO DA SALA DE GUERRA")
        print("=" * 70)

        # Read project context and enrich with file analysis + Perplexity research
        if self.project_path:
            print("\n📂 Lendo contexto do projeto...")
            try:
                import os

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

                # Enrich with file analysis and Perplexity research
                print("\n📊 Enriquecendo contexto com análise de ficheiros + Perplexity...")
                enricher = ContextEnricher(self.project_path)
                enricher.analyze_project_files()

                # Add Perplexity research (async call in async context)
                api_key = os.getenv('PERPLEXITY_API_KEY')
                if api_key:
                    try:
                        query = enricher._generate_research_query()
                        await enricher.enrich_with_web_research(query, api_key)
                    except Exception as e:
                        print(f"   ⚠️  Erro ao pesquisar Perplexity: {e}")

                enriched = enricher.get_enriched_context()
                self.manual_inputs_context += "\n\n" + enriched
                print("   ✅ Contexto enriquecido com ficheiros e pesquisa")

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
        print("\n⏳ Carregando Qwen3-4B LLM para raciocínio de agentes...")
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
            # Phase 1: Individual Agent Analysis + Daemon Debate
            print("\n" + "-" * 70)
            print("📍 FASE 1: Análise Individual + Debate com Daemon")
            print("    (Cada agente consulta o seu daemon antes de emitir parecer)")
            print("-" * 70)

            # Get agents in strategic pipeline order
            ordered_agents = self._get_ordered_agents()

            for i, agent in enumerate(ordered_agents, 1):
                print(f"\n🧙 [{i}/{len(ordered_agents)}] {agent.name} ({agent.role}) está analisando...")
                perspective = await self._get_agent_reasoning(agent)
                self.agent_perspectives[agent.name] = perspective
                
                # Check for research questions and pause if needed
                questions = perspective.get('research_questions', [])
                if questions:
                    print(f"\n❓ {agent.name} tem dúvidas que precisam de pesquisa:")
                    for q in questions:
                        print(f"   - {q}")
                    
                    user_help = input(f"\n🤔 Queres ajudar a pesquisar estas questões no Perplexity agora? (s/n): ").lower()
                    if user_help == 's':
                        research_data = input(f"📝 Introduz aqui os resultados da tua pesquisa (ou 'pular'): ")
                        if research_data.lower() != 'pular':
                            # Update business case with new context for future agents
                            if 'extra_context' not in self.business_case or not self.business_case['extra_context']:
                                self.business_case['extra_context'] = ""
                            
                            self.business_case['extra_context'] += f"\n\n🔍 INFO ADICIONAL (Pesquisada pelo utilizador para {agent.name}):\n{research_data}"
                            print(f"✅ Informação adicionada ao contexto da Sala de Guerra.")

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

            result = {
                "perspectives": self.agent_perspectives,
                "discussion": discussion,
                "consensus": consensus,
                "recommendation": recommendation,
                "status": "COMPLETE"
            }

            # Store in hybrid memory for learning
            try:
                self.hybrid_memory.store_analysis({
                    "project_name": self.business_case.get('project_name'),
                    "project_type": self.business_case.get('project_type'),
                    "summary": str(result)[:500],
                    "perspectives": self.agent_perspectives,
                    "conclusion": recommendation.get('decision', '')
                })
                print("\n📚 Análise armazenada em memória de aprendizado")
            except Exception as e:
                print(f"   ⚠️  Erro ao guardar em memória: {e}")

            return result

        except Exception as e:
            print(f"\n❌ Discussão da Sala de Guerra falhou: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "FAILED", "error": str(e)}

    async def _get_agent_reasoning(self, agent) -> Dict[str, Any]:
        """Get LLM-based reasoning from specific agent with daemon debate.

        Flow:
        1. Agent produces initial reasoning
        2. Daemon critiques and challenges (complementary perspective)
        3. Agent consolidates both views into final opinion
        """
        # Build context for the agent
        business_summary = self._build_business_summary_for_agent(agent)

        # Get past experiences from hybrid memory (RAG + Graph)
        past_experiences = ""
        try:
            # Retrieve similar analyses by agent role
            similar = self.hybrid_memory.retrieve_similar_analyses(
                f"{agent.role} {self.business_case.get('project_type', '')}",
                top_k=2
            )

            # Retrieve pattern insights for this project type
            patterns = self.hybrid_memory.retrieve_pattern_insights(
                self.business_case.get('project_type', '')
            )

            if similar or patterns:
                past_experiences = "\n\n📚 EXPERIÊNCIAS PASSADAS (Memória Aprendida):\n"

                if similar:
                    past_experiences += "Análises similares:\n"
                    for mem in similar:
                        past_experiences += f"- {mem.get('project', 'Projeto anterior')}: {mem.get('conclusion', '')[:80]}...\n"

                if patterns:
                    past_experiences += f"Padrões para {self.business_case.get('project_type')}:\n"
                    if patterns.get('common_risks'):
                        past_experiences += f"- Riscos comuns: {', '.join(patterns['common_risks'][:2])}\n"
                    if patterns.get('common_opportunities'):
                        past_experiences += f"- Oportunidades: {', '.join(patterns['common_opportunities'][:2])}\n"

        except Exception as e:
            pass  # Memory retrieval optional

        # Create personality-specific prompt
        prompt = self._create_agent_prompt(agent, business_summary, past_experiences)

        # Get LLM reasoning
        try:
            # Step 1: Agent's initial reasoning
            print(f"      💭 {agent.name} está a formular a sua análise inicial...")
            initial_reasoning = await self.llm_loader.generate(
                prompt=prompt,
                max_tokens=3000  # Full reasoning without truncation
            )

            # Step 2: Daemon critique (the soul challenges the human)
            daemon_critique = await self._get_daemon_critique(
                agent, initial_reasoning, business_summary
            )

            # Step 3: Agent consolidation (incorporating daemon's feedback)
            if daemon_critique and daemon_critique != "Crítica indisponível":
                consolidation_prompt = f"""Tu és {agent.name} ({agent.role}).
O teu daemon acabou de te desafiar com esta crítica:

{daemon_critique}

A tua análise inicial era:
{initial_reasoning[:600]}

Agora, CONSOLIDA a tua opinião final em 3-5 linhas, incorporando os pontos válidos do teu daemon.
Mantém a tua essência mas reconhece os pontos cegos que o daemon identificou.
Responde em português."""

                print(f"      🔄 {agent.name} está a consolidar a opinião final...")
                consolidated = await self.llm_loader.generate(
                    prompt=consolidation_prompt,
                    max_tokens=500
                )
            else:
                consolidated = initial_reasoning

            # Build the complete reasoning chain
            full_reasoning = f"{initial_reasoning}\n\n--- DAEMON DEBATE ---\n{daemon_critique}\n\n--- OPINIÃO CONSOLIDADA ---\n{consolidated}"

            # Extract research questions
            questions = self._extract_research_questions(consolidated)

            perspective = {
                "agent": agent.name,
                "role": agent.role,
                "daemon": getattr(agent, 'daemon', 'Unknown'),
                "reasoning": consolidated, # Use consolidated for main reasoning
                "initial_reasoning": initial_reasoning,
                "daemon_critique": daemon_critique,
                "consolidated_opinion": consolidated,
                "key_points": self._extract_key_points(consolidated),
                "recommendation": self._extract_recommendation(consolidated),
                "confidence": self._extract_confidence(consolidated),
                "research_questions": questions
            }

            # Print detailed agent thinking + daemon debate
            self._display_agent_thinking(agent, perspective)
            self._display_daemon_debate(agent, perspective)

            self.discussion_log.append({
                "speaker": agent.name,
                "phase": "individual_analysis_with_daemon",
                "content": full_reasoning
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

    async def _get_daemon_critique(self, agent, agent_reasoning: str, business_context: str) -> str:
        """Get the daemon's critical counter-perspective to the agent's reasoning.

        The daemon acts as the agent's internal conscience — a complementary
        voice that challenges assumptions and refines the analysis.
        """
        daemon_name = agent.daemon.split('(')[0].strip() if '(' in agent.daemon else agent.daemon
        print(f"      🐾 {daemon_name} está a desafiar {agent.name}...")

        try:
            # Use the Agent's built-in daemon debate prompt generator
            daemon_prompt = agent.get_daemon_debate_prompt(agent_reasoning, business_context)

            critique = await self.llm_loader.generate(
                prompt=daemon_prompt,
                max_tokens=400  # Daemon should be concise and sharp
            )

            return critique

        except Exception as e:
            print(f"      ⚠️  Daemon não respondeu: {e}")
            return "Crítica indisponível"

    def _display_daemon_debate(self, agent, perspective: Dict[str, Any]):
        """Display the daemon's critique and the agent's consolidated response."""
        daemon_name = agent.daemon.split('(')[0].strip() if '(' in agent.daemon else agent.daemon
        critique = perspective.get('daemon_critique', '')
        consolidated = perspective.get('consolidated_opinion', '')

        if not critique or critique == "Crítica indisponível":
            return

        # Daemon critique box
        print(f"\n   {'╭' + '─' * 66 + '╮'}")
        print(f"   │ 🐾 DAEMON: {daemon_name.upper():<53}│")
        print(f"   │    Desafia {agent.name} com perspectiva complementar{' ' * (10 - len(agent.name))}│")
        print(f"   {'├' + '─' * 66 + '┤'}")

        critique_lines = [l.strip() for l in critique.split('\n') if l.strip()]
        for line in critique_lines[:6]:
            wrapped = line[:62] if len(line) > 62 else line
            print(f"   │    {wrapped:<62}│")

        print(f"   {'╰' + '─' * 66 + '╯'}")

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
            print(f"\n📋 Raciocínio Final:")
            lines = [l.strip() for l in recommendation_text.split('\n') if l.strip()]
            unique_lines = []
            for l in lines:
                if l not in unique_lines and len(l) > 10:
                    unique_lines.append(l)
            
            for line in unique_lines[:3]:
                print(f"   • {line}")

            return recommendation

        except Exception as e:
            print(f"⚠️  Falha ao gerar recomendação: {e}")
            return {
                "decision": "NÃO DETERMINADO",
                "error": str(e)
            }

    def _get_ordered_agents(self) -> List[Any]:
        """Sort agents according to the strategic AGENT_ANALYSIS_ORDER."""
        ordered = []
        
        # Create a map for quick lookup
        agent_map = {}
        for agent in self.agents:
            role_key = agent.id.lower() if hasattr(agent, "id") else agent.role.lower()
            if role_key not in agent_map:
                agent_map[role_key] = []
            agent_map[role_key].append(agent)
            
        # Build list based on order
        for role_id in AGENT_ANALYSIS_ORDER:
            if role_id in agent_map:
                ordered.extend(agent_map[role_id])
                
        # Add any agents not in the ordered list (safety first)
        for agent in self.agents:
            if agent not in ordered:
                ordered.append(agent)
                
        return ordered

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
        # Add strategic research if available
        if case.get('extra_context'):
            summary += f"\n🌐 PESQUISA ESTRATÉGICA (Perplexity):\n{case['extra_context']}\n"

        return summary.strip()

    def _create_agent_prompt(self, agent, business_summary: str, past_experiences: str = "") -> str:
        """Create personality-specific analysis prompt for agent."""
        # Include manual inputs context if available
        manual_context = ""
        if self.manual_inputs_context:
            manual_context = f"\n{self.manual_inputs_context}\n"

        role_prompts = {
            "analyst": f"""{manual_context}{past_experiences}
{agent.name} analisa MÉTRICAS, DADOS e TENDÊNCIAS DE MERCADO.

Caso de negócio:
{business_summary}

Pensamento: Que dizem os números? É viável? Que pressupostos questionar? Que padrões encontra?""",

            "architect": f"""{manual_context}{past_experiences}
{agent.name} analisa ESTRUTURA, ESCALABILIDADE e VIABILIDADE arquitetônica.

Caso de negócio:
{business_summary}

Pensamento: Como está estruturado? Pode escalar? Que fraquezas fundamentais existem?""",

            "developer": f"""{manual_context}{past_experiences}
{agent.name} avalia EXECUÇÃO, RECURSOS e VIABILIDADE TÉCNICA.

Caso de negócio:
{business_summary}

Pensamento: Pode ser construído? Temos recursos? Qual é o risco de implementação?""",

            "researcher": f"""{manual_context}{past_experiences}
{agent.name} explora MERCADO, COMPETIÇÃO e OPORTUNIDADES.

Caso de negócio:
{business_summary}

Pensamento: Qual é a história profunda do mercado? Quem são os verdadeiros concorrentes? Que oportunidades estão ocultas?""",

            "writer": f"""{manual_context}{past_experiences}
{agent.name} avalia POSICIONAMENTO, MENSAGEM e ENTRADA NO MERCADO.

Caso de negócio:
{business_summary}

Pensamento: Como posicionamos? Qual é nossa história? Como ganhamos no mercado?""",

            "validator": f"""{manual_context}{past_experiences}
{agent.name} questiona RISCOS, PRESSUPOSTOS e VALIDAÇÃO.

Caso de negócio:
{business_summary}

Pensamento: O que poderia dar errado? Que pressupostos podem estar errados? O que precisa validação?""",

            "coordinator": f"""{manual_context}{past_experiences}
{agent.name} avalia como LÍDER ESTRATÉGICO a ESTRATÉGIA e ALINHAMENTO.

Caso de negócio:
{business_summary}

Pensamento: Isto está alinhado com nossa visão? Vale nosso tempo e recursos?""",
        }
        # Default
        instruction = "\nResponde DIRECTAMENTE (sem 'Okay' ou introduções) com uma secção final [QUESTOES_DE_PESQUISA] se necessário. Sê incisivo. /no_filler"
        return f"{manual_context}Analise este caso: {business_summary}\n\nOpinião profissional? {instruction}"

    def _extract_research_questions(self, text: str) -> List[str]:
        """Extract research questions from agent output [QUESTOES_DE_PESQUISA]."""
        import re
        pattern = r"\[QUESTOES_DE_PESQUISA\](.*)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
            
        questions_text = match.group(1).strip()
        lines = questions_text.split('\n')
        questions = []
        for line in lines:
            line = line.strip().lstrip('-').lstrip('*').lstrip('123456789.').strip()
            if line and len(line) > 5:
                questions.append(line)
        return questions

    def _build_discussion_prompt(self) -> str:
        """Build prompt for agents to discuss together.

        Now includes consolidated opinions (post-daemon-debate) for richer discussion.
        """
        perspectives_summary = "\n".join([
            f"- {name} (pós-debate com daemon): {p.get('consolidated_opinion', p.get('recommendation', 'Indisponível'))[:120]}"
            for name, p in self.agent_perspectives.items()
        ])

        return f"""Os agentes estão agora tendo uma discussão aberta sobre o caso de negócio:
{self.business_case.get('project_name')}

Posições consolidadas (após debate interno com daemons):
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
        """Extract key points from reasoning text, avoiding the first lines."""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # Skip first 2 lines to avoid repeating the "intro" which user complained about
        meaningful_lines = [l for l in lines[2:] if len(l) > 30]
        if not meaningful_lines: meaningful_lines = lines # fallback
        return meaningful_lines[:3]

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

        # Show reasoning with word wrap and duplicate detection
        reasoning_lines = [l.strip() for l in reasoning.split('\n') if l.strip()]
        unique_lines = []
        for l in reasoning_lines:
            if l not in unique_lines:
                unique_lines.append(l)

        print(f"   │ 💭 RACIOCÍNIO:                                          │")
        for line in unique_lines[:5]:  # Show first 5 unique lines
            wrapped_line = line[:62] if len(line) > 62 else line
            print(f"   │    {wrapped_line:<62}│")
        if len(unique_lines) > 5:
            print(f"   │    ... ({len(unique_lines)-5} mais linhas)               │")

        # Show key points
        if key_points:
            print(f"   │                                                        │")
            print(f"   │ 🎯 PONTOS-CHAVE:                                       │")
            for point in key_points[:3]:
                wrapped_point = point[:58] if len(point) > 58 else point
                print(f"   │    • {wrapped_point:<60}│")

        # Show recommendation and confidence
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
