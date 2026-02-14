"""
Context Reader - Reads project contexto.md and estrutura.md from Obsidian and Apps

Follows the convention defined in AGENTS.md:
- Each project has contexto.md (project context)
- Each project has estrutura.md (project structure)
- Agents receive COMBINED context from both sources (Obsidian + Apps)
"""

from pathlib import Path
from typing import Dict, List, Any


class ContextReader:
    """Reads contexto.md and estrutura.md from project directories."""

    def __init__(self, project_path: str, additional_paths: list = None):
        """Initialize reader.

        Args:
            project_path: Primary project path (usually Apps path)
            additional_paths: List of additional paths to search (e.g., Obsidian path for merged projects)
        """
        self.project_path = Path(project_path)
        self.additional_paths = [Path(p) for p in (additional_paths or [])]
        self.all_paths = [self.project_path] + self.additional_paths
        self.contexts = {
            "contexto": [],  # List of (source, content) tuples
            "estrutura": [],  # List of (source, content) tuples
            "combined": ""  # Final combined context
        }

    def read_contexts(self) -> Dict[str, Any]:
        """Read contexto.md and estrutura.md from all project paths."""
        print("\n📚 Lendo contextos do projeto (contexto.md + estrutura.md)...")

        # Search for context files in all paths
        for project_path in self.all_paths:
            if not project_path.exists():
                continue

            source_name = "Obsidian" if project_path != self.project_path else "Apps"

            # Read contexto.md
            contexto_file = project_path / "contexto.md"
            if contexto_file.exists():
                try:
                    with open(contexto_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.contexts["contexto"].append((source_name, content))
                        print(f"   ✅ contexto.md encontrado ({source_name})")
                except Exception as e:
                    print(f"   ⚠️  Erro ao ler contexto.md ({source_name}): {e}")

            # Read estrutura.md
            estrutura_file = project_path / "estrutura.md"
            if estrutura_file.exists():
                try:
                    with open(estrutura_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.contexts["estrutura"].append((source_name, content))
                        print(f"   ✅ estrutura.md encontrado ({source_name})")
                except Exception as e:
                    print(f"   ⚠️  Erro ao ler estrutura.md ({source_name}): {e}")

        # Combine contexts if found any
        if self.contexts["contexto"] or self.contexts["estrutura"]:
            self._combine_contexts()
            print(f"   ✅ Contextos combinados de múltiplas fontes")
        else:
            print("   ℹ️  Nenhum ficheiro de contexto encontrado")

        return self.contexts

    def _combine_contexts(self):
        """Combine contexts from multiple sources into single formatted context."""
        parts = []

        # Combine all contexto.md files
        if self.contexts["contexto"]:
            parts.append("=== CONTEXTO DO PROJETO ===\n")
            for source, content in self.contexts["contexto"]:
                parts.append(f"\n📍 Fonte: {source}\n")
                parts.append(content)
                parts.append("\n")

        # Combine all estrutura.md files
        if self.contexts["estrutura"]:
            parts.append("\n=== ESTRUTURA DO PROJETO ===\n")
            for source, content in self.contexts["estrutura"]:
                parts.append(f"\n🏗️  Fonte: {source}\n")
                parts.append(content)
                parts.append("\n")

        self.contexts["combined"] = "\n".join(parts) if parts else ""

    def get_context_for_agent(self) -> str:
        """Get formatted context to include in agent prompts."""
        if not self.contexts["combined"]:
            return ""

        context = """
=== CONTEXTO CRÍTICO DO PROJETO ===
(Lido de contexto.md + estrutura.md - FONTE PRIMÁRIA)

"""
        context += self.contexts["combined"]
        context += "\n(Fim do contexto do projeto)\n"

        return context

    def get_summary(self) -> str:
        """Get summary of found contexts."""
        if not self.contexts["contexto"] and not self.contexts["estrutura"]:
            return "Sem contexto de projeto encontrado"

        summary = "Contextos encontrados:\n"
        for source, _ in self.contexts["contexto"]:
            summary += f"  • contexto.md ({source})\n"
        for source, _ in self.contexts["estrutura"]:
            summary += f"  • estrutura.md ({source})\n"

        return summary


def read_project_context(project_path: str, additional_paths: list = None) -> Dict[str, Any]:
    """Factory function to read project context.

    Args:
        project_path: Primary project path
        additional_paths: Additional paths to search (e.g., Obsidian path for merged projects)
    """
    reader = ContextReader(project_path, additional_paths)
    return reader.read_contexts()


def get_context_for_agent(project_path: str, additional_paths: list = None) -> str:
    """Get formatted context from project files.

    Args:
        project_path: Primary project path
        additional_paths: Additional paths to search (e.g., Obsidian path for merged projects)
    """
    reader = ContextReader(project_path, additional_paths)
    reader.read_contexts()
    return reader.get_context_for_agent()


# Backwards compatibility - old manual_inputs functions now redirect to context functions
def read_manual_inputs(project_path: str, additional_paths: list = None) -> Dict[str, Any]:
    """Deprecated: Use read_project_context instead."""
    return read_project_context(project_path, additional_paths)
