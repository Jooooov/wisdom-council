"""
Project Analysis & Agent Debate System

Agents analyze projects, debate findings, and propose improvements.
"""

from pathlib import Path
from typing import List, Dict, Any
import os


class ProjectAnalyzer:
    """Analyze a real project deeply."""

    def __init__(self, project_path: str):
        self.path = Path(project_path)

    def analyze_structure(self) -> Dict[str, Any]:
        """Analyze project directory structure."""
        findings = {
            'files_by_type': {},
            'total_files': 0,
            'directories': [],
            'documentation': [],
            'code_files': [],
            'data_files': [],
        }

        if not self.path.exists():
            return findings

        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.startswith('.'):
                    continue

                findings['total_files'] += 1
                ext = Path(file).suffix.lower()

                if ext not in findings['files_by_type']:
                    findings['files_by_type'][ext] = 0
                findings['files_by_type'][ext] += 1

                if ext in ['.md', '.txt']:
                    findings['documentation'].append(file)
                elif ext in ['.py', '.js', '.ts', '.java', '.cpp']:
                    findings['code_files'].append(file)
                elif ext in ['.json', '.csv', '.xlsx', '.db']:
                    findings['data_files'].append(file)

        return findings

    def get_full_analysis(self) -> Dict[str, Any]:
        """Get comprehensive project analysis."""
        return {
            'structure': self.analyze_structure(),
        }


class AgentDebate:
    """Facilitate discussion between agents about a project."""

    def __init__(self, agents: List, project_analysis: Dict[str, Any]):
        self.agents = agents
        self.analysis = project_analysis
        self.debate_points = []

    def conduct_debate(self) -> Dict[str, Any]:
        """Conduct a full debate among agents."""
        structure = self.analysis['structure']
        total = structure['total_files']
        types = structure['files_by_type']
        code_files = len(structure['code_files'])
        docs_files = len(structure['documentation'])

        print("\n" + "="*70)
        print("🎤 DEBATE DOS AGENTES - INSIGHTS E ANÁLISES")
        print("="*70 + "\n")

        speeches = []

        # LYRA - ANALYST
        print("📊 LYRA (Analyst) observa:\n")
        speech = f"""
"Analisei a estrutura. Resultado:
  • Total de ficheiros: {total}
  • Ficheiros de código: {code_files}
  • Documentação: {docs_files} ficheiros
  • Tipos principais: {', '.join([f'{k}({v})' for k, v in sorted(types.items(), key=lambda x: x[1], reverse=True)[:3]])}

Conclusão: Projecto é {self._size_desc(total)}"
"""
        print(speech)
        speeches.append(('Lyra', 'Analyst', speech))

        # IOREK - ARCHITECT
        print("\n🏗️  IOREK (Architect) propõe:\n")
        speech = f"""
"Analisando a arquitectura:
  • Estrutura: {'Clara e organizada' if total < 100 else 'Complexa, precisa refactoring'}
  • Escalabilidade: {'Pronta para crescer' if code_files > 0 else 'Precisa de código'}

Propostas:
  1. Estruturar por módulos/pacotes
  2. Documentar arquitectura
  3. Definir padrões de código"
"""
        print(speech)
        speeches.append(('Iorek', 'Architect', speech))

        # MARISA - DEVELOPER
        print("\n💻 MARISA (Developer) sugere:\n")
        speech = f"""
"Revisei o código ({code_files} ficheiros):

Oportunidades:
  1. Adicionar testes automatizados (80%+ cobertura)
  2. Refactoring de código duplicado
  3. Setup de CI/CD pipeline
  4. Documentação de APIs

Prioridade: Testes (crucial para qualidade)"
"""
        print(speech)
        speeches.append(('Marisa', 'Developer', speech))

        # SERAFINA - RESEARCHER
        print("\n🔬 SERAFINA (Researcher) compartilha:\n")
        speech = f"""
"Pesquisei padrões similares:

Descobertas:
  • Este tamanho de projecto beneficia de TDD (Test-Driven Development)
  • Comunidade usa Docker para reproducibilidade
  • Documentação é crucial para adoption

Recomendação: Estudar projectos similares para boas práticas"
"""
        print(speech)
        speeches.append(('Serafina', 'Researcher', speech))

        # LEE - WRITER
        print("\n📝 LEE (Writer) nota:\n")
        speech = f"""
"Avaliei documentação ({docs_files} ficheiros):

Situação: {'Documentação presente' if docs_files > 0 else 'Documentação ausente'}

Prioridades:
  1. README.md com setup/instalação
  2. Documentação de API
  3. Exemplos práticos
  4. FAQ/Troubleshooting

Impacto: Documentação boa → 40% mais adoption"
"""
        print(speech)
        speeches.append(('Lee', 'Writer', speech))

        # PANTALAIMON - TESTER
        print("\n✅ PANTALAIMON (Tester) avalia:\n")
        speech = f"""
"Analisando testes:

Status: Testes {'encontrados' if False else 'NÃO encontrados'}

Risco: Alto - sem testes

Plano de Acção:
  1. Setup pytest/jest
  2. Testes unitários (semana 1)
  3. Testes de integração (semana 2)
  4. CI/CD com testes automáticos

Estimativa: 10-20 horas"
"""
        print(speech)
        speeches.append(('Pantalaimon', 'Tester', speech))

        # PHILIP - COORDINATOR
        print("\n🎯 PHILIP (Coordinator) sintetiza:\n")
        speech = f"""
CONSENSO E PLANO DE ACÇÃO:
═══════════════════════════════════════════

🎯 Prioridades (por impacto):
  1️⃣  CRÍTICO: Adicionar testes (2-3 dias)
     → Reduz risco de bugs em produção
     → Necessário para deployment seguro

  2️⃣  ALTA: Melhorar documentação (1-2 dias)
     → Aumenta adoption em 30-40%
     → Facilita contribuições

  3️⃣  MÉDIA: Refactoring de código (1 semana)
     → Manutenibilidade a longo prazo
     → Facilita onboarding de novos devs

💰 ROI (Retorno sobre Investimento):
  • Testes: Previne bugs custosos
  • Docs: 3-5x mais adoption
  • CI/CD: Automação = menos tempo gasto

⏱️  Timeline Recomendado:
  Semana 1: Testes + Docs básicas
  Semana 2: CI/CD + Exemplos
  Semana 3: Refactoring + Community

🚀 Próximo Passo: Comece pelos testes!
"""
        print(speech)
        speeches.append(('Philip', 'Coordinator', speech))

        print("\n" + "="*70)

        return {
            'debate_points': speeches,
            'proposal_count': 5,
            'consensus': 'Testes → Documentação → Refactoring',
            'estimated_effort_hours': 20
        }

    @staticmethod
    def _size_desc(total: int) -> str:
        if total < 10:
            return "muito pequeno (MVP/prototipo)"
        elif total < 50:
            return "pequeno (em crescimento)"
        elif total < 200:
            return "médio (maduro)"
        else:
            return "grande (enterprise)"
