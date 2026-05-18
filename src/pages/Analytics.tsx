import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  TrendingUp,
  Activity,
  PieChart as PieChartIcon,
  BarChart3,
  Calendar,
  Download,
} from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { ThreatDistributionChart } from '../components/charts/ThreatDistributionChart';
import { ScanFrequencyChart } from '../components/charts/ScanFrequencyChart';
import { ConfidenceTrendChart } from '../components/charts/ConfidenceTrendChart';
import { ActivityTimelineChart } from '../components/charts/ActivityTimelineChart';

export const Analytics = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('30d');

  // Mock data - replace with real API calls
  const threatDistribution = {
    high: 18,
    medium: 45,
    low: 184,
  };

  const scanFrequency = [
    { date: 'Mon', scans: 45, threats: 8 },
    { date: 'Tue', scans: 52, threats: 12 },
    { date: 'Wed', scans: 38, threats: 6 },
    { date: 'Thu', scans: 61, threats: 15 },
    { date: 'Fri', scans: 48, threats: 9 },
    { date: 'Sat', scans: 35, threats: 5 },
    { date: 'Sun', scans: 28, threats: 3 },
  ];

  const confidenceTrend = [
    { date: 'Week 1', avgConfidence: 94, detectionRate: 92 },
    { date: 'Week 2', avgConfidence: 96, detectionRate: 94 },
    { date: 'Week 3', avgConfidence: 95, detectionRate: 96 },
    { date: 'Week 4', avgConfidence: 97, detectionRate: 95 },
  ];

  const activityTimeline = [
    { hour: '00:00', activity: 3 },
    { hour: '03:00', activity: 2 },
    { hour: '06:00', activity: 5 },
    { hour: '09:00', activity: 18 },
    { hour: '12:00', activity: 25 },
    { hour: '15:00', activity: 22 },
    { hour: '18:00', activity: 15 },
    { hour: '21:00', activity: 8 },
  ];

  const stats = [
    {
      label: 'Total Analyses',
      value: '247',
      change: '+12.5%',
      trend: 'up',
      icon: <Activity className="w-5 h-5" />,
      color: 'cyber',
    },
    {
      label: 'Avg Confidence',
      value: '96.2%',
      change: '+2.1%',
      trend: 'up',
      icon: <TrendingUp className="w-5 h-5" />,
      color: 'success',
    },
    {
      label: 'Detection Rate',
      value: '94.8%',
      change: '+1.8%',
      trend: 'up',
      icon: <PieChartIcon className="w-5 h-5" />,
      color: 'primary',
    },
    {
      label: 'Threats Blocked',
      value: '18',
      change: '+5',
      trend: 'up',
      icon: <BarChart3 className="w-5 h-5" />,
      color: 'danger',
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="section-container py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">Analytics Dashboard</h1>
              <p className="text-slate-400">Comprehensive security insights and trends</p>
            </div>
            <div className="flex items-center gap-3">
              {/* Time Range Selector */}
              <div className="flex items-center gap-2 glass rounded-lg p-1">
                {(['7d', '30d', '90d'] as const).map((range) => (
                  <button
                    key={range}
                    onClick={() => setTimeRange(range)}
                    className={`px-4 py-2 rounded-md text-sm font-semibold transition-all ${
                      timeRange === range
                        ? 'bg-cyber-500 text-white'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {range === '7d' ? '7 Days' : range === '30d' ? '30 Days' : '90 Days'}
                  </button>
                ))}
              </div>
              <Button variant="secondary" icon={<Download className="w-4 h-4" />}>
                Export
              </Button>
            </div>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="relative overflow-hidden">
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-xl bg-gradient-to-br from-${stat.color}-500/20 to-${stat.color}-600/20`}>
                    <div className={`text-${stat.color}-400`}>{stat.icon}</div>
                  </div>
                  <span className={`text-sm font-semibold ${stat.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                    {stat.change}
                  </span>
                </div>
                <div className="text-3xl font-bold mb-1">{stat.value}</div>
                <div className="text-sm text-slate-400">{stat.label}</div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Scan Frequency */}
          <Card>
            <div className="flex items-center gap-2 mb-6">
              <Calendar className="w-5 h-5 text-cyber-400" />
              <h2 className="text-xl font-semibold">Scan Frequency</h2>
            </div>
            <ScanFrequencyChart data={scanFrequency} />
          </Card>

          {/* Threat Distribution */}
          <Card>
            <div className="flex items-center gap-2 mb-6">
              <PieChartIcon className="w-5 h-5 text-primary-400" />
              <h2 className="text-xl font-semibold">Threat Distribution</h2>
            </div>
            <ThreatDistributionChart data={threatDistribution} />
          </Card>

          {/* Confidence Trend */}
          <Card>
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="w-5 h-5 text-purple-400" />
              <h2 className="text-xl font-semibold">Confidence & Detection Trends</h2>
            </div>
            <ConfidenceTrendChart data={confidenceTrend} />
          </Card>

          {/* Activity Timeline */}
          <Card>
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="w-5 h-5 text-green-400" />
              <h2 className="text-xl font-semibold">Activity Timeline</h2>
            </div>
            <ActivityTimelineChart data={activityTimeline} />
          </Card>
        </div>

        {/* Insights Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card className="bg-gradient-to-r from-cyber-500/10 to-primary-500/10 border-cyber-500/30">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-cyber-500/20 flex items-center justify-center flex-shrink-0">
                <TrendingUp className="w-6 h-6 text-cyber-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-2">AI Insights</h3>
                <div className="space-y-2 text-slate-300">
                  <p>
                    • Your detection accuracy has improved by <span className="text-green-400 font-semibold">2.1%</span> this week
                  </p>
                  <p>
                    • Peak activity hours are between <span className="text-cyber-400 font-semibold">12:00 - 15:00</span>
                  </p>
                  <p>
                    • <span className="text-primary-400 font-semibold">94.8%</span> of threats were successfully identified
                  </p>
                  <p>
                    • Most common threat type: <span className="text-yellow-400 font-semibold">Phishing attempts</span>
                  </p>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};
