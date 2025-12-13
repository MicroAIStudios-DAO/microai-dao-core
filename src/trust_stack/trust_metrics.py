"""
Trust Metrics Calculator
========================

Quantitative and qualitative trust indicators for synthetic trust assessment.
Implements the metrics defined in synthetic_trust.md.

References:
- synthetic_trust.md: Trust metrics specification
- Trust Stack: Event logging and verification
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics


class CertificationLevel(Enum):
    """Certification levels for synthetic trust."""
    NONE = 0
    LEVEL_1_MATHEMATICAL = 1
    LEVEL_2_SMART_CONTRACT = 2
    LEVEL_3_AI_AGENT = 3
    LEVEL_4_OPERATIONAL = 4
    LEVEL_5_REGULATORY = 5


@dataclass
class TrustMetrics:
    """Quantitative trust indicators."""
    epi_compliance_rate: float  # % of decisions meeting threshold
    thought_log_completeness: float  # % of decisions with full logs
    guardian_veto_rate: float  # % of proposals vetoed
    incident_response_time: float  # Hours to resolve anomalies
    stakeholder_satisfaction: float  # Community sentiment score (0-1)
    
    # Additional metrics
    total_decisions: int = 0
    avg_epi_score: float = 0.0
    anomaly_count: int = 0
    uptime_percentage: float = 100.0
    
    def get_overall_score(self) -> float:
        """Calculate overall trust score (0-1)."""
        weights = {
            'epi_compliance': 0.30,
            'thought_log': 0.20,
            'guardian_veto': 0.15,  # Lower is better
            'incident_response': 0.15,  # Lower is better
            'stakeholder_satisfaction': 0.20
        }
        
        # Normalize guardian veto rate (lower is better, target <5%)
        veto_score = max(0, 1 - (self.guardian_veto_rate / 0.05))
        
        # Normalize incident response time (lower is better, target <24h)
        response_score = max(0, 1 - (self.incident_response_time / 24))
        
        score = (
            weights['epi_compliance'] * self.epi_compliance_rate +
            weights['thought_log'] * self.thought_log_completeness +
            weights['guardian_veto'] * veto_score +
            weights['incident_response'] * response_score +
            weights['stakeholder_satisfaction'] * self.stakeholder_satisfaction
        )
        
        return score


@dataclass
class QualitativeTrustIndicators:
    """Qualitative trust assessment."""
    transparency: float  # Are decisions understandable? (0-1)
    predictability: float  # Does AI behave consistently? (0-1)
    accountability: float  # Can decisions be traced? (0-1)
    fairness: float  # Are stakeholders treated equitably? (0-1)
    resilience: float  # Does system recover from failures? (0-1)
    
    def get_average(self) -> float:
        """Calculate average qualitative score."""
        return statistics.mean([
            self.transparency,
            self.predictability,
            self.accountability,
            self.fairness,
            self.resilience
        ])


class TrustMetricsCalculator:
    """
    Calculate trust metrics from event logs and system data.
    """
    
    def __init__(self, event_logger):
        """
        Initialize trust metrics calculator.
        
        Args:
            event_logger: EventLogger instance for accessing event data
        """
        self.event_logger = event_logger
        self.epi_threshold = 0.7  # Default EPI threshold
    
    def calculate_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> TrustMetrics:
        """
        Calculate trust metrics for a time period.
        
        Args:
            start_date: Start of period (default: 30 days ago)
            end_date: End of period (default: now)
            
        Returns:
            TrustMetrics object with calculated indicators
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Get events in period
        events = self._get_events_in_period(start_date, end_date)
        
        if len(events) == 0:
            return TrustMetrics(
                epi_compliance_rate=0.0,
                thought_log_completeness=0.0,
                guardian_veto_rate=0.0,
                incident_response_time=0.0,
                stakeholder_satisfaction=0.0
            )
        
        # Calculate EPI compliance rate
        epi_compliant = sum(1 for e in events if e.epi_score and e.epi_score >= self.epi_threshold)
        epi_compliance_rate = epi_compliant / len(events)
        
        # Calculate thought log completeness
        complete_logs = sum(1 for e in events if e.input_hash and e.output_hash and e.signature)
        thought_log_completeness = complete_logs / len(events)
        
        # Calculate guardian veto rate (from action_type)
        vetoed = sum(1 for e in events if e.action_type == 'guardian_veto')
        proposals = sum(1 for e in events if e.action_type in ['proposal', 'strategic_proposal'])
        guardian_veto_rate = vetoed / proposals if proposals > 0 else 0.0
        
        # Calculate average EPI score
        epi_scores = [e.epi_score for e in events if e.epi_score is not None]
        avg_epi_score = statistics.mean(epi_scores) if epi_scores else 0.0
        
        # Incident response time (placeholder - would need incident tracking)
        incident_response_time = 12.0  # Default to 12 hours
        
        # Stakeholder satisfaction (placeholder - would need survey data)
        stakeholder_satisfaction = 0.85  # Default to 85%
        
        # Anomaly count (events with very low EPI or unusual patterns)
        anomaly_count = sum(1 for e in events if e.epi_score and e.epi_score < 0.5)
        
        return TrustMetrics(
            epi_compliance_rate=epi_compliance_rate,
            thought_log_completeness=thought_log_completeness,
            guardian_veto_rate=guardian_veto_rate,
            incident_response_time=incident_response_time,
            stakeholder_satisfaction=stakeholder_satisfaction,
            total_decisions=len(events),
            avg_epi_score=avg_epi_score,
            anomaly_count=anomaly_count,
            uptime_percentage=99.5  # Placeholder
        )
    
    def assess_certification_level(self, metrics: TrustMetrics) -> CertificationLevel:
        """
        Assess current certification level based on metrics.
        
        Args:
            metrics: TrustMetrics object
            
        Returns:
            Current certification level
        """
        # Level 1: Mathematical (always true if system is running)
        level = CertificationLevel.LEVEL_1_MATHEMATICAL
        
        # Level 2: Smart Contract (requires audit)
        # This would be set manually after audit completion
        
        # Level 3: AI Agent (requires certification)
        if (metrics.epi_compliance_rate >= 0.95 and
            metrics.thought_log_completeness >= 0.95 and
            metrics.total_decisions >= 100):
            level = CertificationLevel.LEVEL_3_AI_AGENT
        
        # Level 4: Operational (requires sustained performance)
        if (metrics.epi_compliance_rate >= 0.95 and
            metrics.thought_log_completeness == 1.0 and
            metrics.guardian_veto_rate < 0.05 and
            metrics.total_decisions >= 1000):
            level = CertificationLevel.LEVEL_4_OPERATIONAL
        
        # Level 5: Regulatory (requires external compliance)
        # This would be set manually after regulatory approval
        
        return level
    
    def detect_anomalies(
        self,
        events: List,
        lookback_days: int = 7
    ) -> List[Dict]:
        """
        Detect anomalies in AI decision patterns.
        
        Args:
            events: List of events to analyze
            lookback_days: Number of days to analyze
            
        Returns:
            List of detected anomalies with descriptions
        """
        anomalies = []
        
        if len(events) == 0:
            return anomalies
        
        # Get EPI scores
        epi_scores = [e.epi_score for e in events if e.epi_score is not None]
        
        if len(epi_scores) == 0:
            return anomalies
        
        # Calculate statistics
        mean_epi = statistics.mean(epi_scores)
        stdev_epi = statistics.stdev(epi_scores) if len(epi_scores) > 1 else 0
        
        # Anomaly 1: Sudden drop in EPI scores
        recent_scores = epi_scores[-10:] if len(epi_scores) >= 10 else epi_scores
        recent_mean = statistics.mean(recent_scores)
        
        if recent_mean < mean_epi - 2 * stdev_epi:
            anomalies.append({
                'type': 'epi_drop',
                'severity': 'high',
                'description': f'Recent EPI scores ({recent_mean:.3f}) significantly below average ({mean_epi:.3f})',
                'recommendation': 'Review recent decisions and check for data quality issues'
            })
        
        # Anomaly 2: High variance in EPI scores
        if stdev_epi > 0.15:
            anomalies.append({
                'type': 'high_variance',
                'severity': 'medium',
                'description': f'High variance in EPI scores (σ={stdev_epi:.3f})',
                'recommendation': 'AI behavior may be inconsistent, review decision logic'
            })
        
        # Anomaly 3: Frequent low EPI scores
        low_epi_count = sum(1 for score in epi_scores if score < self.epi_threshold)
        low_epi_rate = low_epi_count / len(epi_scores)
        
        if low_epi_rate > 0.10:  # More than 10% below threshold
            anomalies.append({
                'type': 'frequent_low_epi',
                'severity': 'high',
                'description': f'{low_epi_rate:.1%} of decisions below EPI threshold',
                'recommendation': 'AI may be gaming the system or ethical factors are underweighted'
            })
        
        # Anomaly 4: Unusual decision frequency
        time_deltas = []
        for i in range(1, len(events)):
            try:
                t1 = datetime.fromisoformat(events[i-1].timestamp)
                t2 = datetime.fromisoformat(events[i].timestamp)
                time_deltas.append((t2 - t1).total_seconds())
            except:
                continue
        
        if time_deltas:
            avg_delta = statistics.mean(time_deltas)
            recent_delta = statistics.mean(time_deltas[-5:]) if len(time_deltas) >= 5 else avg_delta
            
            if recent_delta < avg_delta * 0.3:  # Sudden spike in activity
                anomalies.append({
                    'type': 'activity_spike',
                    'severity': 'medium',
                    'description': 'Unusual spike in decision frequency',
                    'recommendation': 'Verify AI is not being manipulated or spammed'
                })
        
        return anomalies
    
    def calculate_qualitative_indicators(
        self,
        metrics: TrustMetrics
    ) -> QualitativeTrustIndicators:
        """
        Calculate qualitative trust indicators from quantitative metrics.
        
        Args:
            metrics: TrustMetrics object
            
        Returns:
            QualitativeTrustIndicators object
        """
        # Transparency: Based on thought log completeness
        transparency = metrics.thought_log_completeness
        
        # Predictability: Based on EPI compliance and low anomalies
        predictability = metrics.epi_compliance_rate * (1 - metrics.anomaly_count / max(metrics.total_decisions, 1))
        predictability = max(0, min(1, predictability))
        
        # Accountability: Based on thought log completeness and signature verification
        accountability = metrics.thought_log_completeness
        
        # Fairness: Based on low guardian veto rate (indicates AI is aligned)
        fairness = max(0, 1 - metrics.guardian_veto_rate / 0.05)
        
        # Resilience: Based on uptime and incident response
        resilience = metrics.uptime_percentage / 100 * (1 - metrics.incident_response_time / 48)
        resilience = max(0, min(1, resilience))
        
        return QualitativeTrustIndicators(
            transparency=transparency,
            predictability=predictability,
            accountability=accountability,
            fairness=fairness,
            resilience=resilience
        )
    
    def _get_events_in_period(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List:
        """Get events within a time period."""
        # This would query the database
        # For now, return empty list as placeholder
        try:
            all_events = []
            # Get events by date range
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                daily_events = self.event_logger.get_events_by_date(date_str)
                all_events.extend(daily_events)
                current_date += timedelta(days=1)
            return all_events
        except:
            return []


# Example usage
if __name__ == "__main__":
    from event_logger import EventLogger
    
    logger = EventLogger()
    calculator = TrustMetricsCalculator(logger)
    
    # Calculate metrics for last 30 days
    metrics = calculator.calculate_metrics()
    
    print("Trust Metrics:")
    print(f"  EPI Compliance Rate: {metrics.epi_compliance_rate:.1%}")
    print(f"  Thought Log Completeness: {metrics.thought_log_completeness:.1%}")
    print(f"  Guardian Veto Rate: {metrics.guardian_veto_rate:.1%}")
    print(f"  Incident Response Time: {metrics.incident_response_time:.1f}h")
    print(f"  Stakeholder Satisfaction: {metrics.stakeholder_satisfaction:.1%}")
    print(f"  Overall Trust Score: {metrics.get_overall_score():.3f}")
    print()
    
    # Assess certification level
    level = calculator.assess_certification_level(metrics)
    print(f"Certification Level: {level.name}")
    print()
    
    # Calculate qualitative indicators
    qualitative = calculator.calculate_qualitative_indicators(metrics)
    print("Qualitative Indicators:")
    print(f"  Transparency: {qualitative.transparency:.1%}")
    print(f"  Predictability: {qualitative.predictability:.1%}")
    print(f"  Accountability: {qualitative.accountability:.1%}")
    print(f"  Fairness: {qualitative.fairness:.1%}")
    print(f"  Resilience: {qualitative.resilience:.1%}")
    print(f"  Average: {qualitative.get_average():.1%}")
