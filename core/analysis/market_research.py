"""
Market Research Module
- Uses Perplexity MCP to research market data
- Finds competitors, market size, trends
- Gathers competitive intelligence
"""

import httpx
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

PERPLEXITY_MCP = "http://localhost:3007"


class MarketResearcher:
    """Conducts market research using Perplexity MCP."""

    def __init__(self, project_name: str, project_type: str, objectives: list):
        self.project_name = project_name
        self.project_type = project_type
        self.objectives = objectives
        self.perplexity_available = False

    async def _check_perplexity(self):
        """Check if Perplexity MCP is available."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                await client.get(f"{PERPLEXITY_MCP}/health")
                self.perplexity_available = True
                logger.info("✅ Perplexity MCP available")
        except:
            logger.warning("⚠️  Perplexity MCP not available - market research limited")

    async def research(self) -> Dict[str, Any]:
        """Conduct comprehensive market research."""
        research = {
            "market_overview": {},
            "competitors": [],
            "market_size": None,
            "trends": [],
            "gaps": [],
            "opportunities": []
        }

        # Check Perplexity availability
        await self._check_perplexity()

        if not self.perplexity_available:
            logger.warning("Cannot perform market research without Perplexity MCP")
            return research

        print("🔎 Researching market...")

        # Research 1: Market overview
        print("  📊 Market overview...")
        research["market_overview"] = await self._research_market_overview()

        # Research 2: Competitors
        print("  🏆 Competitors...")
        research["competitors"] = await self._research_competitors()

        # Research 3: Market size
        print("  📈 Market size and trends...")
        research["market_size"] = await self._research_market_size()

        # Research 4: Gaps and opportunities
        print("  ⚡ Gaps and opportunities...")
        research["gaps"], research["opportunities"] = await self._research_gaps()

        return research

    async def _research_market_overview(self) -> Dict[str, Any]:
        """Research market overview."""
        query = f"Market overview for {self.project_name} type {self.project_type}. Who are the main players? What is the market doing?"

        result = await self._search(query)
        return {"summary": result}

    async def _research_competitors(self) -> list:
        """Research direct competitors."""
        query = f"Main competitors in {self.project_name} space. Who are the biggest players? What are they doing?"

        result = await self._search(query)

        # Parse result to extract competitors
        competitors = []
        lines = result.split('\n')
        for line in lines[:10]:  # First 10 lines likely have competitors
            if any(x in line.lower() for x in ['company', 'platform', 'app', 'service', 'competitor']):
                competitors.append(line.strip())

        return competitors[:5]  # Top 5

    async def _research_market_size(self) -> Dict[str, Any]:
        """Research market size and trends."""
        query = f"Market size and growth for {self.project_name}. What is the TAM? What are the trends?"

        result = await self._search(query)
        return {"summary": result}

    async def _research_gaps(self) -> tuple:
        """Research market gaps and opportunities."""
        query = f"Market gaps and opportunities in {self.project_name} space. What is missing? Where can new players succeed?"

        result = await self._search(query)

        gaps = []
        opportunities = []

        lines = result.split('\n')
        for line in lines:
            if any(x in line.lower() for x in ['gap', 'missing', 'lacking', 'need']):
                gaps.append(line.strip())
            elif any(x in line.lower() for x in ['opportunity', 'potential', 'could', 'emerging']):
                opportunities.append(line.strip())

        return gaps[:3], opportunities[:3]

    async def _search(self, query: str) -> str:
        """Execute search via Perplexity MCP."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{PERPLEXITY_MCP}/search",
                    json={
                        "query": query,
                        "format": "summary"
                    }
                )
                result = response.json()
                return result.get("summary", result.get("results", "No results"))
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"Research unavailable: {e}"


async def research_market(project_name: str, project_type: str, objectives: list) -> Dict[str, Any]:
    """Factory function for market research."""
    researcher = MarketResearcher(project_name, project_type, objectives)
    await researcher._check_perplexity()
    return await researcher.research()
