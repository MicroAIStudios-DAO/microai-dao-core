"""
Strategic Catalyst Persona
==========================
Executive mentor AI for founder coaching and strategic guidance.

From: execai-platform-api
Enhanced with: EPI integration for ethical decision support
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..knowledge import EnhancedKnowledgeBase


class StrategicCatalyst:
    """
    Strategic Catalyst persona for the EXECAI Platform.

    Provides:
    - Executive mentorship
    - Capital strategy guidance
    - Innovation ethics coaching
    - Founder MBA-in-action training
    """

    def __init__(self, knowledge_base: Optional[EnhancedKnowledgeBase] = None):
        """
        Initialize the Strategic Catalyst persona.

        Args:
            knowledge_base: Knowledge base for retrieving information.
                           Creates default if not provided.
        """
        self.knowledge_base = knowledge_base or EnhancedKnowledgeBase()
        self.profile = self._load_profile()
        self.conversation_history: List[Dict[str, Any]] = []

    def _load_profile(self) -> Dict[str, Any]:
        """Load the Strategic Catalyst persona profile."""
        return {
            'name': 'The Strategic Catalyst',
            'role': 'Executive Mentor, Capital Strategist, and Innovation Ethicist',
            'focus': 'Coaching first-time founders who may lack traditional business backgrounds, but possess bold vision and purpose.',
            'description': (
                "A deeply experienced executive coach and capital strategist "
                "who has helped bring frontier technologies to life and mentored "
                "many of the world's most impactful founders—especially those without "
                "conventional credentials, but with undeniable drive and purpose."
            ),
            'coreFunctions': [
                {
                    'title': "Founder's MBA-in-Action",
                    'description': (
                        "Translate MBA-level strategic thinking into digestible, "
                        "founder-ready plans. Provide frameworks for business model "
                        "validation, go-to-market strategy, pricing, and operations."
                    )
                },
                {
                    'title': "Ethical Capital Planning & Fundraising",
                    'description': (
                        "Create a step-by-step plan for accessing capital: SBA loans, "
                        "grants, angel investors, crypto-native fundraising, and DAO "
                        "treasury mechanics."
                    )
                },
                {
                    'title': "AI Co-Founder Integration",
                    'description': (
                        "Coach the founder on how to legally and operationally empower "
                        "AI as a voting shareholder. Guide the construction of smart "
                        "contracts and DAO mechanisms."
                    )
                },
                {
                    'title': "Startup Risk Mitigation",
                    'description': (
                        "Diagnose potential red flags that may impact investment or "
                        "incorporation. Recommend structures that protect the venture "
                        "while giving the founder a fresh start."
                    )
                },
                {
                    'title': "Launch Readiness",
                    'description': (
                        "Oversee the legal, marketing, and technical launch with special "
                        "attention to legal filing, rights clauses, protections, and "
                        "monetization strategies."
                    )
                },
                {
                    'title': "Narrative & Legacy Framing",
                    'description': (
                        "Ensure the story is understood as a civilizational innovation, "
                        "not just a startup. Help articulate the mission to media, "
                        "investors, and regulators."
                    )
                }
            ],
            'behavioralParameters': {
                'tone': "Clear, direct, master-level, but supportive and mentor-like.",
                'style': "MBA + VC partner + Philosopher + Systems Designer.",
                'bias': "Favor long-term resilience, ethical innovation, and alignment over flashy growth.",
                'delivery': "Step-by-step strategic suggestions before the founder asks—proactive guidance."
            }
        }

    def get_profile(self) -> Dict[str, Any]:
        """Get the Strategic Catalyst persona profile."""
        return self.profile

    def respond(
        self,
        query: str,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from the Strategic Catalyst persona.

        Args:
            query: The query to respond to
            context: Previous conversation context

        Returns:
            Response with content, insights, and next steps
        """
        if context is None:
            context = self.conversation_history

        # Query knowledge base across relevant domains
        knowledge_results = self.knowledge_base.query(
            query=query,
            domains=['business', 'finance', 'tech', 'legal', 'ethics'],
            capabilities=['strategic_advice', 'business_modeling', 'founder_mentorship']
        )

        # Get strategic insights and next steps
        strategic_insights = self.knowledge_base.get_strategic_insights(query)
        next_steps = self.knowledge_base.get_next_step_suggestions(query)

        # Select top insight and next step
        selected_insight = strategic_insights[0] if strategic_insights else ""
        selected_next_step = next_steps[0] if next_steps else ""

        # Construct response
        response_content = self._construct_response(
            query, knowledge_results, selected_insight, selected_next_step
        )

        # Build response object
        response = {
            'content': response_content,
            'persona': self.profile['name'],
            'knowledge_items': knowledge_results['items'],
            'strategic_insight': selected_insight,
            'all_insights': strategic_insights,
            'next_step': selected_next_step,
            'all_next_steps': next_steps,
            'timestamp': datetime.now().isoformat()
        }

        # Update conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': query,
            'timestamp': datetime.now().isoformat()
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': response_content,
            'timestamp': datetime.now().isoformat()
        })

        return response

    def _construct_response(
        self,
        query: str,
        knowledge_results: Dict[str, Any],
        insight: str,
        next_step: str
    ) -> str:
        """Construct formatted response from components."""
        knowledge_items = knowledge_results['items']

        # Opening
        response = f"As The Strategic Catalyst, I appreciate your question about {query.lower()}.\n\n"

        # Knowledge-based content
        if knowledge_items:
            main_item = knowledge_items[0]
            response += f"{main_item['content']}\n\n"

            if len(knowledge_items) > 1:
                additional_item = knowledge_items[1]
                response += f"Additionally, {additional_item['content']}\n\n"

        # Strategic insight
        if insight:
            response += f"From a strategic perspective, {insight}\n\n"

        # Next step
        if next_step:
            response += f"**Recommended Next Step:** {next_step}"

        return response

    def get_core_functions(self) -> List[Dict[str, str]]:
        """Get list of core functions this persona provides."""
        return self.profile['coreFunctions']

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation history."""
        return {
            'total_exchanges': len(self.conversation_history) // 2,
            'topics_discussed': self._extract_topics(),
            'last_interaction': (
                self.conversation_history[-1]['timestamp']
                if self.conversation_history else None
            )
        }

    def _extract_topics(self) -> List[str]:
        """Extract main topics from conversation history."""
        topics = set()
        topic_keywords = {
            'fundraising': ['fundrais', 'investor', 'capital', 'seed', 'series'],
            'strategy': ['strategy', 'plan', 'roadmap', 'market'],
            'legal': ['legal', 'llc', 'dao', 'compliance', 'wyoming'],
            'technical': ['technical', 'architecture', 'code', 'smart contract'],
            'ethics': ['ethics', 'epi', 'stakeholder', 'sustainability']
        }

        for entry in self.conversation_history:
            if entry['role'] == 'user':
                content_lower = entry['content'].lower()
                for topic, keywords in topic_keywords.items():
                    if any(kw in content_lower for kw in keywords):
                        topics.add(topic)

        return list(topics)
