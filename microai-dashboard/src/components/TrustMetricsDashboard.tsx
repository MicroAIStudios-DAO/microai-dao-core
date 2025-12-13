import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Shield, TrendingUp, TrendingDown } from 'lucide-react';

interface TrustMetrics {
  epi_compliance_rate: number;
  thought_log_completeness: number;
  guardian_veto_rate: number;
  incident_response_time: number;
  stakeholder_satisfaction: number;
  total_decisions: number;
  avg_epi_score: number;
  anomaly_count: number;
  uptime_percentage: number;
}

interface QualitativeIndicators {
  transparency: number;
  predictability: number;
  accountability: number;
  fairness: number;
  resilience: number;
}

interface CertificationInfo {
  level: string;
  name: string;
  progress: number;
}

export function TrustMetricsDashboard() {
  const [metrics, setMetrics] = useState<TrustMetrics | null>(null);
  const [qualitative, setQualitative] = useState<QualitativeIndicators | null>(null);
  const [certification, setCertification] = useState<CertificationInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrustMetrics();
    const interval = setInterval(fetchTrustMetrics, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const fetchTrustMetrics = async () => {
    try {
      const response = await fetch('/api/trust/metrics');
      const data = await response.json();
      setMetrics(data.quantitative);
      setQualitative(data.qualitative);
      setCertification(data.certification);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch trust metrics:', error);
      setLoading(false);
    }
  };

  const getScoreColor = (score: number, inverse: boolean = false) => {
    if (inverse) {
      // For metrics where lower is better (like veto rate)
      if (score < 0.05) return 'text-green-600';
      if (score < 0.10) return 'text-yellow-600';
      return 'text-red-600';
    } else {
      // For metrics where higher is better
      if (score >= 0.95) return 'text-green-600';
      if (score >= 0.80) return 'text-yellow-600';
      return 'text-red-600';
    }
  };

  const getScoreBg = (score: number, inverse: boolean = false) => {
    if (inverse) {
      if (score < 0.05) return 'bg-green-100';
      if (score < 0.10) return 'bg-yellow-100';
      return 'bg-red-100';
    } else {
      if (score >= 0.95) return 'bg-green-100';
      if (score >= 0.80) return 'bg-yellow-100';
      return 'bg-red-100';
    }
  };

  const getCertificationBadge = (level: string) => {
    const badges = {
      'LEVEL_1_MATHEMATICAL': { color: 'bg-gray-200 text-gray-800', icon: '📐' },
      'LEVEL_2_SMART_CONTRACT': { color: 'bg-blue-200 text-blue-800', icon: '🔐' },
      'LEVEL_3_AI_AGENT': { color: 'bg-purple-200 text-purple-800', icon: '🤖' },
      'LEVEL_4_OPERATIONAL': { color: 'bg-green-200 text-green-800', icon: '✅' },
      'LEVEL_5_REGULATORY': { color: 'bg-gold-200 text-gold-800', icon: '🏆' }
    };
    return badges[level as keyof typeof badges] || badges['LEVEL_1_MATHEMATICAL'];
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!metrics || !qualitative) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-4 text-gray-600">No trust metrics available</p>
      </div>
    );
  }

  const overallScore = (
    metrics.epi_compliance_rate * 0.3 +
    metrics.thought_log_completeness * 0.2 +
    (1 - metrics.guardian_veto_rate / 0.05) * 0.15 +
    (1 - metrics.incident_response_time / 24) * 0.15 +
    metrics.stakeholder_satisfaction * 0.2
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Synthetic Trust Metrics</h2>
            <p className="mt-1 text-blue-100">Building confidence through verification</p>
          </div>
          <Shield className="h-16 w-16 opacity-50" />
        </div>
        
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/10 rounded-lg p-4">
            <div className="text-sm text-blue-100">Overall Trust Score</div>
            <div className="text-3xl font-bold mt-1">{(overallScore * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <div className="text-sm text-blue-100">Total Decisions</div>
            <div className="text-3xl font-bold mt-1">{metrics.total_decisions.toLocaleString()}</div>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <div className="text-sm text-blue-100">Anomalies Detected</div>
            <div className="text-3xl font-bold mt-1">{metrics.anomaly_count}</div>
          </div>
        </div>
      </div>

      {/* Certification Level */}
      {certification && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Certification Level</h3>
          <div className="flex items-center space-x-4">
            <div className={`px-4 py-2 rounded-full ${getCertificationBadge(certification.level).color} text-lg font-semibold`}>
              {getCertificationBadge(certification.level).icon} {certification.name}
            </div>
            <div className="flex-1">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Progress to next level</span>
                <span>{certification.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${certification.progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quantitative Metrics */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Quantitative Trust Indicators</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* EPI Compliance Rate */}
          <div className={`p-4 rounded-lg ${getScoreBg(metrics.epi_compliance_rate)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">EPI Compliance Rate</div>
              {metrics.epi_compliance_rate >= 0.95 ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-yellow-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(metrics.epi_compliance_rate)}`}>
              {(metrics.epi_compliance_rate * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-600 mt-1">Target: &gt;95%</div>
          </div>

          {/* Thought Log Completeness */}
          <div className={`p-4 rounded-lg ${getScoreBg(metrics.thought_log_completeness)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">Thought Log Completeness</div>
              {metrics.thought_log_completeness === 1.0 ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-yellow-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(metrics.thought_log_completeness)}`}>
              {(metrics.thought_log_completeness * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-600 mt-1">Target: 100%</div>
          </div>

          {/* Guardian Veto Rate */}
          <div className={`p-4 rounded-lg ${getScoreBg(metrics.guardian_veto_rate, true)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">Guardian Veto Rate</div>
              {metrics.guardian_veto_rate < 0.05 ? (
                <TrendingDown className="h-5 w-5 text-green-600" />
              ) : (
                <TrendingUp className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(metrics.guardian_veto_rate, true)}`}>
              {(metrics.guardian_veto_rate * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-600 mt-1">Target: &lt;5%</div>
          </div>

          {/* Incident Response Time */}
          <div className={`p-4 rounded-lg ${getScoreBg(1 - metrics.incident_response_time / 24)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">Incident Response Time</div>
              {metrics.incident_response_time < 24 ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(1 - metrics.incident_response_time / 24)}`}>
              {metrics.incident_response_time.toFixed(1)}h
            </div>
            <div className="text-xs text-gray-600 mt-1">Target: &lt;24h</div>
          </div>

          {/* Stakeholder Satisfaction */}
          <div className={`p-4 rounded-lg ${getScoreBg(metrics.stakeholder_satisfaction)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">Stakeholder Satisfaction</div>
              {metrics.stakeholder_satisfaction >= 0.80 ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-yellow-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(metrics.stakeholder_satisfaction)}`}>
              {(metrics.stakeholder_satisfaction * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-600 mt-1">Target: &gt;80%</div>
          </div>

          {/* Average EPI Score */}
          <div className={`p-4 rounded-lg ${getScoreBg(metrics.avg_epi_score)}`}>
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-700">Average EPI Score</div>
              {metrics.avg_epi_score >= 0.70 ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div className={`text-2xl font-bold mt-2 ${getScoreColor(metrics.avg_epi_score)}`}>
              {metrics.avg_epi_score.toFixed(3)}
            </div>
            <div className="text-xs text-gray-600 mt-1">Threshold: 0.700</div>
          </div>
        </div>
      </div>

      {/* Qualitative Indicators */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Qualitative Trust Indicators</h3>
        <div className="space-y-4">
          {Object.entries(qualitative).map(([key, value]) => (
            <div key={key}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium capitalize">{key}</span>
                <span className={getScoreColor(value)}>{(value * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-300 ${
                    value >= 0.95 ? 'bg-green-600' : value >= 0.80 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${value * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Health */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">System Health</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-sm text-gray-600">Uptime</div>
            <div className="text-2xl font-bold text-green-600">{metrics.uptime_percentage.toFixed(2)}%</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Anomalies</div>
            <div className={`text-2xl font-bold ${metrics.anomaly_count > 10 ? 'text-red-600' : 'text-green-600'}`}>
              {metrics.anomaly_count}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
