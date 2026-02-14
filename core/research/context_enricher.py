"""
Context Enricher - Enrich project context with file analysis and web research

Reads all project files to understand structure and uses Perplexity to research
industry/business type to provide agents with comprehensive context.
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
import json


class ContextEnricher:
    """Enriches project context by analyzing files and researching industry."""

    def __init__(self, project_path: str):
        """Initialize enricher."""
        self.project_path = Path(project_path)
        self.enriched_context = {
            "files_found": [],
            "key_files": {},
            "project_type": "",
            "industry": "",
            "web_research": "",
            "combined_context": ""
        }

    def analyze_project_files(self) -> Dict[str, Any]:
        """Scan and analyze all project files."""
        print("\n📁 Analisando ficheiros do projeto...")

        if not self.project_path.exists():
            print(f"   ⚠️  Caminho não existe: {self.project_path}")
            return self.enriched_context

        # Scan for important files
        important_extensions = ['.md', '.txt', '.py', '.json', '.yaml', '.yml']
        important_names = [
            'README', 'contexto', 'estrutura', 'config', 'setup',
            'requirements', 'package.json', 'dockerfile', '.env'
        ]

        files_by_type = {}
        total_size = 0

        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue

            # Skip hidden/cache dirs
            if any(part.startswith('.') for part in file_path.parts):
                continue
            if '__pycache__' in str(file_path):
                continue

            # Categorize files
            ext = file_path.suffix.lower()
            name = file_path.name.lower()

            if ext in important_extensions or any(imp in name for imp in important_names):
                file_type = ext or 'other'
                if file_type not in files_by_type:
                    files_by_type[file_type] = []

                try:
                    size = file_path.stat().st_size
                    total_size += size
                    files_by_type[file_type].append({
                        'name': file_path.name,
                        'path': str(file_path.relative_to(self.project_path)),
                        'size': size
                    })
                except Exception as e:
                    pass

        # Store findings
        self.enriched_context['files_found'] = files_by_type
        print(f"   ✅ Encontrados {sum(len(f) for f in files_by_type.values())} ficheiros importantes")
        print(f"   ✅ Tamanho total: {total_size / 1024:.1f} KB")

        # Analyze key files for context
        self._extract_key_information()

        return self.enriched_context

    def _extract_key_information(self):
        """Extract key information from important files."""
        print("\n🔍 Extraindo informação-chave dos ficheiros...")

        # Read contexto.md if exists
        contexto_file = self.project_path / "contexto.md"
        if contexto_file.exists():
            try:
                with open(contexto_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.enriched_context['key_files']['contexto'] = content[:500]  # First 500 chars

                    # Try to extract project type
                    lines = content.split('\n')
                    for line in lines[:20]:
                        if 'tipo' in line.lower() or 'type' in line.lower():
                            self.enriched_context['project_type'] = line.strip()
                            break
            except Exception as e:
                pass

        # Read README if exists
        readme_file = self.project_path / "README.md"
        if readme_file.exists():
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.enriched_context['key_files']['readme'] = content[:500]
            except Exception as e:
                pass

        print("   ✅ Informação extraída")

    async def enrich_with_web_research(self, query: str = None) -> str:
        """Use Perplexity to research industry/business type."""
        if not query:
            query = self._generate_research_query()

        print(f"\n🌐 Pesquisando no Perplexity: {query[:60]}...")

        try:
            # Try to use Perplexity MCP if available
            from core.research.web_researcher import research_with_perplexity

            research = await research_with_perplexity(query)
            self.enriched_context['web_research'] = research
            print("   ✅ Pesquisa concluída")
            return research

        except Exception as e:
            print(f"   ⚠️  Perplexity não disponível: {e}")
            # Fallback to mock research
            return self._generate_mock_research(query)

    def _generate_research_query(self) -> str:
        """Generate intelligent research query from project context."""
        project_type = self.enriched_context.get('project_type', '')
        files = self.enriched_context.get('files_found', {})

        # Extract industry keywords
        keywords = []
        if 'electroplating' in project_type.lower():
            keywords.append('electroplating industry Portugal')
        if 'research' in project_type.lower():
            keywords.append('research methodology best practices')
        if 'scrapper' in str(self.project_path).lower():
            keywords.append('web scraping industry trends')

        if keywords:
            return f"Industry analysis: {keywords[0]}"
        else:
            return f"Project analysis for {self.project_path.name}"

    def _generate_mock_research(self, query: str) -> str:
        """Generate mock research when Perplexity unavailable."""
        return f"""
Pesquisa simulada para: {query}

Nota: Perplexity não está disponível neste momento.
Para enriquecimento completo, configure o MCP do Perplexity.

Recomendações gerais:
- Documentar contexto estratégico do negócio
- Adicionar análise de mercado se disponível
- Incluir requisitos técnicos específicos
- Definir métricas de sucesso
"""

    def get_enriched_context(self) -> str:
        """Get formatted enriched context for agents."""
        context = """
=== CONTEXTO ENRIQUECIDO DO PROJETO ===
(Análise de ficheiros + Pesquisa de indústria)

"""
        # Add files analysis
        if self.enriched_context['files_found']:
            context += "📁 FICHEIROS DO PROJETO:\n"
            for file_type, files in self.enriched_context['files_found'].items():
                context += f"  • {file_type}: {len(files)} ficheiro(s)\n"
                for f in files[:3]:  # Show first 3 of each type
                    context += f"    - {f['name']}\n"
            context += "\n"

        # Add key information
        if self.enriched_context['key_files']:
            context += "🔑 INFORMAÇÃO-CHAVE:\n"
            if 'contexto' in self.enriched_context['key_files']:
                context += "Contexto do projeto:\n"
                context += self.enriched_context['key_files']['contexto'] + "\n\n"

        # Add web research
        if self.enriched_context['web_research']:
            context += "🌐 PESQUISA DE INDÚSTRIA:\n"
            context += self.enriched_context['web_research'] + "\n"

        self.enriched_context['combined_context'] = context
        return context


async def enrich_context(project_path: str, research_query: str = None) -> str:
    """Factory function to enrich project context.

    Args:
        project_path: Path to project
        research_query: Optional custom research query
    """
    enricher = ContextEnricher(project_path)

    # Analyze files
    enricher.analyze_project_files()

    # Enrich with web research
    if research_query:
        await enricher.enrich_with_web_research(research_query)
    else:
        # Auto-generate research query
        query = enricher._generate_research_query()
        await enricher.enrich_with_web_research(query)

    return enricher.get_enriched_context()
