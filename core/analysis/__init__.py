"""
Business Analysis Module
Comprehensive business analysis for projects:
- Context discovery (project type, objectives)
- Market research (competitors, gaps, opportunities)
- Competitive analysis (advantages, threats, viability)
- Agent discussion (consultants provide perspectives)
"""

from .context_analyzer import ContextAnalyzer, get_context
from .market_research import MarketResearcher, research_market
from .competitive_analyzer import CompetitiveAnalyzer, analyze_competitive_position
from .business_analyzer import BusinessAnalyzer, analyze_business
from .agent_business_discussion import AgentBusinessDiscussion, discuss_business_case

__all__ = [
    "ContextAnalyzer",
    "get_context",
    "MarketResearcher",
    "research_market",
    "CompetitiveAnalyzer",
    "analyze_competitive_position",
    "BusinessAnalyzer",
    "analyze_business",
    "AgentBusinessDiscussion",
    "discuss_business_case",
]
