"""
MLX Analyzer - Real code analysis using Qwen3 14B via MLX
Provides semantic understanding of code and projects
"""

import logging
import json
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class MLXAnalyzer:
    """Analyzes code and projects using Qwen3 14B MLX."""

    def __init__(self, mlx_loader):
        self.loader = mlx_loader

    async def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single code file with semantic understanding."""

        if not self.loader.is_loaded:
            return {"error": "MLX model not loaded"}

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()

            # Limit code size for analysis (keep tokens reasonable)
            if len(code) > 4000:
                code = code[:4000] + "\n... [code truncated] ...\n"

            prompt = f"""Analyze this Python code file and identify issues, patterns, and improvements:

File: {Path(file_path).name}

```python
{code}
```

Provide analysis:
1. What are the main issues (bugs, inefficiencies, bad practices)?
2. What patterns do you see?
3. What are 3 specific recommendations for improvement?
4. Quality score (0-100)?

Be specific and actionable."""

            response = await self.loader.generate(prompt, max_tokens=150)

            return {
                "file_name": Path(file_path).name,
                "analysis": response,
                "size": len(code)
            }

        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {e}")
            return {"error": f"Analysis failed: {e}", "file_name": Path(file_path).name}

    async def analyze_project(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Analyze entire project with Qwen3 14B."""

        if not self.loader.is_loaded:
            return {"error": "MLX model not loaded"}

        project_path = Path(project_path)
        findings = {
            "project": project_name,
            "model": "Qwen3 14B MLX",
            "files_analyzed": [],
            "analysis_summary": ""
        }

        # Analyze Python files
        print(f"\n🔍 Deep Code Analysis: {project_name}")
        py_files = list(project_path.glob("**/*.py"))[:3]  # Analyze first 3 for speed with MLX
        py_files = [f for f in py_files if ".venv" not in str(f) and "__pycache__" not in str(f)]

        for i, py_file in enumerate(py_files, 1):
            print(f"  [{i}/{len(py_files)}] {py_file.name}...")
            analysis = await self.analyze_code_file(str(py_file))
            findings["files_analyzed"].append(analysis)

        # Generate overall summary
        if findings["files_analyzed"]:
            print(f"\n  📊 Generating project summary...")
            findings["analysis_summary"] = await self._generate_summary(findings)

        logger.info(f"✅ Analysis complete: {len(findings['files_analyzed'])} files analyzed")

        return findings

    async def _generate_summary(self, findings: Dict[str, Any]) -> str:
        """Generate overall project summary."""

        file_summaries = "\n".join([
            f"- {f['file_name']}: {f.get('analysis', 'N/A')[:100]}..."
            for f in findings["files_analyzed"]
        ])

        prompt = f"""Based on these code analyses, provide a brief overall summary:

{file_summaries}

Summary (2-3 sentences max):"""

        try:
            response = await self.loader.generate(prompt, max_tokens=100)
            return response.strip()
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return "Analysis completed but summary generation failed"


async def analyze_with_mlx(
    mlx_loader,
    project_path: str,
    project_name: str
) -> Dict[str, Any]:
    """Factory function for MLX analysis."""

    analyzer = MLXAnalyzer(mlx_loader)
    return await analyzer.analyze_project(project_path, project_name)
