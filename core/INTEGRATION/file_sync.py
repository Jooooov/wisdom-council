"""
File Sync - Integração com Obsidian e projectos locais.

APENAS PROJECTOS REAIS:
- Obsidian: Pastas em "1 - Projectos/"
- Apps: Pastas com .git/ ou estrutura de código
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProjectFinder:
    """Encontra e lê APENAS projectos reais de ficheiros locais."""

    def __init__(self):
        """Initialize project finder."""
        # Caminhos corretos
        self.obsidian_projects_path = Path.home() / "Obsidian-Vault" / "1 - Projectos"
        self.apps_path = Path.home() / "Desktop" / "Apps"
        self.projects = []

    def find_all_projects(self) -> List[Dict[str, Any]]:
        """Encontra APENAS projectos reais."""
        self.projects = []
        seen_paths = set()  # Para evitar duplicados

        # Procura em Obsidian (apenas em 1 - Projectos)
        self._scan_obsidian_projects(seen_paths)

        # Procura em Apps (apenas projectos com código/git)
        self._scan_apps_projects(seen_paths)

        return self.projects

    def _scan_obsidian_projects(self, seen_paths: set):
        """Procura projectos em Obsidian - APENAS pasta '1 - Projectos'."""
        if not self.obsidian_projects_path.exists():
            logger.warning(f"Obsidian projects path not found: {self.obsidian_projects_path}")
            return

        try:
            # Procura APENAS as pastas diretas em "1 - Projectos"
            for project_dir in self.obsidian_projects_path.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    real_path = str(project_dir.resolve())
                    if real_path not in seen_paths:
                        seen_paths.add(real_path)
                        project = self._read_obsidian_project(project_dir)
                        if project:
                            self.projects.append(project)

            logger.info(f"Found {len([p for p in self.projects if p['source'] == 'Obsidian'])} real projects in Obsidian")

        except Exception as e:
            logger.error(f"Error scanning Obsidian: {e}")

    def _scan_apps_projects(self, seen_paths: set):
        """Procura projectos em Apps - APENAS com estrutura de código."""
        if not self.apps_path.exists():
            logger.warning(f"Apps path not found: {self.apps_path}")
            return

        try:
            # Procura pastas de projectos
            for item in self.apps_path.iterdir():
                if not item.is_dir():
                    continue
                if item.name.startswith('.'):
                    continue

                # Descartar: backups, apps compiladas, pastas de tarefas
                if self._should_exclude_folder(item.name):
                    continue

                # Evitar duplicados
                real_path = str(item.resolve())
                if real_path in seen_paths:
                    continue
                seen_paths.add(real_path)

                # Verificar se é um projecto real
                if self._is_real_project(item):
                    project = self._read_app_project(item)
                    if project:
                        self.projects.append(project)

            logger.info(f"Found {len([p for p in self.projects if p['source'] == 'Apps'])} real projects in Apps")

        except Exception as e:
            logger.error(f"Error scanning Apps: {e}")

    def _should_exclude_folder(self, folder_name: str) -> bool:
        """Determina se uma pasta deve ser excluída."""
        # Excluir aplicações compiladas
        if folder_name.endswith('.app'):
            return True

        # Excluir backups
        if 'BACKUP' in folder_name.upper() or 'backup' in folder_name:
            return True

        # Excluir pastas de tarefas/planos
        if 'To-do' in folder_name or 'Todo' in folder_name or 'todo' in folder_name:
            return True

        # Excluir pastas de sistema
        if folder_name in ['venv', 'node_modules', '__pycache__', '.git', '.vscode']:
            return True

        return False

    def _is_real_project(self, folder_path: Path) -> bool:
        """Verifica se a pasta é um projecto real."""
        # Critério 1: Tem .git (repositório)
        if (folder_path / ".git").exists():
            return True

        # Critério 2: Tem documentação do projecto
        doc_files = [
            "README.md", "PROJECT_CONTEXT.md", "INDEX.md",
            "ARCHITECTURE.md", "project.md", "readme.md"
        ]
        for doc in doc_files:
            if (folder_path / doc).exists():
                return True

        # Critério 3: Tem pasta de código comum
        code_dirs = [
            "src", "code", "lib", "main", "app",
            "crystal_ball", "mundo_barbaro", "wisdom",
            "client", "server", "backend", "frontend"
        ]
        for code_dir in code_dirs:
            if (folder_path / code_dir).exists():
                return True

        # Critério 4: Tem requirements.txt ou package.json (indica código Python ou Node)
        if (folder_path / "requirements.txt").exists() or (folder_path / "package.json").exists():
            return True

        return False

    def _read_obsidian_project(self, folder_path: Path) -> Optional[Dict[str, Any]]:
        """Lê um projecto de Obsidian (pasta em 1 - Projectos)."""
        try:
            title = folder_path.name

            # Contar ficheiros e pastas para descrição
            md_files = list(folder_path.glob("**/*.md"))
            subfolders = [d for d in folder_path.iterdir() if d.is_dir()]

            description = f"Projecto Obsidian com {len(subfolders)} sub-pastas e {len(md_files)} ficheiros"

            # Tentar encontrar arquivo README ou INDEX
            content_sample = ""
            for readme in ["README.md", "INDEX.md", "project.md"]:
                readme_path = folder_path / readme
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content_sample = f.read()[:500]
                    break

            return {
                "title": title,
                "description": description,
                "source": "Obsidian",
                "path": str(folder_path),
                "type": "obsidian_project",
                "content_sample": content_sample,
                "created": datetime.fromtimestamp(folder_path.stat().st_birthtime).isoformat(),
                "modified": datetime.fromtimestamp(folder_path.stat().st_mtime).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error reading Obsidian project: {e}")
            return None

    def _read_app_project(self, folder_path: Path) -> Optional[Dict[str, Any]]:
        """Lê um projecto de Apps."""
        try:
            title = folder_path.name
            description = "Projecto local"
            content_sample = ""
            resources = []
            outputs_path = None

            # Procura README ou PROJECT_CONTEXT
            for readme in ["README.md", "PROJECT_CONTEXT.md", "INDEX.md", "project.md", "readme.md"]:
                readme_path = folder_path / readme
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        full_content = f.read()
                        # Primeira linha como descrição
                        lines = full_content.split('\n')
                        for line in lines:
                            if line.strip() and not line.startswith('#'):
                                description = line.strip()[:150]
                                break
                        content_sample = full_content[:500]
                    break

            # Se não tem README, usar estatísticas
            if description == "Projecto local":
                py_files = len(list(folder_path.glob("**/*.py")))
                js_files = len(list(folder_path.glob("**/*.js")))
                md_files = len(list(folder_path.glob("**/*.md")))
                if py_files > 0 or js_files > 0 or md_files > 0:
                    description = f"Código: {py_files}×.py, {js_files}×.js, {md_files}×.md"

            # Procurar recursos/outputs do projecto
            # Suporta: OUTPUT, outputs, resources, data, results, etc.
            possible_resource_dirs = ["OUTPUT", "outputs", "resources", "data", "results", "data_export"]
            for resource_dir_name in possible_resource_dirs:
                resource_path = folder_path / resource_dir_name
                if resource_path.exists() and resource_path.is_dir():
                    outputs_path = str(resource_path)
                    # Contar ficheiros nos outputs
                    output_files = list(resource_path.glob("**/*"))
                    if output_files:
                        resources = [str(f.relative_to(resource_path)) for f in output_files if f.is_file()][:20]
                    break

            project_dict = {
                "title": title,
                "description": description,
                "source": "Apps",
                "path": str(folder_path),
                "type": "app_project",
                "content_sample": content_sample,
                "created": datetime.fromtimestamp(folder_path.stat().st_birthtime).isoformat(),
                "modified": datetime.fromtimestamp(folder_path.stat().st_mtime).isoformat(),
            }

            # Adicionar recursos se existem
            if outputs_path:
                project_dict["outputs_path"] = outputs_path
                project_dict["resources"] = resources
                project_dict["has_outputs"] = True
            else:
                project_dict["has_outputs"] = False

            return project_dict

        except Exception as e:
            logger.error(f"Error reading App project {folder_path.name}: {e}")
            return None

    def search_projects(self, query: str) -> List[Dict[str, Any]]:
        """Procura projectos por nome ou descrição."""
        query_lower = query.lower()
        results = []

        for project in self.projects:
            title_match = query_lower in project['title'].lower()
            desc_match = query_lower in project['description'].lower()

            if title_match or desc_match:
                results.append(project)

        return results

    def get_projects_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Retorna projectos de uma fonte específica (Obsidian ou Apps)."""
        return [p for p in self.projects if p['source'] == source]


class ProjectSync:
    """Sincroniza projectos com o sistema de intake."""

    def sync_all(self, intake) -> Dict[str, int]:
        """Sincroniza TODOS os projectos reais."""
        finder = ProjectFinder()
        finder.find_all_projects()

        obsidian_count = 0
        apps_count = 0

        for project in finder.projects:
            try:
                # Adicionar ao intake
                project_id = intake.accept_project(
                    title=project['title'],
                    brief=project['description'],
                    requirements=["analysis", "development", "documentation"]
                )

                if project['source'] == "Obsidian":
                    obsidian_count += 1
                else:
                    apps_count += 1

            except Exception as e:
                logger.error(f"Error syncing project {project['title']}: {e}")

        return {
            "obsidian": obsidian_count,
            "apps": apps_count,
            "total": obsidian_count + apps_count
        }


# Singleton factory functions
_project_finder = None
_project_sync = None


def get_project_finder() -> ProjectFinder:
    """Get or create ProjectFinder instance."""
    global _project_finder
    if _project_finder is None:
        _project_finder = ProjectFinder()
    return _project_finder


def get_project_sync() -> ProjectSync:
    """Get or create ProjectSync instance."""
    global _project_sync
    if _project_sync is None:
        _project_sync = ProjectSync()
    return _project_sync
