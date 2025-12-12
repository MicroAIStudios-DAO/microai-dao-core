"""
Enhanced Knowledge Base
=======================
TF-IDF based knowledge retrieval for AI executive personas.

From: execai-platform-api
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class EnhancedKnowledgeBase:
    """
    Knowledge base with semantic search capabilities.

    Supports:
    - Multi-domain knowledge organization
    - TF-IDF based similarity search
    - Strategic insights by topic
    - Actionable next-step suggestions
    """

    DOMAINS = {
        'business': {
            'name': 'Business Strategy',
            'description': 'Business models, go-to-market, operations',
            'capabilities': ['strategic_advice', 'business_modeling', 'market_analysis']
        },
        'finance': {
            'name': 'Financial Intelligence',
            'description': 'Fundraising, unit economics, capital planning',
            'capabilities': ['financial_analysis', 'fundraising', 'valuation']
        },
        'tech': {
            'name': 'Technical Expertise',
            'description': 'Architecture, scalability, code review',
            'capabilities': ['technical_review', 'architecture', 'scalability']
        },
        'legal': {
            'name': 'Legal & Compliance',
            'description': 'Entity formation, contracts, regulatory',
            'capabilities': ['legal_guidance', 'compliance', 'contracts']
        },
        'ethics': {
            'name': 'Ethics & Governance',
            'description': 'AI ethics, stakeholder alignment, sustainability',
            'capabilities': ['ethical_assessment', 'governance', 'sustainability']
        }
    }

    def __init__(self):
        """Initialize knowledge base with domains and corpus."""
        self.domains = self.DOMAINS
        self.corpus = self._load_knowledge_corpus()
        self.vectorizer = None
        self.vectors = None

        if SKLEARN_AVAILABLE:
            self._initialize_vectorizer()

    def _load_knowledge_corpus(self) -> List[Dict[str, Any]]:
        """Load knowledge items with metadata."""
        return [
            # Business Strategy
            {
                'id': 'biz_001',
                'domain': 'business',
                'content': 'A strong go-to-market strategy starts with identifying your ideal customer profile (ICP) and understanding their pain points deeply.',
                'capabilities': ['strategic_advice', 'market_analysis'],
                'keywords': ['go-to-market', 'GTM', 'customer', 'ICP', 'strategy']
            },
            {
                'id': 'biz_002',
                'domain': 'business',
                'content': 'Business model validation requires testing core assumptions through customer discovery before building full products.',
                'capabilities': ['business_modeling', 'strategic_advice'],
                'keywords': ['business model', 'validation', 'customer discovery', 'MVP']
            },
            {
                'id': 'biz_003',
                'domain': 'business',
                'content': 'Pricing strategy should balance value capture with market penetration. Consider value-based pricing for differentiated offerings.',
                'capabilities': ['strategic_advice', 'business_modeling'],
                'keywords': ['pricing', 'value', 'strategy', 'revenue']
            },
            # Finance
            {
                'id': 'fin_001',
                'domain': 'finance',
                'content': 'Unit economics (CAC, LTV, payback period) are crucial metrics for demonstrating business viability to investors.',
                'capabilities': ['financial_analysis', 'fundraising'],
                'keywords': ['unit economics', 'CAC', 'LTV', 'metrics', 'investors']
            },
            {
                'id': 'fin_002',
                'domain': 'finance',
                'content': 'Fundraising stages (pre-seed, seed, Series A) each have different expectations for traction, team, and market size.',
                'capabilities': ['fundraising', 'financial_analysis'],
                'keywords': ['fundraising', 'seed', 'series A', 'investors', 'traction']
            },
            {
                'id': 'fin_003',
                'domain': 'finance',
                'content': 'Consider alternative funding: SBA loans, grants, revenue-based financing, and DAO treasuries for non-dilutive capital.',
                'capabilities': ['fundraising', 'financial_analysis'],
                'keywords': ['SBA', 'grants', 'DAO', 'non-dilutive', 'alternative funding']
            },
            # Technical
            {
                'id': 'tech_001',
                'domain': 'tech',
                'content': 'Scalable architecture patterns include microservices, event-driven design, and horizontal scaling strategies.',
                'capabilities': ['architecture', 'scalability'],
                'keywords': ['architecture', 'microservices', 'scaling', 'design patterns']
            },
            {
                'id': 'tech_002',
                'domain': 'tech',
                'content': 'Smart contract security requires thorough auditing, formal verification, and following established patterns like OpenZeppelin.',
                'capabilities': ['technical_review', 'architecture'],
                'keywords': ['smart contract', 'security', 'audit', 'Solana', 'Ethereum']
            },
            # Legal
            {
                'id': 'legal_001',
                'domain': 'legal',
                'content': 'Wyoming DAO LLC provides legal recognition for DAOs with liability protection and smart contract governance capabilities.',
                'capabilities': ['legal_guidance', 'compliance'],
                'keywords': ['Wyoming', 'DAO', 'LLC', 'legal', 'governance']
            },
            {
                'id': 'legal_002',
                'domain': 'legal',
                'content': 'AI as a shareholder or stakeholder requires careful legal structuring to ensure voting rights and fiduciary responsibilities.',
                'capabilities': ['legal_guidance', 'governance'],
                'keywords': ['AI', 'shareholder', 'voting', 'fiduciary', 'EXECAI']
            },
            # Ethics
            {
                'id': 'ethics_001',
                'domain': 'ethics',
                'content': 'The Ethical Profitability Index (EPI) uses harmonic mean to ensure neither ethics nor profit can be sacrificed for the other.',
                'capabilities': ['ethical_assessment', 'governance'],
                'keywords': ['EPI', 'ethics', 'profitability', 'harmonic mean', 'balance']
            },
            {
                'id': 'ethics_002',
                'domain': 'ethics',
                'content': 'Stakeholder capitalism considers impact on shareholders, employees, customers, community, environment, and future generations.',
                'capabilities': ['ethical_assessment', 'sustainability'],
                'keywords': ['stakeholder', 'ESG', 'sustainability', 'impact']
            }
        ]

    def _initialize_vectorizer(self) -> None:
        """Initialize TF-IDF vectorizer and compute vectors."""
        if not SKLEARN_AVAILABLE:
            return

        texts = [item['content'] for item in self.corpus]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.vectors = self.vectorizer.fit_transform(texts)

    def query(
        self,
        query: str,
        domains: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        limit: int = 5,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Query the knowledge base.

        Args:
            query: Search query
            domains: Filter by domains (optional)
            capabilities: Filter by capabilities (optional)
            limit: Maximum results to return
            threshold: Minimum similarity threshold

        Returns:
            Dict with matched items and metadata
        """
        # Filter corpus by domains and capabilities
        filtered_corpus = self.corpus
        if domains:
            filtered_corpus = [
                item for item in filtered_corpus
                if item['domain'] in domains
            ]
        if capabilities:
            filtered_corpus = [
                item for item in filtered_corpus
                if any(cap in item['capabilities'] for cap in capabilities)
            ]

        # If sklearn available, use TF-IDF similarity
        if SKLEARN_AVAILABLE and self.vectorizer is not None:
            query_vector = self.vectorizer.transform([query])
            filtered_indices = [
                self.corpus.index(item) for item in filtered_corpus
            ]
            filtered_vectors = self.vectors[filtered_indices]

            similarities = cosine_similarity(query_vector, filtered_vectors).flatten()

            # Get top results above threshold
            results = []
            for idx, sim in enumerate(similarities):
                if sim >= threshold:
                    item = filtered_corpus[idx].copy()
                    item['similarity'] = float(sim)
                    results.append(item)

            results.sort(key=lambda x: x['similarity'], reverse=True)
            results = results[:limit]
        else:
            # Fallback: keyword matching
            results = []
            query_lower = query.lower()
            for item in filtered_corpus:
                score = sum(1 for kw in item.get('keywords', []) if kw in query_lower)
                if score > 0:
                    item_copy = item.copy()
                    item_copy['similarity'] = score / 10
                    results.append(item_copy)

            results.sort(key=lambda x: x['similarity'], reverse=True)
            results = results[:limit]

        return {
            'items': results,
            'query': query,
            'domains_searched': domains or list(self.domains.keys()),
            'total_matches': len(results),
            'timestamp': datetime.now().isoformat()
        }

    def get_domains(self) -> Dict[str, Any]:
        """Get available knowledge domains."""
        return {
            'domains': self.domains,
            'count': len(self.domains)
        }

    def get_strategic_insights(self, query: str) -> List[str]:
        """Get strategic insights based on query topic."""
        insights = self._get_insights_by_topic(query)
        return insights

    def _get_insights_by_topic(self, query: str) -> List[str]:
        """Map query to relevant strategic insights."""
        query_lower = query.lower()

        insights_map = {
            'fundraising': [
                "Focus on demonstrating product-market fit before approaching investors.",
                "Build relationships with investors 6-12 months before you need funding.",
                "Consider your runway and raise enough to hit clear milestones."
            ],
            'pricing': [
                "Value-based pricing captures more value than cost-plus approaches.",
                "Test price sensitivity early with real customers.",
                "Consider tiered pricing to capture different market segments."
            ],
            'scaling': [
                "Scale what's working, not what you hope will work.",
                "Hiring is your biggest lever and biggest risk when scaling.",
                "Culture becomes harder to maintain as you grow - be intentional."
            ],
            'ethics': [
                "Ethical decisions compound - small compromises lead to larger ones.",
                "Transparency with stakeholders builds long-term trust.",
                "The EPI framework helps quantify ethical-profit tradeoffs."
            ],
            'dao': [
                "DAOs work best for decisions that benefit from decentralization.",
                "Wyoming DAO LLC provides legal wrapper for on-chain governance.",
                "AI stakeholders require careful legal structuring for voting rights."
            ]
        }

        for topic, topic_insights in insights_map.items():
            if topic in query_lower:
                return topic_insights

        # Default insights
        return [
            "Start with the problem, not the solution.",
            "Validate assumptions before building.",
            "Focus on one thing at a time."
        ]

    def get_next_step_suggestions(self, query: str) -> List[str]:
        """Get actionable next steps based on query."""
        return self._get_suggestions_by_topic(query)

    def _get_suggestions_by_topic(self, query: str) -> List[str]:
        """Map query to relevant next steps."""
        query_lower = query.lower()

        suggestions_map = {
            'fundraising': [
                "Create a pitch deck that tells a compelling story.",
                "Build a target list of investors aligned with your stage and sector.",
                "Practice your pitch with advisors before investor meetings."
            ],
            'launch': [
                "Define clear success metrics for your launch.",
                "Build a waitlist to gauge demand before launch.",
                "Plan your launch marketing 4-6 weeks in advance."
            ],
            'legal': [
                "Consult with a startup-experienced attorney.",
                "Document all founder agreements in writing.",
                "Ensure proper IP assignment from all contributors."
            ],
            'team': [
                "Define roles and responsibilities clearly.",
                "Set up regular 1:1s and team syncs.",
                "Document your culture and values early."
            ]
        }

        for topic, topic_suggestions in suggestions_map.items():
            if topic in query_lower:
                return topic_suggestions

        return [
            "Break down your goal into specific, measurable actions.",
            "Identify the one thing that would make everything else easier.",
            "Set a deadline and accountability partner for your next step."
        ]
