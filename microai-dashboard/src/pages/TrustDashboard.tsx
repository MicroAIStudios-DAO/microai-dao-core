/**
 * TrustDashboard - Main trust monitoring and verification page
 * 
 * Integrates:
 * - TrustPanel (real-time status)
 * - EPIMetrics (EPI analysis)
 * - AuditBrowser (event logs)
 * - Agent monitoring
 */

import React, { useState } from 'react';
import { TrustPanel } from '../components/TrustPanel';
import { EPIMetrics } from '../components/EPIMetrics';
import { AuditBrowser } from '../components/AuditBrowser';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Shield, TrendingUp, FileText, Users, Activity } from 'lucide-react';

export function TrustDashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2">Trust Dashboard</h1>
              <p className="text-blue-100 text-lg">
                Verifiable AI Governance with Cryptographic Proof
              </p>
            </div>
            <Shield className="w-16 h-16 opacity-80" />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-grid">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="epi" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              EPI Analysis
            </TabsTrigger>
            <TabsTrigger value="audit" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Audit Trail
            </TabsTrigger>
            <TabsTrigger value="agents" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              AI Agents
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <TrustPanel />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <EPIMetrics profit={0.75} ethics={0.85} violations={[]} />
              
              <Card className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">System Health</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="font-medium text-gray-900">API Server</span>
                    </div>
                    <Badge className="bg-green-500 text-white">Operational</Badge>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="font-medium text-gray-900">Event Logger</span>
                    </div>
                    <Badge className="bg-green-500 text-white">Active</Badge>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="font-medium text-gray-900">EPI Calculator</span>
                    </div>
                    <Badge className="bg-green-500 text-white">Ready</Badge>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                      <span className="font-medium text-gray-900">Merkle Anchoring</span>
                    </div>
                    <Badge className="bg-yellow-500 text-white">Pending</Badge>
                  </div>
                </div>
              </Card>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                <div className="text-sm font-medium text-blue-700 mb-1">Total Events</div>
                <div className="text-3xl font-bold text-blue-900">1,247</div>
                <div className="text-xs text-blue-600 mt-1">↑ 12% from last week</div>
              </Card>
              
              <Card className="p-4 bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                <div className="text-sm font-medium text-green-700 mb-1">Avg EPI Score</div>
                <div className="text-3xl font-bold text-green-900">0.823</div>
                <div className="text-xs text-green-600 mt-1">✓ Above threshold</div>
              </Card>
              
              <Card className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                <div className="text-sm font-medium text-purple-700 mb-1">Active Agents</div>
                <div className="text-3xl font-bold text-purple-900">3</div>
                <div className="text-xs text-purple-600 mt-1">CEO, CFO, EXECAI</div>
              </Card>
              
              <Card className="p-4 bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                <div className="text-sm font-medium text-orange-700 mb-1">Trust Badge</div>
                <div className="text-3xl font-bold text-orange-900">Bronze</div>
                <div className="text-xs text-orange-600 mt-1">Upgrade to Silver</div>
              </Card>
            </div>
          </TabsContent>

          {/* EPI Analysis Tab */}
          <TabsContent value="epi" className="space-y-6">
            <EPIMetrics profit={0.75} ethics={0.85} violations={[]} />
            
            <Card className="p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">EPI Optimization</h3>
              <div className="space-y-4">
                <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-2">Golden Ratio Balance</h4>
                  <p className="text-sm text-blue-800">
                    Your profit-ethics balance is close to the golden ratio (φ ≈ 0.618). 
                    This indicates optimal harmony between profitability and ethical considerations.
                  </p>
                </div>
                
                <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                  <h4 className="font-semibold text-green-900 mb-2">Trust Accumulator</h4>
                  <p className="text-sm text-green-800">
                    No violations detected. Your trust score remains at maximum (1.0). 
                    Continue maintaining ethical standards to preserve stakeholder confidence.
                  </p>
                </div>
                
                <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                  <h4 className="font-semibold text-yellow-900 mb-2">Improvement Opportunity</h4>
                  <p className="text-sm text-yellow-800">
                    Consider increasing transparency score by publishing more detailed decision rationales. 
                    This could boost your overall EPI by 0.05-0.08 points.
                  </p>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Audit Trail Tab */}
          <TabsContent value="audit">
            <AuditBrowser />
          </TabsContent>

          {/* AI Agents Tab */}
          <TabsContent value="agents" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* CEO-AI */}
              <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-900">CEO-AI</h3>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Strategic decision-making agent with EPI constraints
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Proposals</span>
                    <span className="font-semibold text-gray-900">24</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Approval Rate</span>
                    <span className="font-semibold text-green-600">87.5%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Avg EPI Score</span>
                    <span className="font-semibold text-gray-900">0.834</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Model</span>
                    <span className="font-mono text-xs text-gray-700">Phi-3-mini</span>
                  </div>
                </div>
              </Card>

              {/* CFO-AI */}
              <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-900">CFO-AI</h3>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Financial decision-making with budget optimization
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Payments</span>
                    <span className="font-semibold text-gray-900">156</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Approval Rate</span>
                    <span className="font-semibold text-green-600">92.3%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Avg EPI Score</span>
                    <span className="font-semibold text-gray-900">0.812</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Treasury Balance</span>
                    <span className="font-semibold text-green-600">$950K</span>
                  </div>
                </div>
              </Card>

              {/* EXECAI */}
              <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-900">EXECAI</h3>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Autonomous voting agent with 33% voting power
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Votes</span>
                    <span className="font-semibold text-gray-900">89</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Approval Rate</span>
                    <span className="font-semibold text-green-600">78.7%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Avg EPI Score</span>
                    <span className="font-semibold text-gray-900">0.798</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Voting Power</span>
                    <span className="font-semibold text-purple-600">33%</span>
                  </div>
                </div>
              </Card>
            </div>

            {/* Agent Activity Timeline */}
            <Card className="p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Agent Activity</h3>
              <div className="space-y-3">
                <div className="flex items-start gap-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="w-2 h-2 rounded-full bg-blue-500 mt-2"></div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-gray-900">CEO-AI</span>
                      <span className="text-xs text-gray-500">2 minutes ago</span>
                    </div>
                    <p className="text-sm text-gray-700">
                      Submitted strategic proposal: "Healthcare AI Investment" (EPI: 0.847)
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-3 bg-green-50 rounded-lg border border-green-200">
                  <div className="w-2 h-2 rounded-full bg-green-500 mt-2"></div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-gray-900">CFO-AI</span>
                      <span className="text-xs text-gray-500">15 minutes ago</span>
                    </div>
                    <p className="text-sm text-gray-700">
                      Approved payment: $50,000 to Healthcare AI Vendor (EPI: 0.821)
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-3 bg-purple-50 rounded-lg border border-purple-200">
                  <div className="w-2 h-2 rounded-full bg-purple-500 mt-2"></div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-gray-900">EXECAI</span>
                      <span className="text-xs text-gray-500">1 hour ago</span>
                    </div>
                    <p className="text-sm text-gray-700">
                      Voted YES on Proposal #42: "Community Grants Program" (EPI: 0.789)
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
