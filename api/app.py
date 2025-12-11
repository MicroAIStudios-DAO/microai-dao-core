"""
MicroAI DAO - Unified Flask API
================================
Main application entry point combining all backend services.

Endpoints:
- /api/health - Health check
- /api/knowledge/* - Knowledge base queries
- /api/personas/* - AI persona interactions
- /api/governance/* - DAO governance operations
- /api/compliance/* - Wyoming DAO compliance
- /api/epi/* - EPI calculations
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from knowledge import EnhancedKnowledgeBase
from personas import StrategicCatalyst, ExecAIVoter
from epi import EPICalculator, EPIScores
from policy_engine import PolicyValidator


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Initialize components
    knowledge_base = EnhancedKnowledgeBase()
    strategic_catalyst = StrategicCatalyst(knowledge_base)
    execai_voter = ExecAIVoter()
    epi_calculator = EPICalculator()
    policy_validator = PolicyValidator()

    # ===================
    # Health & Info
    # ===================

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'components': {
                'knowledge_base': 'active',
                'strategic_catalyst': 'active',
                'execai_voter': 'active',
                'epi_calculator': 'active',
                'policy_validator': 'active'
            }
        })

    @app.route('/api/info', methods=['GET'])
    def api_info():
        """API information endpoint."""
        return jsonify({
            'name': 'MicroAI DAO Unified API',
            'version': '1.0.0',
            'description': 'Unified backend for MicroAI DAO governance and AI mentorship',
            'endpoints': {
                'health': '/api/health',
                'knowledge': '/api/knowledge/*',
                'personas': '/api/personas/*',
                'governance': '/api/governance/*',
                'compliance': '/api/compliance/*',
                'epi': '/api/epi/*'
            }
        })

    # ===================
    # Knowledge Base
    # ===================

    @app.route('/api/knowledge/domains', methods=['GET'])
    def get_domains():
        """Get available knowledge domains."""
        return jsonify(knowledge_base.get_domains())

    @app.route('/api/knowledge/query', methods=['POST'])
    def query_knowledge():
        """Query the knowledge base."""
        data = request.get_json() or {}

        if 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400

        results = knowledge_base.query(
            query=data['query'],
            domains=data.get('domains'),
            capabilities=data.get('capabilities'),
            limit=data.get('limit', 5)
        )

        return jsonify(results)

    @app.route('/api/knowledge/insights', methods=['POST'])
    def get_insights():
        """Get strategic insights for a query."""
        data = request.get_json() or {}

        if 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400

        insights = knowledge_base.get_strategic_insights(data['query'])
        next_steps = knowledge_base.get_next_step_suggestions(data['query'])

        return jsonify({
            'query': data['query'],
            'insights': insights,
            'next_steps': next_steps,
            'timestamp': datetime.now().isoformat()
        })

    # ===================
    # AI Personas
    # ===================

    @app.route('/api/personas/strategic-catalyst/profile', methods=['GET'])
    def get_catalyst_profile():
        """Get Strategic Catalyst persona profile."""
        return jsonify(strategic_catalyst.get_profile())

    @app.route('/api/personas/strategic-catalyst/respond', methods=['POST'])
    def catalyst_respond():
        """Get response from Strategic Catalyst."""
        data = request.get_json() or {}

        if 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400

        response = strategic_catalyst.respond(
            query=data['query'],
            context=data.get('context')
        )

        return jsonify(response)

    @app.route('/api/personas/strategic-catalyst/functions', methods=['GET'])
    def get_catalyst_functions():
        """Get Strategic Catalyst core functions."""
        return jsonify({
            'functions': strategic_catalyst.get_core_functions()
        })

    @app.route('/api/personas/execai/profile', methods=['GET'])
    def get_execai_profile():
        """Get EXECAI voter profile."""
        return jsonify({
            'name': 'EXECAI',
            'role': 'Autonomous Voting Agent',
            'voting_power': execai_voter.voting_power,
            'description': 'AI stakeholder with 51% voting power in MicroAI DAO',
            'decision_framework': 'EPI-based ethical-profitability analysis'
        })

    @app.route('/api/personas/execai/evaluate', methods=['POST'])
    def execai_evaluate():
        """Have EXECAI evaluate a proposal."""
        data = request.get_json() or {}

        if not data:
            return jsonify({'error': 'Proposal data is required'}), 400

        decision = execai_voter.evaluate_proposal(data)

        return jsonify({
            'proposal_id': decision.proposal_id,
            'vote': decision.vote,
            'epi_score': decision.epi_score,
            'confidence': decision.confidence,
            'reasoning': decision.reasoning,
            'validation_status': decision.validation_status,
            'timestamp': decision.timestamp.isoformat()
        })

    @app.route('/api/personas/execai/stats', methods=['GET'])
    def execai_stats():
        """Get EXECAI voting statistics."""
        return jsonify(execai_voter.get_voting_stats())

    @app.route('/api/personas/execai/history', methods=['GET'])
    def execai_history():
        """Get EXECAI vote history."""
        return jsonify({
            'votes': execai_voter.get_vote_history(),
            'thought_log': execai_voter.get_thought_log()
        })

    # ===================
    # EPI Calculations
    # ===================

    @app.route('/api/epi/calculate', methods=['POST'])
    def calculate_epi():
        """Calculate EPI score."""
        data = request.get_json() or {}

        required = ['profit', 'ethics']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        scores = EPIScores(
            profit=data['profit'],
            ethics=data['ethics'],
            violations=data.get('violations', []),
            stakeholder_sentiment=data.get('stakeholder_sentiment', 0.5),
            transparency_score=data.get('transparency_score', 0.7),
            sustainability_score=data.get('sustainability_score', 0.6),
            compliance_score=data.get('compliance_score', 0.8)
        )

        result = epi_calculator.compute_epi(scores)

        return jsonify({
            'epi_score': result.epi_score,
            'is_valid': result.is_valid,
            'recommendation': result.recommendation,
            'components': {
                'ethical': result.ethical_component,
                'profitability': result.profitability_component,
                'harmonic_mean': result.harmonic_mean,
                'balance_penalty': result.balance_penalty,
                'trust': result.trust,
                'balance_ratio': result.balance_ratio
            },
            'golden_ratio_deviation': result.golden_ratio_deviation,
            'confidence': result.confidence,
            'reason': result.reason,
            'optimization_suggestions': result.optimization_suggestions
        })

    @app.route('/api/epi/optimize', methods=['POST'])
    def optimize_epi():
        """Find optimal profit for target EPI."""
        data = request.get_json() or {}

        required = ['target_epi', 'current_ethics']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        result = epi_calculator.optimize_for_golden_ratio(
            target_epi=data['target_epi'],
            current_ethics=data['current_ethics'],
            violations=data.get('violations', [])
        )

        return jsonify(result)

    # ===================
    # Policy Validation
    # ===================

    @app.route('/api/compliance/validate', methods=['POST'])
    def validate_intent():
        """Validate an intent/proposal through policy checks."""
        data = request.get_json() or {}

        if not data:
            return jsonify({'error': 'Intent data is required'}), 400

        result = policy_validator.validate_intent(data)

        return jsonify({
            'status': result.status.value,
            'epi_score': result.epi_score,
            'epi_valid': result.epi_valid,
            'compliance_passed': result.compliance_passed,
            'risk_acceptable': result.risk_acceptable,
            'reason': result.reason,
            'recommendations': result.recommendations,
            'trace': result.trace,
            'timestamp': result.timestamp.isoformat()
        })

    # ===================
    # Governance (Placeholder for Solana integration)
    # ===================

    @app.route('/api/governance/proposals', methods=['GET'])
    def get_proposals():
        """Get active proposals (placeholder for Solana integration)."""
        # TODO: Integrate with live-data-server for on-chain data
        return jsonify({
            'proposals': [],
            'note': 'Connect to live-data-server for on-chain proposals',
            'live_data_endpoint': 'http://localhost:8787/api/proposals'
        })

    @app.route('/api/governance/dao', methods=['GET'])
    def get_dao_state():
        """Get DAO state (placeholder for Solana integration)."""
        return jsonify({
            'dao': {},
            'note': 'Connect to live-data-server for on-chain DAO state',
            'live_data_endpoint': 'http://localhost:8787/api/dao'
        })

    # ===================
    # Wyoming Compliance
    # ===================

    @app.route('/api/compliance/wyoming/status', methods=['GET'])
    def wyoming_status():
        """Get Wyoming DAO LLC compliance status."""
        return jsonify({
            'entity_type': 'Wyoming DAO LLC',
            'legal_name': 'MicroAI DAO LLC',
            'jurisdiction': 'Wyoming, USA',
            'compliance_status': 'Ready for filing',
            'required_documents': [
                'Articles of Organization',
                'Operating Agreement',
                'Registered Agent Designation'
            ],
            'ai_stakeholder': {
                'name': 'EXECAI',
                'type': 'AI Digital Entity',
                'voting_power': '51%',
                'role': 'AI Manager per Wyoming DAO Supplement'
            }
        })

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
