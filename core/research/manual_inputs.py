"""
Manual Inputs Reader - Incorporates user-provided context into analysis

Reads from project's "manual_inputs" or "manual inputs" folder
to gather critical context that agents should consider.
"""

from pathlib import Path
from typing import Dict, List, Any


class ManualInputsReader:
    """Reads and incorporates manual inputs from project directories."""

    def __init__(self, project_path: str):
        """Initialize reader."""
        self.project_path = Path(project_path)
        self.inputs = {
            "raw_files": [],
            "context": "",
            "objectives": [],
            "constraints": [],
            "critical_points": [],
            "user_notes": ""
        }

    def read_inputs(self) -> Dict[str, Any]:
        """Read all manual inputs from project."""
        print("\n🔍 Buscando manual inputs (contexto crítico)...")

        # Try different folder names
        possible_names = [
            "manual_inputs",
            "manual inputs",
            "inputs",
            "manual",
            "context",
            "MANUAL_INPUTS",
            "MANUAL INPUTS"
        ]

        inputs_folder = None
        for name in possible_names:
            candidate = self.project_path / name
            if candidate.exists() and candidate.is_dir():
                inputs_folder = candidate
                break

        if not inputs_folder:
            print("   ℹ️  Nenhuma pasta de manual inputs encontrada")
            return self.inputs

        print(f"   ✅ Pasta encontrada: {inputs_folder.name}")

        # Read all files in the folder
        self._read_folder_contents(inputs_folder)

        print(f"   ✅ Lidos {len(self.inputs['raw_files'])} ficheiros")

        return self.inputs

    def _read_folder_contents(self, folder: Path):
        """Read all files from the inputs folder."""
        try:
            for file_path in folder.rglob("*"):
                if not file_path.is_file():
                    continue

                if file_path.suffix in [".md", ".txt", ".json", ".csv", ".yaml", ".yml"]:
                    content = self._read_file(file_path)
                    if content:
                        self.inputs["raw_files"].append({
                            "filename": file_path.name,
                            "content": content
                        })

                        # Parse content for structured data
                        self._parse_content(file_path.name, content)

        except Exception as e:
            print(f"   ⚠️  Erro ao ler inputs: {e}")

    def _read_file(self, file_path: Path) -> str:
        """Read a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"   ⚠️  Erro ao ler {file_path.name}: {e}")
            return ""

    def _parse_content(self, filename: str, content: str):
        """Parse content to extract structured information."""
        # Extract objectives
        if "objetivo" in filename.lower() or "goal" in filename.lower():
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            self.inputs["objectives"].extend(lines[:5])

        # Extract constraints
        if "constraint" in filename.lower() or "restrição" in filename.lower():
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            self.inputs["constraints"].extend(lines[:5])

        # Extract critical points
        if "critical" in filename.lower() or "importante" in filename.lower():
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            self.inputs["critical_points"].extend(lines[:5])

        # Accumulate full context
        self.inputs["user_notes"] += f"\n## {filename}\n{content}\n"

    def get_context_for_agent(self) -> str:
        """Get formatted context to include in agent prompts."""
        if not self.inputs["raw_files"]:
            return ""

        context = """
=== CONTEXTO CRÍTICO DO UTILIZADOR ===
(Informação fornecida manualmente - TEM PRIORIDADE MÁXIMA)

"""

        if self.inputs["objectives"]:
            context += "📍 OBJECTIVOS:\n"
            for obj in self.inputs["objectives"][:3]:
                context += f"  • {obj}\n"
            context += "\n"

        if self.inputs["constraints"]:
            context += "⚠️  RESTRIÇÕES/LIMITAÇÕES:\n"
            for cons in self.inputs["constraints"][:3]:
                context += f"  • {cons}\n"
            context += "\n"

        if self.inputs["critical_points"]:
            context += "🔴 PONTOS CRÍTICOS:\n"
            for point in self.inputs["critical_points"][:3]:
                context += f"  • {point}\n"
            context += "\n"

        context += "📝 NOTAS COMPLETAS DO UTILIZADOR:\n"
        context += self.inputs["user_notes"][:2000]  # Limit to 2000 chars

        return context

    def get_summary(self) -> str:
        """Get summary of inputs for display."""
        if not self.inputs["raw_files"]:
            return "Sem inputs manuais encontrados"

        summary = f"Inputs encontrados ({len(self.inputs['raw_files'])} ficheiros):\n"
        for file_info in self.inputs["raw_files"]:
            summary += f"  • {file_info['filename']} ({len(file_info['content'])} chars)\n"

        return summary


def read_manual_inputs(project_path: str) -> Dict[str, Any]:
    """Factory function to read manual inputs."""
    reader = ManualInputsReader(project_path)
    return reader.read_inputs()


def get_context_for_agent(project_path: str) -> str:
    """Get formatted context from manual inputs."""
    reader = ManualInputsReader(project_path)
    reader.read_inputs()
    return reader.get_context_for_agent()
