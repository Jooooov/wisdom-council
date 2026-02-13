"""
Project Context Analyzer
- Determines project type (business, software, research, etc)
- Extracts objectives and structure
- Identifies if business analysis needed
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import re


class ContextAnalyzer:
    """Analyzes project context to determine type and objectives."""

    def __init__(self, project_path: str, project_name: str):
        self.project_path = Path(project_path)
        self.project_name = project_name
        self.context = {
            "project_name": project_name,
            "project_type": None,
            "is_business": False,
            "objectives": [],
            "structure": {},
            "files_found": {},
            "indicators": {}
        }

    async def analyze(self) -> Dict[str, Any]:
        """Analyze project context."""
        print(f"\n📊 ANALYZING PROJECT CONTEXT: {self.project_name}")
        print("-" * 70)

        # Step 1: Read documentation
        print("📖 Reading documentation...")
        self._read_documentation()

        # Step 2: Analyze structure
        print("🏗️  Analyzing project structure...")
        self._analyze_structure()

        # Step 3: Detect project type
        print("🔍 Detecting project type...")
        self._detect_project_type()

        # Step 4: Check if business
        print("💼 Checking if business project...")
        self._check_if_business()

        return self.context

    def _read_documentation(self):
        """Read README and other documentation."""
        readme_files = [
            "README.md",
            "readme.md",
            "README.txt",
            "ABOUT.md",
        ]

        for readme in readme_files:
            readme_path = self.project_path / readme
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.context["files_found"]["readme"] = readme
                        self._extract_objectives(content)
                except:
                    pass
                break

        # Also check for .md files in root
        md_files = list(self.project_path.glob("*.md"))[:3]
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self._extract_objectives(content)
            except:
                pass

    def _extract_objectives(self, content: str):
        """Extract objectives from documentation."""
        # Look for common patterns
        patterns = [
            r"(?:Objective|Objectives|Goal|Goals|Purpose).*?[:]\s*(.+?)(?:\n\n|\n-)",
            r"(?:This project|This app|This system).*?(?:is|does|provides).*?:?\s*(.+?)(?:\n|\.|$)",
            r"(?:Description|About|What).*?[:]\s*(.+?)(?:\n\n|\n-)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                text = match.strip()[:200]  # First 200 chars
                if text and text not in self.context["objectives"]:
                    self.context["objectives"].append(text)

    def _analyze_structure(self):
        """Analyze project structure."""
        structure = {
            "python_files": 0,
            "javascript_files": 0,
            "config_files": 0,
            "documentation_files": 0,
            "test_files": 0,
            "directories": []
        }

        # Count file types
        py_files = list(self.project_path.glob("**/*.py"))
        js_files = list(self.project_path.glob("**/*.js"))

        # Config files (multiple extensions)
        config_files = []
        for ext in ['yaml', 'yml', 'json', 'toml', 'ini']:
            config_files.extend(self.project_path.glob(f"**/*.{ext}"))

        doc_files = list(self.project_path.glob("**/*.md"))
        test_files = [f for f in py_files if 'test' in f.name]

        structure["python_files"] = len([f for f in py_files if ".venv" not in str(f) and "__pycache__" not in str(f)])
        structure["javascript_files"] = len(js_files)
        structure["config_files"] = len(config_files)
        structure["documentation_files"] = len(doc_files)
        structure["test_files"] = len(test_files)

        # Get main directories
        structure["directories"] = [
            d.name for d in self.project_path.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ][:10]

        self.context["structure"] = structure

    def _detect_project_type(self):
        """Detect what type of project this is."""
        indicators = {
            "is_web_app": False,
            "is_api": False,
            "is_data_tool": False,
            "is_ml_tool": False,
            "is_cli_tool": False,
            "is_library": False,
            "is_business_app": False,
            "is_research": False,
        }

        structure = self.context["structure"]
        docs = "\n".join(self.context["objectives"]).lower()

        # Check for web app indicators
        if any(x in docs for x in ["web", "frontend", "react", "vue", "django", "flask"]):
            indicators["is_web_app"] = True

        # Check for API indicators
        if any(x in docs for x in ["api", "rest", "endpoint", "fastapi", "flask"]):
            indicators["is_api"] = True

        # Check for data tool
        if any(x in docs for x in ["data", "analytics", "dashboard", "database", "sql"]):
            indicators["is_data_tool"] = True

        # Check for ML
        if any(x in docs for x in ["ml", "machine learning", "model", "ai", "pytorch", "tensorflow"]):
            indicators["is_ml_tool"] = True

        # Check for CLI
        if any(x in docs for x in ["cli", "command", "terminal", "script"]):
            indicators["is_cli_tool"] = True

        # Check for library
        if any(x in docs for x in ["library", "module", "sdk", "package"]):
            indicators["is_library"] = True

        # Check for business app
        if any(x in docs for x in ["business", "crm", "erp", "invoic", "payment", "ecommerce"]):
            indicators["is_business_app"] = True

        # Check for research
        if any(x in docs for x in ["research", "study", "analysis", "experiment"]):
            indicators["is_research"] = True

        self.context["indicators"] = indicators

        # Determine primary type
        if indicators["is_business_app"]:
            self.context["project_type"] = "BUSINESS"
        elif indicators["is_ml_tool"]:
            self.context["project_type"] = "ML_TOOL"
        elif indicators["is_api"]:
            self.context["project_type"] = "API"
        elif indicators["is_web_app"]:
            self.context["project_type"] = "WEB_APP"
        elif indicators["is_data_tool"]:
            self.context["project_type"] = "DATA_TOOL"
        elif indicators["is_cli_tool"]:
            self.context["project_type"] = "CLI_TOOL"
        elif indicators["is_research"]:
            self.context["project_type"] = "RESEARCH"
        else:
            self.context["project_type"] = "SOFTWARE"

    def _check_if_business(self):
        """Check if this is a business project that needs market analysis."""
        # Business if:
        # 1. Explicitly marked as business app
        # 2. Has business-related objectives
        # 3. Project name suggests it's a product/service

        business_keywords = [
            "business", "product", "service", "startup", "platform",
            "marketplace", "saas", "app", "tool", "solution",
            "crm", "erp", "invoic", "payment", "ecommerce",
            "mundo", "wisdom", "crystal", "reddit"  # Your projects
        ]

        docs = (self.project_name + " " + "\n".join(self.context["objectives"])).lower()

        for keyword in business_keywords:
            if keyword in docs:
                self.context["is_business"] = True
                break

        # If it's marked as BUSINESS type, definitely flag it
        if self.context["project_type"] == "BUSINESS":
            self.context["is_business"] = True


async def get_context(project_path: str, project_name: str) -> Dict[str, Any]:
    """Factory function for context analysis."""
    analyzer = ContextAnalyzer(project_path, project_name)
    return await analyzer.analyze()
