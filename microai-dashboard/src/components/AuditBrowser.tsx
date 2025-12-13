/**
 * AuditBrowser - Event log explorer with search and filtering
 * 
 * Features:
 * - Browse all logged events
 * - Filter by agent, date, action type
 * - View event details
 * - Verify cryptographic signatures
 * - Export audit trails
 */

import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Search, Filter, Download, Eye, Shield, Calendar, User } from 'lucide-react';

interface TrustEvent {
  event_id: string;
  timestamp: string;
  tenant_id: string;
  agent_id: string;
  action_type: string;
  model: string | null;
  input_hash: string;
  output_hash: string;
  policy_version: string;
  epi_score: number | null;
  tools_called: string[];
  redactions: string[];
  evaluations: any[];
  signature: string;
}

export function AuditBrowser() {
  const [events, setEvents] = useState<TrustEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState<string>('all');
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [selectedEvent, setSelectedEvent] = useState<TrustEvent | null>(null);

  useEffect(() => {
    fetchEvents();
  }, [selectedAgent, selectedDate]);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      let url = 'http://localhost:5000/api/trust/events/date/' + selectedDate;
      
      if (selectedAgent !== 'all') {
        url = `http://localhost:5000/api/trust/events/agent/${selectedAgent}?limit=50`;
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch events');
      
      const data = await response.json();
      setEvents(data.events || []);
    } catch (err) {
      console.error('Error fetching events:', err);
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action: string) => {
    const colors: Record<string, string> = {
      'proposal': 'bg-blue-100 text-blue-800',
      'payment': 'bg-green-100 text-green-800',
      'vote': 'bg-purple-100 text-purple-800',
      'decision': 'bg-yellow-100 text-yellow-800',
      'strategy': 'bg-pink-100 text-pink-800',
      'compliance_check': 'bg-gray-100 text-gray-800',
      'strategic_proposal': 'bg-indigo-100 text-indigo-800',
      'budget_allocation': 'bg-orange-100 text-orange-800'
    };
    return colors[action] || 'bg-gray-100 text-gray-800';
  };

  const getEPIBadge = (score: number | null) => {
    if (score === null) return null;
    
    if (score >= 0.8) {
      return <Badge className="bg-green-500 text-white">EPI: {score.toFixed(3)}</Badge>;
    } else if (score >= 0.6) {
      return <Badge className="bg-yellow-500 text-white">EPI: {score.toFixed(3)}</Badge>;
    } else {
      return <Badge className="bg-red-500 text-white">EPI: {score.toFixed(3)}</Badge>;
    }
  };

  const exportAuditTrail = () => {
    const dataStr = JSON.stringify(events, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `audit-trail-${selectedDate}.json`;
    link.click();
  };

  return (
    <div className="space-y-4">
      {/* Filters */}
      <Card className="p-4">
        <div className="flex flex-wrap items-center gap-4">
          {/* Date Filter */}
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-gray-500" />
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Agent Filter */}
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-gray-500" />
            <select
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Agents</option>
              <option value="CEO-AI">CEO-AI</option>
              <option value="CFO-AI">CFO-AI</option>
              <option value="EXECAI">EXECAI</option>
              <option value="Strategic-Catalyst">Strategic Catalyst</option>
            </select>
          </div>

          {/* Export Button */}
          <Button
            onClick={exportAuditTrail}
            variant="outline"
            size="sm"
            className="ml-auto"
            disabled={events.length === 0}
          >
            <Download className="w-4 h-4 mr-2" />
            Export Audit Trail
          </Button>
        </div>
      </Card>

      {/* Events List */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Audit Trail</h2>
            <p className="text-sm text-gray-600">
              {events.length} events {selectedAgent !== 'all' ? `from ${selectedAgent}` : `on ${selectedDate}`}
            </p>
          </div>
          <Shield className="w-8 h-8 text-blue-600" />
        </div>

        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="h-24 bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <Shield className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No events found for the selected filters</p>
          </div>
        ) : (
          <div className="space-y-3">
            {events.map((event) => (
              <div
                key={event.event_id}
                className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer"
                onClick={() => setSelectedEvent(event)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Badge className={getActionColor(event.action_type)}>
                        {event.action_type.replace('_', ' ')}
                      </Badge>
                      <span className="font-semibold text-gray-900">{event.agent_id}</span>
                      {getEPIBadge(event.epi_score)}
                    </div>
                    
                    <div className="text-sm text-gray-600 space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs text-gray-500">
                          {event.event_id.substring(0, 8)}...
                        </span>
                        <span>•</span>
                        <span>{new Date(event.timestamp).toLocaleString()}</span>
                      </div>
                      
                      {event.tools_called.length > 0 && (
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-xs text-gray-500">Tools:</span>
                          {event.tools_called.map((tool, i) => (
                            <Badge key={i} variant="secondary" className="text-xs">
                              {tool}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedEvent(event);
                    }}
                  >
                    <Eye className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Event Details Modal */}
      {selectedEvent && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedEvent(null)}
        >
          <Card 
            className="max-w-3xl w-full max-h-[80vh] overflow-auto p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-gray-900">Event Details</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedEvent(null)}
                >
                  ✕
                </Button>
              </div>

              <div className="space-y-3 text-sm">
                <div>
                  <span className="font-semibold text-gray-700">Event ID:</span>
                  <p className="font-mono text-gray-600 mt-1">{selectedEvent.event_id}</p>
                </div>

                <div>
                  <span className="font-semibold text-gray-700">Timestamp:</span>
                  <p className="text-gray-600 mt-1">{new Date(selectedEvent.timestamp).toLocaleString()}</p>
                </div>

                <div>
                  <span className="font-semibold text-gray-700">Agent:</span>
                  <p className="text-gray-600 mt-1">{selectedEvent.agent_id}</p>
                </div>

                <div>
                  <span className="font-semibold text-gray-700">Action Type:</span>
                  <p className="text-gray-600 mt-1">{selectedEvent.action_type}</p>
                </div>

                {selectedEvent.epi_score !== null && (
                  <div>
                    <span className="font-semibold text-gray-700">EPI Score:</span>
                    <p className="text-gray-600 mt-1">{selectedEvent.epi_score.toFixed(3)}</p>
                  </div>
                )}

                <div>
                  <span className="font-semibold text-gray-700">Input Hash:</span>
                  <p className="font-mono text-xs text-gray-600 mt-1 break-all">{selectedEvent.input_hash}</p>
                </div>

                <div>
                  <span className="font-semibold text-gray-700">Output Hash:</span>
                  <p className="font-mono text-xs text-gray-600 mt-1 break-all">{selectedEvent.output_hash}</p>
                </div>

                <div>
                  <span className="font-semibold text-gray-700">Signature:</span>
                  <p className="font-mono text-xs text-gray-600 mt-1 break-all">{selectedEvent.signature}</p>
                </div>

                {selectedEvent.evaluations.length > 0 && (
                  <div>
                    <span className="font-semibold text-gray-700">Evaluations:</span>
                    <div className="mt-2 space-y-2">
                      {selectedEvent.evaluations.map((eval: any, i: number) => (
                        <div key={i} className="p-2 bg-gray-50 rounded border border-gray-200">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-medium">{eval.evaluator}</span>
                            <Badge className={eval.result === 'pass' ? 'bg-green-500' : 'bg-red-500'}>
                              {eval.result}
                            </Badge>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            Category: {eval.category} • Confidence: {(eval.confidence * 100).toFixed(0)}%
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-gray-200">
                <Button
                  onClick={() => window.open(`/trust/verify/${selectedEvent.event_id}`, '_blank')}
                  className="w-full"
                >
                  <Shield className="w-4 h-4 mr-2" />
                  Verify Cryptographic Proof
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
