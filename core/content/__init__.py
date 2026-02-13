"""
Content Reader - Extract real insights from projects
"""

from pathlib import Path
from typing import Dict, List, Any
import json
import re


class ContentReader:
    """Read and extract insights from project files."""

    def __init__(self, project_path: str):
        self.path = Path(project_path)
        self.content_cache = {}

    def read_project_content(self) -> Dict[str, Any]:
        """Read all relevant content from project."""
        insights = {
            'title': '',
            'themes': [],
            'key_files': [],
            'data_files': [],
            'raw_content': [],
            'extracted_ideas': [],
        }

        if not self.path.exists():
            return insights

        # Read all markdown files
        for md_file in self.path.glob('**/*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    insights['raw_content'].append({
                        'file': md_file.name,
                        'content': content[:1000]  # First 1000 chars
                    })
                    insights['key_files'].append(md_file.name)
            except Exception as e:
                pass

        # Read JSON files (data)
        for json_file in self.path.glob('**/*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    insights['data_files'].append({
                        'file': json_file.name,
                        'size': len(json.dumps(data)),
                        'data': data if isinstance(data, dict) else {}
                    })
            except Exception as e:
                pass

        # Extract ideas from content
        insights['extracted_ideas'] = self._extract_ideas(insights['raw_content'])

        return insights

    def _extract_ideas(self, content_list: List[Dict]) -> List[str]:
        """Extract key ideas from content."""
        ideas = []

        for item in content_list:
            content = item['content'].lower()

            # Extract sentences that look like insights
            sentences = re.split(r'[.!?]+', content)

            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and len(sentence) < 200:
                    # Look for insight keywords
                    if any(keyword in sentence for keyword in [
                        'important', 'key', 'insight', 'discover', 'find',
                        'conclus', 'result', 'success', 'fail', 'problem',
                        'solution', 'benefit', 'challenge', 'opportunity'
                    ]):
                        ideas.append(sentence.capitalize())

        return list(set(ideas))[:10]  # Return top 10 unique ideas

    def get_summary(self) -> Dict[str, Any]:
        """Get project content summary."""
        content = self.read_project_content()

        return {
            'total_files': len(content['key_files']),
            'markdown_files': len(content['key_files']),
            'data_files': len(content['data_files']),
            'ideas_extracted': len(content['extracted_ideas']),
            'top_ideas': content['extracted_ideas'][:5],
            'key_files': content['key_files'],
        }


class WisdomExtractor:
    """Extract wisdom/insights from Wisdom of Reddit project."""

    def __init__(self, project_path: str):
        self.reader = ContentReader(project_path)
        self.insights = {}

    def extract_wisdom(self) -> Dict[str, Any]:
        """Extract all wisdom from project."""
        content = self.reader.read_project_content()

        wisdom = {
            'total_insights': 0,
            'themes': self._extract_themes(content),
            'actionable_items': self._extract_actions(content),
            'opportunities': self._extract_opportunities(content),
            'key_takeaways': content['extracted_ideas'][:5],
        }

        wisdom['total_insights'] = (
            len(wisdom['themes']) +
            len(wisdom['actionable_items']) +
            len(wisdom['opportunities'])
        )

        return wisdom

    def _extract_themes(self, content: Dict) -> List[str]:
        """Extract main themes."""
        themes = []
        all_content = '\n'.join([item.get('content', '') for item in content['raw_content']])

        theme_keywords = {
            'Produtividade': ['produtiv', 'efficien', 'workflow', 'productivity'],
            'Remote Work': ['remote', 'home', 'teletrabalho', 'wfh'],
            'Saúde': ['saude', 'health', 'mental', 'wellness'],
            'Negócio': ['business', 'startup', 'entrepreneurship', 'negocio'],
            'Tecnologia': ['tech', 'software', 'code', 'development'],
            'Finanças': ['finance', 'money', 'economic', 'financeiro'],
        }

        for theme, keywords in theme_keywords.items():
            if any(kw.lower() in all_content.lower() for kw in keywords):
                themes.append(theme)

        return themes

    def _extract_actions(self, content: Dict) -> List[str]:
        """Extract actionable items."""
        actions = []
        content_text = '\n'.join([item.get('content', '') for item in content['raw_content']])

        # Look for action words
        action_phrases = re.findall(
            r'(do|implement|create|build|develop|start|begin|try|test|use)\s+([a-z\s]+)',
            content_text.lower()
        )

        for _, phrase in action_phrases[:5]:
            actions.append(f"Action: {phrase.strip().capitalize()}")

        return actions

    def _extract_opportunities(self, content: Dict) -> List[str]:
        """Extract business opportunities."""
        opportunities = []

        # Simple heuristic: look for problems that could be opportunities
        for idea in content['extracted_ideas'][:3]:
            opportunities.append(f"Opportunity: Build solution for: {idea[:50]}...")

        return opportunities
