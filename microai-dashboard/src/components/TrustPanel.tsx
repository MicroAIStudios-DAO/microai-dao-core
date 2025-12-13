/**
 * TrustPanel - Real-time trust status and verification display
 * 
 * Shows:
 * - Trust badge level (Bronze/Silver/Gold)
 * - Live EPI metrics
 * - Event count and verification status
 * - Merkle root anchoring status
 * - Quick verification link
 */

import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Shield, CheckCircle, AlertCircle, ExternalLink, TrendingUp } from 'lucide-react';

interface TrustStatus {
  status: string;
  date: string;
  events_today: number;
  agent_activity: Record<string, { count: number; actions: string[] }>;
  average_epi_score: number;
  trust_badge: string;
  last_anchor: string | null;
}

export function TrustPanel() {
  const [trustStatus, setTrustStatus] = useState<TrustStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTrustStatus();
    // Refresh every 30 seconds
    const interval = setInterval(fetchTrustStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchTrustStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/trust/status');
      if (!response.ok) throw new Error('Failed to fetch trust status');
      const data = await response.json();
      setTrustStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (badge: string) => {
    switch (badge.toLowerCase()) {
      case 'gold':
        return 'bg-yellow-500 text-white';
      case 'silver':
        return 'bg-gray-400 text-white';
      case 'bronze':
        return 'bg-orange-600 text-white';
      default:
        return 'bg-gray-300 text-gray-700';
    }
  };

  const getEPIColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6 border-red-200 bg-red-50">
        <div className="flex items-center gap-2 text-red-600">
          <AlertCircle className="w-5 h-5" />
          <span>Error loading trust status: {error}</span>
        </div>
      </Card>
    );
  }

  if (!trustStatus) return null;

  return (
    <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-600" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Trust Status</h2>
              <p className="text-sm text-gray-600">Real-time verification & monitoring</p>
            </div>
          </div>
          <Badge className={`${getBadgeColor(trustStatus.trust_badge)} text-lg px-4 py-2 font-bold`}>
            {trustStatus.trust_badge} Badge
          </Badge>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* EPI Score */}
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Average EPI</span>
              <TrendingUp className="w-4 h-4 text-gray-400" />
            </div>
            <div className={`text-3xl font-bold ${getEPIColor(trustStatus.average_epi_score)}`}>
              {trustStatus.average_epi_score.toFixed(3)}
            </div>
            <div className="mt-2 text-xs text-gray-500">
              {trustStatus.average_epi_score >= 0.7 ? '✓ Above threshold' : '⚠ Below threshold'}
            </div>
          </div>

          {/* Events Today */}
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Events Today</span>
              <CheckCircle className="w-4 h-4 text-gray-400" />
            </div>
            <div className="text-3xl font-bold text-gray-900">
              {trustStatus.events_today}
            </div>
            <div className="mt-2 text-xs text-gray-500">
              {Object.keys(trustStatus.agent_activity).length} agents active
            </div>
          </div>

          {/* Anchor Status */}
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Merkle Root</span>
              <Shield className="w-4 h-4 text-gray-400" />
            </div>
            <div className="text-sm font-mono text-gray-700 truncate">
              {trustStatus.last_anchor ? trustStatus.last_anchor.substring(0, 16) + '...' : 'Not anchored'}
            </div>
            <div className="mt-2 text-xs text-gray-500">
              {trustStatus.last_anchor ? '✓ Anchored' : '⏳ Pending'}
            </div>
          </div>
        </div>

        {/* Agent Activity */}
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Agent Activity</h3>
          <div className="space-y-2">
            {Object.entries(trustStatus.agent_activity).map(([agent, data]) => (
              <div key={agent} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  <span className="font-medium text-gray-900">{agent}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-600">{data.count} actions</span>
                  <div className="flex gap-1">
                    {[...new Set(data.actions)].slice(0, 3).map((action, i) => (
                      <Badge key={i} variant="secondary" className="text-xs">
                        {action}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Verification Link */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <div className="text-sm text-gray-600">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
          <a
            href="/trust/verify"
            className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
          >
            <span>Verify cryptographic proof</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </Card>
  );
}
