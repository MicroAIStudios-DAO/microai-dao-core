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
from trust_stack import EventLogger, MerkleTree, AttestationGenerator, ProofVerifier, DailyMerkleAnchor


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
    event_logger = EventLogger()
    attestation_gen = AttestationGenerator()
    proof_verifier = ProofVerifier()
    merkle_anchor = DailyMerkleAnchor()

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
                'policy_validator': 'active',
                'trust_stack': 'active'
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
                'epi': '/api/epi/*',
                'trust': '/api/trust/*'
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
            'description': 'AI stakeholder with 33% voting power in MicroAI DAO (balanced: 33% AI, 33% founders, 33% investors)',
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
                'voting_power': '33%',
                'role': 'AI Manager per Wyoming DAO Supplement'
            }
        })

    # ===================
    # Trust Stack
    # ===================

    @app.route('/api/trust/log', methods=['POST'])
    def log_trust_event():
        """Log a trust event with cryptographic signature."""
        data = request.get_json() or {}

        required = ['tenant_id', 'agent_id', 'action_type', 'input_data', 'output_data', 'policy_version']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            event = event_logger.log_event(
                tenant_id=data['tenant_id'],
                agent_id=data['agent_id'],
                action_type=data['action_type'],
                input_data=data['input_data'],
                output_data=data['output_data'],
                policy_version=data['policy_version'],
                epi_score=data.get('epi_score'),
                model=data.get('model'),
                tools_called=data.get('tools_called'),
                redactions=data.get('redactions'),
                evaluations=data.get('evaluations')
            )

            return jsonify({
                'success': True,
                'event': event.to_dict(),
                'message': 'Event logged successfully'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/trust/event/<event_id>', methods=['GET'])
    def get_trust_event(event_id):
        """Retrieve a trust event by ID."""
        event = event_logger.get_event(event_id)

        if event:
            return jsonify({
                'success': True,
                'event': event.to_dict()
            })
        else:
            return jsonify({'error': 'Event not found'}), 404

    @app.route('/api/trust/events/agent/<agent_id>', methods=['GET'])
    def get_agent_events(agent_id):
        """Get recent events for a specific agent."""
        limit = request.args.get('limit', 100, type=int)
        events = event_logger.get_events_by_agent(agent_id, limit=limit)

        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'count': len(events),
            'events': [e.to_dict() for e in events]
        })

    @app.route('/api/trust/events/date/<date>', methods=['GET'])
    def get_events_by_date(date):
        """Get all events for a specific date (YYYY-MM-DD)."""
        events = event_logger.get_events_by_date(date)

        return jsonify({
            'success': True,
            'date': date,
            'count': len(events),
            'events': [e.to_dict() for e in events]
        })

    @app.route('/api/trust/prove/<event_id>', methods=['GET'])
    def prove_event(event_id):
        """Generate Merkle proof for an event."""
        event = event_logger.get_event(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        # Get date from event
        date = event.timestamp[:10]

        # Get all hashes for that day
        event_hashes = event_logger.get_daily_hashes(date)

        if not event_hashes:
            return jsonify({'error': 'No events found for that date'}), 404

        # Build Merkle tree
        tree = MerkleTree(event_hashes)

        # Get event hash
        event_hash = event_logger.hash_data(event.input_hash + event.output_hash)

        # Generate proof
        proof = tree.get_proof(event_hash)

        if proof:
            return jsonify({
                'success': True,
                'event_id': event_id,
                'proof': proof.to_dict(),
                'tree_info': tree.get_tree_info()
            })
        else:
            return jsonify({'error': 'Could not generate proof'}), 500

    @app.route('/api/trust/verify/event', methods=['POST'])
    def verify_event():
        """Verify an event signature."""
        data = request.get_json() or {}

        if 'event' not in data:
            return jsonify({'error': 'Event data is required'}), 400

        try:
            from trust_stack.event_logger import TrustEvent
            event = TrustEvent(**data['event'])
            result = proof_verifier.verify_event_signature(event)

            return jsonify(result.to_dict())

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/trust/verify/proof', methods=['POST'])
    def verify_proof():
        """Verify a Merkle proof."""
        data = request.get_json() or {}

        if 'proof' not in data:
            return jsonify({'error': 'Proof data is required'}), 400

        try:
            from trust_stack.merkle_tree import MerkleProof
            proof = MerkleProof(**data['proof'])
            result = proof_verifier.verify_merkle_proof(proof)

            return jsonify(result.to_dict())

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/trust/anchor/daily/<date>', methods=['POST'])
    def anchor_daily_root(date):
        """Generate and anchor daily Merkle root."""
        event_hashes = event_logger.get_daily_hashes(date)

        if not event_hashes:
            return jsonify({'error': 'No events found for that date'}), 404

        root = merkle_anchor.generate_daily_root(date, event_hashes)
        anchor_tx = merkle_anchor.prepare_anchor_transaction(date, root)

        return jsonify({
            'success': True,
            'date': date,
            'event_count': len(event_hashes),
            'merkle_root': root,
            'anchor_transaction': anchor_tx
        })

    @app.route('/api/trust/attestation/generate', methods=['POST'])
    def generate_attestation():
        """Generate an attestation bundle for a release."""
        data = request.get_json() or {}

        required = ['release_id', 'log_root', 'policy_version']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            # Generate model card
            model_card = attestation_gen.generate_model_card(
                model_name=data.get('model_name', 'MicroAI-DAO'),
                model_version=data['release_id'],
                description=data.get('description', 'AI governance system'),
                intended_use=data.get('intended_use', 'DAO governance and decision-making'),
                limitations=data.get('limitations', 'Requires guardian oversight'),
                training_data=data.get('training_data', 'Business strategy corpus'),
                performance_metrics=data.get('performance_metrics', {})
            )

            # Generate SBOM
            sbom = attestation_gen.generate_sbom(
                components=data.get('components', []),
                format=data.get('sbom_format', 'SPDX')
            )

            # Compile eval summary
            eval_summary = attestation_gen.compile_eval_summary(
                total_requests=data.get('total_requests', 0),
                evaluated_requests=data.get('evaluated_requests', 0),
                passed_requests=data.get('passed_requests', 0),
                category_results=data.get('category_results', {}),
                last_red_team_date=data.get('last_red_team_date', datetime.now().strftime('%Y-%m-%d'))
            )

            # Generate attestation
            attestation = attestation_gen.generate_attestation(
                release_id=data['release_id'],
                model_card=model_card,
                sbom=sbom,
                eval_summary=eval_summary,
                log_root=data['log_root'],
                policy_version=data['policy_version'],
                compliance_frameworks=data.get('compliance_frameworks'),
                metadata=data.get('metadata')
            )

            return jsonify({
                'success': True,
                'attestation': attestation.to_dict(),
                'message': 'Attestation generated successfully'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/trust/status', methods=['GET'])
    def trust_status():
        """Get overall trust system status."""
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        events_today = event_logger.get_events_by_date(today)

        # Calculate stats
        agent_stats = {}
        epi_scores = []

        for event in events_today:
            if event.agent_id not in agent_stats:
                agent_stats[event.agent_id] = {'count': 0, 'actions': []}
            agent_stats[event.agent_id]['count'] += 1
            agent_stats[event.agent_id]['actions'].append(event.action_type)

            if event.epi_score is not None:
                epi_scores.append(event.epi_score)

        avg_epi = sum(epi_scores) / len(epi_scores) if epi_scores else 0

        return jsonify({
            'success': True,
            'status': 'operational',
            'date': today,
            'events_today': len(events_today),
            'agent_activity': agent_stats,
            'average_epi_score': round(avg_epi, 3),
            'trust_badge': 'Bronze' if len(events_today) > 0 else 'None',
            'last_anchor': merkle_anchor.get_root_for_date(today)
        })

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
