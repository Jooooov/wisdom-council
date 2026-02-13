"""
Integration module - connects to external systems and projects
"""

from .file_sync import get_project_finder, ProjectFinder, ProjectSync

__all__ = ['get_project_finder', 'ProjectFinder', 'ProjectSync']
