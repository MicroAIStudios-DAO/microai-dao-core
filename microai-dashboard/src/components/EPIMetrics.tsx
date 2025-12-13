/**
 * EPIMetrics - EPI score visualization and breakdown
 * 
 * Displays:
 * - Overall EPI score with visual indicator
 * - Component breakdown (profit, ethics, balance, trust)
 * - Historical trend
 * - Optimization suggestions
 */

import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Progress } from './ui/progress';
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle2, Lightbulb } from 'lucide-react';

interface EPIResult {
  epi_score: number;
  is_valid: boolean;
  recommendation: string;
  components: {
    ethical: number;
    profitability: number;
    harmonic_mean: number;
    balance_penalty: number;
    trust: number;
    balance_ratio: number;
  };
  golden_ratio_deviation: number;
  confidence: number;
  reason: string;
  optimization_suggestions: string[];
}

interface EPIMetricsProps {
  profit?: number;
  ethics?: number;
  violations?: number[];
}

export function EPIMetrics({ profit = 0.75, ethics = 0.85, violations = [] }: EPIMetricsProps) {
  const [epiResult, setEpiResult] = useState<EPIResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    calculateEPI();
  }, [profit, ethics, violations]);

  const calculateEPI = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/epi/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profit,
          ethics,
          violations,
          stakeholder_sentiment: 0.7,
          transparency_score: 0.8,
          sustainability_score: 0.75,
          compliance_score: 0.9
        })
      });

      if (!response.ok) throw new Error('Failed to calculate EPI');
      const data = await response.json();
      setEpiResult(data);
    } catch (err) {
      console.error('EPI calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading || !epiResult) {
    return (
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          <div className="h-24 bg-gray-200 rounded"></div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">EPI Metrics</h2>
            <p className="text-sm text-gray-600">Ethical Profitability Index Analysis</p>
          </div>
          {epiResult.is_valid ? (
            <CheckCircle2 className="w-8 h-8 text-green-600" />
          ) : (
            <AlertTriangle className="w-8 h-8 text-red-600" />
          )}
        </div>

        {/* Main EPI Score */}
        <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <span className="text-lg font-semibold text-gray-700">Overall EPI Score</span>
            <div className="flex items-center gap-2">
              {epiResult.epi_score >= 0.7 ? (
                <TrendingUp className="w-5 h-5 text-green-600" />
              ) : (
                <TrendingDown className="w-5 h-5 text-red-600" />
              )}
              <span className={`text-4xl font-bold ${getScoreColor(epiResult.epi_score)}`}>
                {epiResult.epi_score.toFixed(3)}
              </span>
            </div>
          </div>
          
          <Progress 
            value={epiResult.epi_score * 100} 
            className="h-3"
          />
          
          <div className="mt-4 flex items-center justify-between text-sm">
            <span className="text-gray-600">Threshold: 0.700</span>
            <span className={`font-medium ${epiResult.is_valid ? 'text-green-600' : 'text-red-600'}`}>
              {epiResult.is_valid ? '✓ Valid' : '✗ Below Threshold'}
            </span>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-900">
              <strong>Recommendation:</strong> {epiResult.recommendation}
            </p>
          </div>
        </div>

        {/* Component Breakdown */}
        <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Component Breakdown</h3>
          
          <div className="space-y-4">
            {/* Profitability */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Profitability</span>
                <span className="text-sm font-bold text-gray-900">
                  {epiResult.components.profitability.toFixed(3)}
                </span>
              </div>
              <Progress 
                value={epiResult.components.profitability * 100}
                className="h-2"
              />
            </div>

            {/* Ethics */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Ethics</span>
                <span className="text-sm font-bold text-gray-900">
                  {epiResult.components.ethical.toFixed(3)}
                </span>
              </div>
              <Progress 
                value={epiResult.components.ethical * 100}
                className="h-2"
              />
            </div>

            {/* Harmonic Mean */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Harmonic Mean</span>
                <span className="text-sm font-bold text-gray-900">
                  {epiResult.components.harmonic_mean.toFixed(3)}
                </span>
              </div>
              <Progress 
                value={epiResult.components.harmonic_mean * 100}
                className="h-2"
              />
            </div>

            {/* Balance Penalty */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Balance Penalty</span>
                <span className="text-sm font-bold text-gray-900">
                  {epiResult.components.balance_penalty.toFixed(3)}
                </span>
              </div>
              <Progress 
                value={epiResult.components.balance_penalty * 100}
                className="h-2"
              />
              <p className="text-xs text-gray-500 mt-1">
                Golden ratio deviation: {epiResult.golden_ratio_deviation.toFixed(3)}
              </p>
            </div>

            {/* Trust */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Trust Accumulator</span>
                <span className="text-sm font-bold text-gray-900">
                  {epiResult.components.trust.toFixed(3)}
                </span>
              </div>
              <Progress 
                value={epiResult.components.trust * 100}
                className="h-2"
              />
              <p className="text-xs text-gray-500 mt-1">
                Violations: {violations.length}
              </p>
            </div>
          </div>
        </div>

        {/* Optimization Suggestions */}
        {epiResult.optimization_suggestions && epiResult.optimization_suggestions.length > 0 && (
          <div className="bg-white rounded-lg p-6 shadow-sm border border-yellow-200">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="w-5 h-5 text-yellow-600" />
              <h3 className="text-lg font-semibold text-gray-900">Optimization Suggestions</h3>
            </div>
            <ul className="space-y-2">
              {epiResult.optimization_suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                  <span className="text-yellow-600 mt-0.5">•</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Confidence & Reason */}
        <div className="flex items-center justify-between text-sm text-gray-600 pt-4 border-t border-gray-200">
          <span>Confidence: {(epiResult.confidence * 100).toFixed(1)}%</span>
          <span className="italic">{epiResult.reason}</span>
        </div>
      </div>
    </Card>
  );
}
