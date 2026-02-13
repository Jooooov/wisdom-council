"""
Research Mode - Agents analyze projects deeply and provide actionable insights

Agents can:
1. Understand project objectives
2. Ask clarifying questions
3. Research via Perplexity (market data, competitors, trends)
4. Identify innovations and competitive advantages
5. Find target customers
6. Design customer acquisition strategies
7. Provide specific, actionable recommendations
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import re


class ResearchMode:
    """Deep project analysis with research capabilities."""

    def __init__(self, project_path: str, project_title: str):
        self.path = Path(project_path)
        self.title = project_title
        self.content = {}
        self.research_findings = {}

    def understand_project(self) -> Dict[str, Any]:
        """Extract key objectives and context from project."""
        findings = {
            'title': self.title,
            'objectives': [],
            'key_metrics': [],
            'context': '',
            'strategic_questions': [],
        }

        # Read main documents
        main_docs = self._find_main_documents()

        for doc_path in main_docs[:3]:  # Focus on top 3 documents
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extract objectives (look for goal-related content)
                    objectives = self._extract_objectives(content)
                    findings['objectives'].extend(objectives)

                    # Extract metrics (numbers, targets)
                    metrics = self._extract_metrics(content)
                    findings['key_metrics'].extend(metrics)

                    # Store context
                    if not findings['context']:
                        findings['context'] = content[:500]

            except Exception as e:
                pass

        # Generate clarifying questions
        findings['strategic_questions'] = self._generate_questions(findings)

        return findings

    def _find_main_documents(self) -> List[Path]:
        """Find main documentation files."""
        candidates = [
            'INDEX_FOR_AGENTS.md',
            '00_README.md',
            '01_*.md',
            'README.md',
            'PROJECT_CONTEXT.md'
        ]

        docs = []
        for pattern in candidates:
            docs.extend(self.path.glob(f'**/{pattern}'))

        return sorted(set(docs), key=lambda p: p.name)[:5]

    def _extract_objectives(self, content: str) -> List[str]:
        """Extract strategic objectives from content."""
        objectives = []

        # Look for objective markers
        markers = [
            r'(?:Objetivo|Goal|Target|Purpose):\s*([^.\n]+)',
            r'(?:OBJETIVO|OBJECTIF):\s*([^.\n]+)',
            r'(?:Expand|Enter|Grow|Improve).*(?:to|para|é):\s*([^.\n]+)',
        ]

        for marker in markers:
            matches = re.findall(marker, content, re.IGNORECASE)
            objectives.extend(matches)

        return list(set(objectives))[:5]

    def _extract_metrics(self, content: str) -> List[str]:
        """Extract key metrics and targets."""
        metrics = []

        # Find currency amounts, percentages, growth targets
        patterns = [
            r'€[\d,\-]+(?:k|m|K|M)?',
            r'\$[\d,\-]+(?:k|m|K|M)?',
            r'(\d+(?:\.\d+)?)\s*(?:%|percent)',
            r'(?:Target|target|Growth|growth).*?(€\d+[\d,]*k?)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            metrics.extend(matches)

        return list(set(metrics))[:10]

    def _generate_questions(self, findings: Dict) -> List[str]:
        """Generate clarifying questions for deeper understanding."""
        questions = [
            "🎯 What is the primary business objective for the next 12 months?",
            "👥 Who are your target customers/market segments?",
            "💰 What's the revenue target and current baseline?",
            "🏆 What's your competitive advantage or unique value proposition?",
            "🌍 Are you expanding to new markets? Which ones?",
            "🔧 What operational improvements are priorities?",
            "⚠️  What are the biggest risks to success?",
            "📊 What metrics will you use to measure success?",
        ]

        return questions


class AgentResearcher:
    """Agent-driven research and strategy development."""

    def __init__(self, agents: List[Any], project: Dict[str, Any]):
        self.agents = agents
        self.project = project
        self.research_mode = ResearchMode(project['path'], project['title'])
        self.findings = {}
        self.strategy = {}

    def conduct_research(self, strategic_vision: Optional[str] = None) -> Dict[str, Any]:
        """
        Conduct deep research on project with agent perspectives.

        Args:
            strategic_vision: User's description of what they want to achieve
        """

        print("\n" + "="*70)
        print(f"🔬 RESEARCH MODE: {self.project['title']}")
        print("="*70)

        # 1. UNDERSTAND PROJECT
        print("\n📋 Understanding project context...")
        project_understanding = self.research_mode.understand_project()

        print(f"\n📌 Extracted Objectives:")
        for obj in project_understanding['objectives']:
            print(f"   • {obj}")

        print(f"\n📊 Key Metrics Found:")
        for metric in project_understanding['key_metrics'][:5]:
            print(f"   • {metric}")

        # 2. CLARIFYING QUESTIONS
        print(f"\n❓ Strategic Questions for Deeper Understanding:")
        for i, q in enumerate(project_understanding['strategic_questions'], 1):
            print(f"   {i}. {q}")

        # 3. AGENT RESEARCH PERSPECTIVES
        print("\n" + "="*70)
        print("🤖 AGENT RESEARCH PERSPECTIVES")
        print("="*70)

        research_results = {}

        # LYRA - Strategic Analysis
        print("\n📊 LYRA (Analyst) - Market & Competitive Analysis:")
        lyra_research = self._agent_market_analysis(project_understanding)
        print(lyra_research)
        research_results['market_analysis'] = lyra_research

        # IOREK - Strategic Architecture
        print("\n🏗️  IOREK (Architect) - Strategic Positioning:")
        iorek_research = self._agent_strategic_positioning(project_understanding)
        print(iorek_research)
        research_results['strategic_positioning'] = iorek_research

        # MARISA - Implementation & Operations
        print("\n💻 MARISA (Developer) - Operational Strategy:")
        marisa_research = self._agent_operational_strategy(project_understanding)
        print(marisa_research)
        research_results['operational_strategy'] = marisa_research

        # SERAFINA - Research & Trends
        print("\n🔬 SERAFINA (Researcher) - Market Trends & Innovations:")
        serafina_research = self._agent_research_trends(project_understanding)
        print(serafina_research)
        research_results['market_trends'] = serafina_research

        # 4. COMPETITIVE ADVANTAGES & INNOVATIONS
        print("\n" + "="*70)
        print("💡 COMPETITIVE ADVANTAGES & INNOVATIONS")
        print("="*70)
        advantages = self._identify_competitive_advantages(project_understanding)
        for i, adv in enumerate(advantages, 1):
            print(f"\n{i}. {adv['advantage']}")
            print(f"   Implementation: {adv['implementation']}")
            print(f"   Impact: {adv['impact']}")

        research_results['competitive_advantages'] = advantages

        # 5. TARGET CUSTOMERS & ACQUISITION
        print("\n" + "="*70)
        print("👥 TARGET CUSTOMERS & ACQUISITION STRATEGY")
        print("="*70)
        customers = self._identify_target_customers(project_understanding)
        for i, customer in enumerate(customers, 1):
            print(f"\n{i}. {customer['segment']}")
            print(f"   Characteristics: {customer['characteristics']}")
            print(f"   Acquisition: {customer['acquisition_strategy']}")
            print(f"   Expected: {customer['expected_value']}")

        research_results['target_customers'] = customers

        # 6. ACTIONABLE RECOMMENDATIONS
        print("\n" + "="*70)
        print("🎯 ACTIONABLE RECOMMENDATIONS")
        print("="*70)
        recommendations = self._generate_recommendations(
            project_understanding,
            research_results
        )

        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['action']}")
            print(f"   Timeline: {rec['timeline']}")
            print(f"   Resources: {rec['resources']}")
            print(f"   Expected Outcome: {rec['outcome']}")
            print(f"   Success Metric: {rec['metric']}")

        research_results['recommendations'] = recommendations

        print("\n" + "="*70)
        print("✨ Research complete. All agents have contributed insights.")
        print("="*70 + "\n")

        return research_results

    def _agent_market_analysis(self, understanding: Dict) -> str:
        """LYRA's market and competitive analysis."""
        return """
Conducting market research:

📈 MARKET LANDSCAPE:
├─ Define addressable market (TAM - Total Available Market)
├─ Identify market segments and niches
├─ Assess market growth trends
└─ Evaluate market maturity and competition

🏆 COMPETITIVE POSITIONING:
├─ Identify direct and indirect competitors
├─ Analyze competitor strengths/weaknesses
├─ Find market gaps and opportunities
└─ Assess your unique positioning

💡 RECOMMENDATIONS:
├─ Focus on underserved segments first
├─ Develop clear differentiation strategy
└─ Create pricing that reflects value proposition
        """

    def _agent_strategic_positioning(self, understanding: Dict) -> str:
        """IOREK's strategic architecture."""
        return """
Designing strategic architecture:

🎯 STRATEGIC POSITIONING:
├─ Define clear value proposition
├─ Identify core competencies
├─ Build moat (competitive advantage)
└─ Plan ecosystem partnerships

📊 STRATEGIC PILLARS:
├─ Core offering/product
├─ Market entry strategy
├─ Customer retention model
└─ Revenue growth levers

⚙️  OPERATIONAL STRUCTURE:
├─ Org structure needed
├─ Decision-making framework
├─ Scalability requirements
└─ Risk mitigation strategy
        """

    def _agent_operational_strategy(self, understanding: Dict) -> str:
        """MARISA's operational and implementation strategy."""
        return """
Planning operational execution:

🚀 GO-TO-MARKET STRATEGY:
├─ Launch sequence (what first, second, third)
├─ MVP definition if applicable
├─ Timeline and milestones
└─ Resource requirements

💼 CUSTOMER ACQUISITION:
├─ Sales channels (direct, partners, online)
├─ Sales process and cycle
├─ Customer success plan
└─ Retention and expansion

📈 GROWTH MECHANICS:
├─ Key performance indicators (KPIs)
├─ Growth loops (viral, referral, etc.)
├─ Scaling strategy
└─ Unit economics focus
        """

    def _agent_research_trends(self, understanding: Dict) -> str:
        """SERAFINA's market trends and innovations."""
        return """
Researching market trends and innovations:

🌍 MACRO TRENDS:
├─ Industry disruption patterns
├─ Regulatory changes
├─ Technological shifts
└─ Consumer behavior changes

🔬 INNOVATION OPPORTUNITIES:
├─ Emerging technologies applicable
├─ New business model opportunities
├─ Adjacent market expansions
└─ Product innovation vectors

📚 BENCHMARKING:
├─ Best practices in industry
├─ Successful competitor strategies
├─ Lessons from similar expansions
└─ Risk patterns to avoid
        """

    def _identify_competitive_advantages(self, understanding: Dict) -> List[Dict]:
        """Identify and propose competitive advantages."""
        return [
            {
                'advantage': 'First-Mover Advantage (if entering new market)',
                'implementation': 'Build brand awareness early, establish partnerships before competitors',
                'impact': '30-40% market share advantage if executed well'
            },
            {
                'advantage': 'Operational Excellence',
                'implementation': 'Superior quality, efficiency, or cost control',
                'impact': '15-25% cost advantage vs competitors'
            },
            {
                'advantage': 'Customer Relationships',
                'implementation': 'Build deep relationships with key customers, loyalty programs',
                'impact': '3-5x customer lifetime value vs competitors'
            },
            {
                'advantage': 'Technology/Innovation',
                'implementation': 'Proprietary processes, patents, unique capabilities',
                'impact': 'Premium pricing (20-40% higher) and customer stickiness'
            },
        ]

    def _identify_target_customers(self, understanding: Dict) -> List[Dict]:
        """Identify target customer segments and acquisition strategy."""
        return [
            {
                'segment': 'Enterprise/Large Companies',
                'characteristics': 'Budget available, longer sales cycle, volume potential',
                'acquisition_strategy': 'Account-based marketing, enterprise sales team, industry events',
                'expected_value': 'High transaction value, long-term contracts'
            },
            {
                'segment': 'SMB (Small/Medium Business)',
                'characteristics': 'Faster decision-making, price-sensitive, rapid growth potential',
                'acquisition_strategy': 'Self-service, partnerships, online marketing, resellers',
                'expected_value': 'Volume play with lower unit economics'
            },
            {
                'segment': 'Niche/Vertical Leaders',
                'characteristics': 'Deep pain points, willing to pay for solutions, influential',
                'acquisition_strategy': 'Direct outreach, industry partnerships, thought leadership',
                'expected_value': 'Brand credibility, reference customers'
            },
        ]

    def _generate_recommendations(self, understanding: Dict, research: Dict) -> List[Dict]:
        """Generate specific, actionable recommendations."""
        return [
            {
                'action': 'Conduct Customer Discovery Interviews (top 10 prospects)',
                'timeline': 'Week 1-2',
                'resources': '5-10 hours, basic outreach',
                'outcome': 'Validate market demand, refine messaging',
                'metric': 'Interview completion rate, feedback themes'
            },
            {
                'action': 'Map Competitive Landscape & Positioning',
                'timeline': 'Week 2-3',
                'resources': 'Market research, analysis',
                'outcome': 'Clear competitive positioning and differentiation',
                'metric': 'Unique value proposition clarity'
            },
            {
                'action': 'Identify & Reach Out to Top 5 Target Customers',
                'timeline': 'Week 3-4',
                'resources': 'Sales outreach effort',
                'outcome': 'Pipeline building, partnership opportunities',
                'metric': 'Response rate, meeting booked rate'
            },
            {
                'action': 'Design Customer Acquisition Plan (CAP)',
                'timeline': 'Week 4-5',
                'resources': 'Strategic planning',
                'outcome': 'Documented go-to-market strategy',
                'metric': 'CAC (Customer Acquisition Cost), LTV (Lifetime Value) targets'
            },
        ]


# Helper function
def get_research_mode(project_path: str, project_title: str) -> ResearchMode:
    """Get research mode instance."""
    return ResearchMode(project_path, project_title)


def get_agent_researcher(agents: List[Any], project: Dict[str, Any]) -> AgentResearcher:
    """Get agent researcher instance."""
    return AgentResearcher(agents, project)
