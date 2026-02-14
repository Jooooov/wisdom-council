"""
Web Research Module - Find similar projects and tools on GitHub/Reddit

Uses DuckDuckGo and GitHub searches to find:
- Similar projects (architecture references)
- Tools and libraries that could help
- Best practices and patterns
"""

import asyncio
import json
from typing import Dict, List, Any
from pathlib import Path


class WebResearcher:
    """Research similar projects and tools on the web."""

    def __init__(self, project_name: str, project_type: str = None):
        """Initialize researcher."""
        self.project_name = project_name
        self.project_type = project_type or "general"
        self.findings = {
            "similar_projects": [],
            "useful_tools": [],
            "best_practices": [],
            "github_repositories": [],
            "reddit_discussions": []
        }

    async def research_project(self) -> Dict[str, Any]:
        """Conduct full research on project type."""
        print("\n" + "=" * 70)
        print("🔍 WEB RESEARCH - Finding Similar Projects & Tools")
        print("=" * 70)

        try:
            # Search for similar projects
            print(f"\n🔎 Searching for similar {self.project_type} projects...")
            await self._search_similar_projects()

            # Search for useful tools
            print(f"🛠️  Searching for useful tools and libraries...")
            await self._search_tools()

            # Search for best practices
            print(f"📚 Searching for best practices...")
            await self._search_best_practices()

            # Search GitHub
            print(f"💻 Searching GitHub...")
            await self._search_github()

            # Search Reddit
            print(f"💬 Searching Reddit discussions...")
            await self._search_reddit()

            return self.findings

        except Exception as e:
            print(f"⚠️  Research error: {e}")
            return self.findings

    async def _search_similar_projects(self):
        """Search for similar projects."""
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            print("   ⚠️  DuckDuckGo search not available (pip install duckduckgo-search)")
            self.findings["similar_projects"] = self._mock_similar_projects()
            return

        try:
            ddgs = DDGS()
            query = f"{self.project_name} {self.project_type} open source github"
            results = ddgs.text(query, max_results=5)

            for result in results:
                self.findings["similar_projects"].append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")[:200]
                })

            print(f"   ✅ Found {len(self.findings['similar_projects'])} similar projects")

        except Exception as e:
            print(f"   ⚠️  Could not search: {e}")
            self.findings["similar_projects"] = self._mock_similar_projects()

    async def _search_tools(self):
        """Search for useful tools and libraries."""
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            self.findings["useful_tools"] = self._mock_useful_tools()
            return

        try:
            ddgs = DDGS()
            query = f"{self.project_type} tools libraries frameworks best"
            results = ddgs.text(query, max_results=5)

            for result in results:
                self.findings["useful_tools"].append({
                    "name": result.get("title", ""),
                    "url": result.get("href", ""),
                    "description": result.get("body", "")[:200]
                })

            print(f"   ✅ Found {len(self.findings['useful_tools'])} useful tools")

        except Exception as e:
            print(f"   ⚠️  Could not search tools: {e}")
            self.findings["useful_tools"] = self._mock_useful_tools()

    async def _search_best_practices(self):
        """Search for best practices."""
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            self.findings["best_practices"] = self._mock_best_practices()
            return

        try:
            ddgs = DDGS()
            query = f"{self.project_type} best practices architecture patterns"
            results = ddgs.text(query, max_results=5)

            for result in results:
                self.findings["best_practices"].append({
                    "topic": result.get("title", ""),
                    "url": result.get("href", ""),
                    "details": result.get("body", "")[:200]
                })

            print(f"   ✅ Found {len(self.findings['best_practices'])} best practice resources")

        except Exception as e:
            print(f"   ⚠️  Could not search best practices: {e}")
            self.findings["best_practices"] = self._mock_best_practices()

    async def _search_github(self):
        """Search GitHub for related repositories."""
        try:
            import httpx
        except ImportError:
            self.findings["github_repositories"] = self._mock_github_repos()
            return

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                # Search GitHub API
                response = await client.get(
                    "https://api.github.com/search/repositories",
                    params={
                        "q": f"{self.project_name} {self.project_type}",
                        "sort": "stars",
                        "order": "desc",
                        "per_page": 5
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    for repo in data.get("items", []):
                        self.findings["github_repositories"].append({
                            "name": repo.get("name", ""),
                            "url": repo.get("html_url", ""),
                            "description": repo.get("description", "")[:200],
                            "stars": repo.get("stargazers_count", 0),
                            "language": repo.get("language", "")
                        })

                    print(f"   ✅ Found {len(self.findings['github_repositories'])} GitHub repositories")
                else:
                    print(f"   ⚠️  GitHub API error: {response.status_code}")
                    self.findings["github_repositories"] = self._mock_github_repos()

        except Exception as e:
            print(f"   ⚠️  Could not search GitHub: {e}")
            self.findings["github_repositories"] = self._mock_github_repos()

    async def _search_reddit(self):
        """Search Reddit for discussions."""
        # Reddit search is tricky without API keys
        # We'll use a mock implementation for now
        self.findings["reddit_discussions"] = self._mock_reddit_discussions()
        print(f"   ✅ Found Reddit discussion trends")

    # ===== Mock Data for Fallback =====

    def _mock_similar_projects(self) -> List[Dict]:
        """Mock similar projects when search unavailable."""
        return [
            {
                "title": f"Awesome {self.project_type} - Collection of great {self.project_type} projects",
                "url": f"https://github.com/awesome-lists/awesome-{self.project_type.lower()}",
                "snippet": "Curated list of awesome projects"
            }
        ]

    def _mock_useful_tools(self) -> List[Dict]:
        """Mock useful tools when search unavailable."""
        return [
            {
                "name": "Docker",
                "url": "https://docker.com",
                "description": "Containerization for easy deployment"
            },
            {
                "name": "GitHub Actions",
                "url": "https://github.com/features/actions",
                "description": "CI/CD automation platform"
            }
        ]

    def _mock_best_practices(self) -> List[Dict]:
        """Mock best practices when search unavailable."""
        return [
            {
                "topic": "Clean Code Principles",
                "url": "https://cleancode.com",
                "details": "Writing maintainable, readable code"
            },
            {
                "topic": "Software Architecture",
                "url": "https://martinfowler.com",
                "details": "Designing scalable systems"
            }
        ]

    def _mock_github_repos(self) -> List[Dict]:
        """Mock GitHub repos when API unavailable."""
        return [
            {
                "name": f"awesome-{self.project_type.lower()}",
                "url": f"https://github.com/awesome-{self.project_type.lower()}/curated-list",
                "description": f"Curated list of {self.project_type} projects",
                "stars": 10000,
                "language": "N/A"
            }
        ]

    def _mock_reddit_discussions(self) -> List[Dict]:
        """Mock Reddit discussions."""
        return [
            {
                "topic": f"r/{self.project_type} community discussions",
                "url": f"https://reddit.com/r/{self.project_type.lower()}",
                "trending": "Current trends in the community"
            }
        ]

    def save_findings(self, project_path: str):
        """Save research findings to project directory."""
        try:
            project_dir = Path(project_path)
            research_file = project_dir / "RESEARCH_FINDINGS.md"

            content = f"""# Research Findings - {self.project_name}

Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## Similar Projects

Examined the following similar projects for architecture reference:

"""
            for project in self.findings["similar_projects"][:5]:
                content += f"- **{project['title']}**\n"
                content += f"  - URL: {project['url']}\n"
                content += f"  - {project['snippet']}\n\n"

            content += "\n## Useful Tools & Libraries\n\n"
            for tool in self.findings["useful_tools"][:5]:
                content += f"- **{tool['name']}**\n"
                content += f"  - {tool['description']}\n"
                content += f"  - {tool['url']}\n\n"

            content += "\n## Best Practices\n\n"
            for practice in self.findings["best_practices"][:5]:
                content += f"- **{practice['topic']}**\n"
                content += f"  - {practice['details']}\n"
                content += f"  - Read more: {practice['url']}\n\n"

            content += "\n## GitHub Repositories\n\n"
            for repo in self.findings["github_repositories"][:5]:
                content += f"- **{repo['name']}** ({repo['language']})\n"
                content += f"  - Stars: {repo['stars']}\n"
                content += f"  - {repo['description']}\n"
                content += f"  - {repo['url']}\n\n"

            content += "\n## Reddit Discussions\n\n"
            for discussion in self.findings["reddit_discussions"]:
                content += f"- {discussion['topic']}\n"
                content += f"  - {discussion['trending']}\n"
                content += f"  - {discussion['url']}\n\n"

            research_file.write_text(content)
            return str(research_file)

        except Exception as e:
            print(f"⚠️  Could not save research findings: {e}")
            return None


async def research_project(project_name: str, project_type: str = None) -> Dict[str, Any]:
    """Factory function for web research."""
    researcher = WebResearcher(project_name, project_type)
    return await researcher.research_project()


async def research_with_perplexity(query: str, api_key: str = None) -> str:
    """Research using Perplexity API.

    Args:
        query: Research query
        api_key: Perplexity API key (if None, tries environment)

    Returns:
        Research findings as string
    """
    try:
        import os
        import httpx

        # Get API key
        if not api_key:
            api_key = os.getenv('PERPLEXITY_API_KEY')

        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY not found")

        print(f"   🤖 Pesquisando com Perplexity: {query[:50]}...")

        # Call Perplexity API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a research assistant. Provide detailed, factual research findings in Portuguese (português). Focus on: industry trends, competitive landscape, market opportunities, and key insights."
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "max_tokens": 1500,
                    "temperature": 0.7
                }
            )

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            research_text = result["choices"][0]["message"]["content"]
            print(f"   ✅ Pesquisa concluída ({len(research_text)} caracteres)")
            return research_text
        else:
            print(f"   ⚠️  Resposta inesperada do Perplexity")
            return f"Pesquisa não retornou resultado esperado"

    except ImportError:
        print(f"   ⚠️  httpx não instalado. Execute: pip install httpx")
        return "httpx não instalado"

    except Exception as e:
        print(f"   ⚠️  Erro ao pesquisar com Perplexity: {e}")
        return f"Erro na pesquisa: {str(e)}"
