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

    def __init__(self, project_path: str, obsidian_path: str = None):
        """Initialize enricher.

        Args:
            project_path: Path to project in Apps folder
            obsidian_path: Path to corresponding Obsidian project folder (optional)
        """
        self.project_path = Path(project_path)
        self.obsidian_path = Path(obsidian_path) if obsidian_path else None
        self.enriched_context = {
            "files_found": [],
            "obsidian_files": [],
            "key_files": {},
            "obsidian_content": {},
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
        else:
            # Scan for important files in Apps folder
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
            print(f"   ✅ Encontrados {sum(len(f) for f in files_by_type.values())} ficheiros importantes (Apps)")
            print(f"   ✅ Tamanho total: {total_size / 1024:.1f} KB")

        # Read Obsidian project files if available
        if self.obsidian_path:
            self._read_obsidian_files()

        # Analyze key files for context
        self._extract_key_information()

        return self.enriched_context

    def _read_obsidian_files(self) -> None:
        """Read all markdown files from Obsidian project folder."""
        if not self.obsidian_path or not self.obsidian_path.exists():
            return

        print(f"\n📚 Lendo ficheiros do Obsidian ({self.obsidian_path.name})...")

        obsidian_files = []
        total_chars = 0

        for file_path in self.obsidian_path.glob('*.md'):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                obsidian_files.append({
                    'name': file_path.name,
                    'size': len(content)
                })

                # Store content with attribution
                source_key = f"obsidian_{file_path.stem}"
                self.enriched_context['obsidian_content'][source_key] = {
                    'filename': file_path.name,
                    'content': content
                }

                total_chars += len(content)

            except Exception as e:
                print(f"   ⚠️  Erro ao ler {file_path.name}: {e}")

        self.enriched_context['obsidian_files'] = obsidian_files
        if obsidian_files:
            print(f"   ✅ Lidos {len(obsidian_files)} ficheiros do Obsidian")
            print(f"   ✅ Total: {total_chars:,} caracteres")

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

    async def enrich_with_web_research(self, query: str = None, api_key: str = None) -> str:
        """Use Perplexity to research industry/business type."""
        if not query:
            query = self._generate_research_query()

        print(f"\n🌐 Pesquisando no Perplexity: {query[:60]}...")

        try:
            # Try to use Perplexity API
            from core.research.web_researcher import research_with_perplexity

            research = await research_with_perplexity(query, api_key)
            self.enriched_context['web_research'] = research
            print("   ✅ Pesquisa concluída")
            return research

        except Exception as e:
            print(f"   ⚠️  Perplexity não disponível: {e}")
            # Fallback to mock research
            return self._generate_mock_research(query)

    def _generate_research_query(self) -> str:
        """Generate intelligent research query by analyzing actual project content."""
        keywords = set()

        # Extract keywords from contexto.md
        contexto = self.enriched_context.get('key_files', {}).get('contexto', '')
        if contexto:
            # Extract meaningful keywords from contexto
            lines = contexto.split('\n')
            for line in lines:
                line_lower = line.lower()
                # Look for business type indicators
                if 'company' in line_lower or 'empresa' in line_lower:
                    words = [w.strip('.,;:').lower() for w in line.split()
                            if len(w) > 3 and w.strip('.,;:').lower() not in ['the', 'and', 'that', 'this', 'with', 'from']]
                    keywords.update(words[:5])
                if 'type' in line_lower or 'tipo' in line_lower:
                    words = [w.strip('.,;:').lower() for w in line.split()
                            if len(w) > 4 and w.strip('.,;:').lower() not in ['the', 'type', 'tipo']]
                    keywords.update(words[:3])

        # Extract from project name and files
        project_name = self.project_path.name.lower()
        keywords.add(project_name)

        # Look at file types to infer domain
        files = self.enriched_context.get('files_found', {})
        if '.py' in files:
            keywords.add('software development')
        if '.md' in files:
            keywords.add('documentation')

        # Filter out generic words and build query
        filtered = [k for k in keywords if k and len(k) > 2 and k not in
                   ['the', 'and', 'that', 'this', 'from', 'with', 'for', 'project', 'analysis']]

        if filtered:
            # Build natural language query
            query_terms = filtered[:5]
            query = f"Market analysis and industry trends for: {', '.join(query_terms)}"
        else:
            query = f"Strategic analysis for {project_name}"

        return query

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
(Análise de ficheiros + Obsidian + Pesquisa de indústria)

"""
        # Add files analysis
        if self.enriched_context['files_found']:
            context += "📁 FICHEIROS DO PROJETO (Apps):\n"
            for file_type, files in self.enriched_context['files_found'].items():
                context += f"  • {file_type}: {len(files)} ficheiro(s)\n"
                for f in files[:3]:  # Show first 3 of each type
                    context += f"    - {f['name']}\n"
            context += "\n"

        # Add Obsidian content
        if self.enriched_context['obsidian_content']:
            context += "📚 FICHEIROS DO OBSIDIAN (Contexto Estratégico):\n"
            for key, file_info in self.enriched_context['obsidian_content'].items():
                context += f"\n  📄 {file_info['filename']}:\n"
                # Limit to first 1000 chars to avoid too much context
                content_preview = file_info['content'][:1500]
                for line in content_preview.split('\n'):
                    context += f"    {line}\n"
                if len(file_info['content']) > 1500:
                    context += "    ... (conteúdo truncado)\n"
            context += "\n"

        # Add key information from contexto.md in Apps
        if self.enriched_context['key_files']:
            context += "🔑 INFORMAÇÃO-CHAVE:\n"
            if 'contexto' in self.enriched_context['key_files']:
                context += "Contexto do projeto:\n"
                context += self.enriched_context['key_files']['contexto'] + "\n\n"

        # Add web research
        if self.enriched_context['web_research']:
            context += "🌐 PESQUISA DE INDÚSTRIA (Perplexity):\n"
            context += self.enriched_context['web_research'] + "\n"

        self.enriched_context['combined_context'] = context
        return context


async def enrich_context(project_path: str, obsidian_path: str = None, research_query: str = None, api_key: str = None) -> str:
    """Factory function to enrich project context.

    Args:
        project_path: Path to project in Apps folder
        obsidian_path: Path to corresponding Obsidian project folder (optional)
        research_query: Optional custom research query
        api_key: Perplexity API key (if None, uses environment)
    """
    enricher = ContextEnricher(project_path, obsidian_path)

    # Analyze files
    enricher.analyze_project_files()

    # Enrich with web research
    if research_query:
        await enricher.enrich_with_web_research(research_query, api_key)
    else:
        # Auto-generate research query
        query = enricher._generate_research_query()
        await enricher.enrich_with_web_research(query, api_key)

    return enricher.get_enriched_context()
