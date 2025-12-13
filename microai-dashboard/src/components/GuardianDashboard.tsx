import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Play, Pause, CheckCircle, XCircle, Clock } from 'lucide-react';

interface Guardian {
  guardian_id: string;
  name: string;
  role: string;
  active: boolean;
  veto_count: number;
  total_actions: number;
  last_action_date: string | null;
}

interface GuardianAction {
  action_id: string;
  guardian_id: string;
  guardian_name: string;
  action_type: string;
  target_id: string;
  reason: string;
  timestamp: string;
}

interface SystemStatus {
  is_paused: boolean;
  pause_reason: string | null;
  paused_by: string | null;
  paused_at: string | null;
  total_guardians: number;
  active_guardians: number;
  class_a_guardians: number;
  total_vetoes: number;
  veto_rate: number;
  total_actions: number;
}

export function GuardianDashboard() {
  const [guardians, setGuardians] = useState<Guardian[]>([]);
  const [recentActions, setRecentActions] = useState<GuardianAction[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGuardianData();
    const interval = setInterval(fetchGuardianData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchGuardianData = async () => {
    try {
      const [guardiansRes, actionsRes, statusRes] = await Promise.all([
        fetch('/api/guardians/list'),
        fetch('/api/guardians/actions/recent'),
        fetch('/api/guardians/status')
      ]);

      const guardiansData = await guardiansRes.json();
      const actionsData = await actionsRes.json();
      const statusData = await statusRes.json();

      setGuardians(guardiansData.guardians || []);
      setRecentActions(actionsData.actions || []);
      setSystemStatus(statusData);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch guardian data:', error);
      setLoading(false);
    }
  };

  const getRoleBadge = (role: string) => {
    const badges = {
      'class_a': { color: 'bg-purple-100 text-purple-800', label: 'Class A' },
      'class_b': { color: 'bg-blue-100 text-blue-800', label: 'Class B' },
      'observer': { color: 'bg-gray-100 text-gray-800', label: 'Observer' }
    };
    return badges[role as keyof typeof badges] || badges['observer'];
  };

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case 'veto':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'approve':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'pause':
        return <Pause className="h-5 w-5 text-orange-600" />;
      case 'resume':
        return <Play className="h-5 w-5 text-green-600" />;
      default:
        return <Shield className="h-5 w-5 text-gray-600" />;
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Guardian Oversight</h2>
            <p className="mt-1 text-purple-100">Human safety net for AI governance</p>
          </div>
          <Shield className="h-16 w-16 opacity-50" />
        </div>
      </div>

      {/* System Status Alert */}
      {systemStatus?.is_paused && (
        <div className="bg-red-50 border-l-4 border-red-600 p-4 rounded">
          <div className="flex items-center">
            <AlertTriangle className="h-6 w-6 text-red-600 mr-3" />
            <div>
              <h3 className="text-lg font-semibold text-red-900">System Paused</h3>
              <p className="text-red-700 mt-1">
                Paused by: {systemStatus.paused_by} at {formatDate(systemStatus.paused_at)}
              </p>
              <p className="text-red-600 mt-1">Reason: {systemStatus.pause_reason}</p>
            </div>
          </div>
        </div>
      )}

      {/* System Statistics */}
      {systemStatus && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm text-gray-600">Total Guardians</div>
            <div className="text-2xl font-bold text-purple-600 mt-1">{systemStatus.total_guardians}</div>
            <div className="text-xs text-gray-500 mt-1">{systemStatus.active_guardians} active</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm text-gray-600">Class A Guardians</div>
            <div className="text-2xl font-bold text-indigo-600 mt-1">{systemStatus.class_a_guardians}</div>
            <div className="text-xs text-gray-500 mt-1">Full authority</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm text-gray-600">Veto Rate</div>
            <div className={`text-2xl font-bold mt-1 ${
              systemStatus.veto_rate < 0.05 ? 'text-green-600' : 
              systemStatus.veto_rate < 0.10 ? 'text-yellow-600' : 'text-red-600'
            }`}>
              {(systemStatus.veto_rate * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-500 mt-1">Target: &lt;5%</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm text-gray-600">Total Actions</div>
            <div className="text-2xl font-bold text-gray-800 mt-1">{systemStatus.total_actions}</div>
            <div className="text-xs text-gray-500 mt-1">{systemStatus.total_vetoes} vetoes</div>
          </div>
        </div>
      )}

      {/* Guardians List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Active Guardians</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {guardians.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500">
              No guardians configured
            </div>
          ) : (
            guardians.map((guardian) => (
              <div key={guardian.guardian_id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                      guardian.active ? 'bg-purple-100' : 'bg-gray-100'
                    }`}>
                      <Shield className={`h-6 w-6 ${
                        guardian.active ? 'text-purple-600' : 'text-gray-400'
                      }`} />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h4 className="font-semibold text-gray-900">{guardian.name}</h4>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          getRoleBadge(guardian.role).color
                        }`}>
                          {getRoleBadge(guardian.role).label}
                        </span>
                        {!guardian.active && (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                            Inactive
                          </span>
                        )}
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        {guardian.total_actions} actions • {guardian.veto_count} vetoes
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-600">Last Action</div>
                    <div className="text-sm font-medium text-gray-900">
                      {formatDate(guardian.last_action_date)}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Recent Actions */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Recent Guardian Actions</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {recentActions.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500">
              No recent actions
            </div>
          ) : (
            recentActions.map((action) => (
              <div key={action.action_id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-start space-x-4">
                  <div className="mt-1">
                    {getActionIcon(action.action_type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="font-semibold text-gray-900">{action.guardian_name}</span>
                        <span className="text-gray-600 mx-2">•</span>
                        <span className="text-gray-700 capitalize">{action.action_type}</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <Clock className="h-4 w-4 mr-1" />
                        {formatDate(action.timestamp)}
                      </div>
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      Target: <span className="font-mono text-xs">{action.target_id}</span>
                    </div>
                    {action.reason && (
                      <div className="text-sm text-gray-700 mt-2 bg-gray-50 p-2 rounded">
                        {action.reason}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Guardian Responsibilities */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-4">Guardian Responsibilities</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-semibold text-blue-800 mb-2">Class A Guardians</h4>
            <ul className="space-y-1 text-blue-700">
              <li>• Veto any proposal</li>
              <li>• Emergency system pause</li>
              <li>• Upgrade authority</li>
              <li>• Dispute resolution</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-blue-800 mb-2">Class B Guardians</h4>
            <ul className="space-y-1 text-blue-700">
              <li>• Veto proposals</li>
              <li>• Review decisions</li>
              <li>• Provide feedback</li>
              <li>• Monitor anomalies</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
