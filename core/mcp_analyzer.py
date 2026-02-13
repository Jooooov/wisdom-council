"""
Real Analysis Engine using MCPs + Local MLX
- MLX (Qwen3): Local code analysis via mlx_lm
- Perplexity MCP: Web research for context (port 3007)
- Obsidian MCP: Save insights and findings (port 3001)
- Paper Search MCP: Academic papers (port 3003)
"""

import httpx
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# MCP Endpoints
PERPLEXITY_MCP = "http://localhost:3007"  # Web research
OBSIDIAN_MCP = "http://localhost:3001"  # Knowledge base
PAPER_SEARCH_MCP = "http://localhost:3003"  # Academic papers

# MLX Local LLM
try:
    from mlx_lm import load, generate
    MLX_MODEL = None  # Will be loaded on demand
    MLX_AVAILABLE = True
except ImportError:
    logger.warning("MLX not available, install with: pip install mlx-lm")
    MLX_AVAILABLE = False


class MCPAnalyzer:
    """Real analysis using MLX + MCPs"""

    def __init__(self):
        self.mlx_available = MLX_AVAILABLE
        self.perplexity_available = False
        self.obsidian_available = False
        self.paper_search_available = False
        self._check_mcps()

    async def _check_mcps(self):
        """Verify which MCPs are running"""
        try:
            async with httpx.AsyncClient() as client:
                # Check Perplexity MCP (3007)
                try:
                    await client.get(f"{PERPLEXITY_MCP}/health", timeout=2)
                    self.perplexity_available = True
                    logger.info("✅ Perplexity MCP available (port 3007)")
                except:
                    logger.warning("⚠️  Perplexity MCP not available (port 3007)")

                # Check Obsidian MCP (3001)
                try:
                    await client.get(f"{OBSIDIAN_MCP}/health", timeout=2)
                    self.obsidian_available = True
                    logger.info("✅ Obsidian MCP available (port 3001)")
                except:
                    logger.warning("⚠️  Obsidian MCP not available (port 3001)")

                # Check Paper Search MCP (3003)
                try:
                    await client.get(f"{PAPER_SEARCH_MCP}/health", timeout=2)
                    self.paper_search_available = True
                    logger.info("✅ Paper Search MCP available (port 3003)")
                except:
                    logger.warning("⚠️  Paper Search MCP not available (port 3003)")

                if self.mlx_available:
                    logger.info("✅ MLX (Local LLM) available")
        except Exception as e:
            logger.error(f"Error checking MCPs: {e}")

    async def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single code file using local MLX LLM"""
        if not self.mlx_available:
            return {"error": "MLX (Local LLM) not available"}

        try:
            with open(file_path, 'r') as f:
                code = f.read()

            # Truncate code if too large (prevent token overflow)
            if len(code) > 4000:
                code = code[:4000] + "\n... [truncated] ..."

            # Use MLX for local analysis
            prompt = f"""Analisa este código Python e identifica (JSON):

CÓDIGO:
```python
{code}
```

ANÁLISE (responde em JSON):
{{
  "file": "{file_path}",
  "issues": [
    {{"type": "performance", "severity": "high", "description": "...", "fix": "..."}}
  ],
  "summary": "Descrição breve",
  "actionable_fixes": ["Fix 1", "Fix 2"]
}}"""

            # Call MLX for analysis
            analysis = await self._call_mlx_local(prompt)

            # Try to parse JSON from response
            try:
                # Extract JSON from response if wrapped in markdown
                if "```json" in analysis:
                    json_str = analysis.split("```json")[1].split("```")[0].strip()
                elif "```" in analysis:
                    json_str = analysis.split("```")[1].split("```")[0].strip()
                else:
                    json_str = analysis

                return json.loads(json_str)
            except:
                # Return raw analysis if not valid JSON
                return {"analysis": analysis, "file": file_path}

        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {e}")
            return {"error": f"Analysis failed: {e}"}

    async def _call_mlx_local(self, prompt: str) -> str:
        """Call MLX LLM locally for analysis"""
        if not self.mlx_available:
            return "MLX not available"

        try:
            # Run MLX in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_mlx_sync,
                prompt
            )
            return result
        except Exception as e:
            logger.error(f"MLX call failed: {e}")
            return f"Error: {e}"

    def _run_mlx_sync(self, prompt: str) -> str:
        """Synchronous MLX call"""
        try:
            global MLX_MODEL
            if MLX_MODEL is None:
                # Load model on first use
                print("🔄 Loading Qwen3 model (this may take a moment)...")
                MLX_MODEL = load("mlx-community/Qwen2.5-0.5B-4bit")

            # Generate response
            response = generate(
                MLX_MODEL,
                prompt,
                max_tokens=1000,
                temperature=0.7
            )
            return response
        except Exception as e:
            logger.error(f"MLX sync failed: {e}")
            return f"Error: {e}"

    async def search_context(self, project_name: str, query: str) -> Dict[str, Any]:
        """Search for context using Perplexity MCP (port 3007)"""
        if not self.perplexity_available:
            logger.warning("Perplexity MCP not available for search")
            return {"error": "Perplexity MCP not available"}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{PERPLEXITY_MCP}/search",
                    json={
                        "query": query,
                        "context": project_name,
                        "format": "summary"
                    }
                )
                result = response.json()
                logger.info(f"✅ Found research context for: {query}")
                return result
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {"error": f"Search failed: {e}"}

    async def analyze_project_real(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Complete real analysis of a project"""
        findings = {
            "project": project_name,
            "files_analyzed": [],
            "total_issues": 0,
            "critical_problems": [],
            "performance_issues": [],
            "actionable_fixes": [],
            "estimated_effort": {},
        }

        project_path = Path(project_path)

        # 1. Analyze all Python files
        print(f"\n🔍 Analyzing code files in {project_name}...")
        py_files = list(project_path.glob("**/*.py"))[:10]  # Limit to first 10

        for py_file in py_files:
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            print(f"  📄 Analyzing {py_file.name}...")
            analysis = await self.analyze_code_file(str(py_file))

            if "error" not in analysis:
                findings["files_analyzed"].append({
                    "file": py_file.name,
                    "issues": analysis.get("issues", []),
                    "recommendations": analysis.get("recommendations", [])
                })

        # 2. Search for context/best practices
        print(f"\n🔎 Researching best practices for {project_name}...")
        context = await self.search_context(
            project_name,
            f"Best practices for {project_name} architecture"
        )
        findings["research_context"] = context

        # 3. Identify critical issues
        for file_analysis in findings["files_analyzed"]:
            for issue in file_analysis.get("issues", []):
                if issue.get("severity") == "critical":
                    findings["critical_problems"].append({
                        "file": file_analysis["file"],
                        "issue": issue
                    })
                if "performance" in issue.get("type", "").lower():
                    findings["performance_issues"].append({
                        "file": file_analysis["file"],
                        "issue": issue
                    })

        # 4. Generate actionable fixes
        findings["actionable_fixes"] = self._generate_actionable_fixes(findings)

        return findings

    def _generate_actionable_fixes(self, findings: Dict) -> List[Dict]:
        """Convert findings into actionable fixes"""
        fixes = []

        for issue in findings.get("critical_problems", []):
            fixes.append({
                "problem": issue["issue"]["description"],
                "file": issue["file"],
                "severity": "HIGH",
                "fix_description": issue["issue"].get("recommended_fix"),
                "estimated_time": issue["issue"].get("estimated_fix_time", "1-2 hours")
            })

        for issue in findings.get("performance_issues", []):
            fixes.append({
                "problem": f"Performance: {issue['issue']['description']}",
                "file": issue["file"],
                "severity": "MEDIUM",
                "fix_description": issue["issue"].get("optimization_strategy"),
                "estimated_time": issue["issue"].get("estimated_fix_time", "2-4 hours")
            })

        return fixes

    async def save_to_obsidian(self, findings: Dict) -> bool:
        """Save findings to Obsidian vault via MCP (port 3001)"""
        if not self.obsidian_available:
            logger.warning("Obsidian MCP not available (port 3001), skipping save")
            return False

        try:
            # Format findings as markdown
            markdown = self._format_findings_markdown(findings)

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{OBSIDIAN_MCP}/write",
                    json={
                        "filename": f"RealAnalysis/{findings['project']}_analysis.md",
                        "content": markdown
                    }
                )
                result = response.json().get("success", False)
                if result:
                    logger.info(f"✅ Saved analysis to Obsidian: {findings['project']}")
                return result
        except Exception as e:
            logger.error(f"Failed to save to Obsidian: {e}")
            return False

    def _format_findings_markdown(self, findings: Dict) -> str:
        """Format findings as markdown for Obsidian"""
        md = f"""# 🔍 Real Analysis: {findings['project']}
**Date:** {Path.cwd()}
**Status:** Real code analysis with actionable insights

## Summary
- Files analyzed: {len(findings['files_analyzed'])}
- Critical issues: {len(findings['critical_problems'])}
- Performance issues: {len(findings['performance_issues'])}
- Actionable fixes: {len(findings['actionable_fixes'])}

## Critical Problems
"""
        for problem in findings.get("critical_problems", []):
            md += f"\n### {problem['file']}\n"
            md += f"**Issue:** {problem['issue'].get('description', 'Unknown')}\n"
            md += f"**Severity:** 🔴 CRITICAL\n"

        md += "\n## Actionable Fixes (THIS WEEK)\n"
        for fix in findings.get("actionable_fixes", [])[:5]:
            md += f"""
### {fix['problem']}
- **File:** {fix['file']}
- **Severity:** {fix['severity']}
- **Estimated Time:** {fix['estimated_time']}
- **Fix:** {fix['fix_description']}
"""

        return md


def get_mcp_analyzer() -> MCPAnalyzer:
    """Factory function for MCPAnalyzer"""
    return MCPAnalyzer()
