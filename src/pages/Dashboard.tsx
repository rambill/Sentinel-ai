import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import {
  Shield,
  FileText,
  Image as ImageIcon,
  TrendingUp,
  Activity,
  Zap,
  Eye,
  Clock,
  BarChart3,
} from 'lucide-react';
import { Card } from '../components/ui/Card';
import { ProgressBar } from '../components/ui/ProgressBar';
import { SkeletonDashboard } from '../components/ui/Skeleton';
import { useAuthStore } from '../store/authStore';
import { ThreatDistributionChart } from '../components/charts/ThreatDistributionChart';
import { ScanFrequencyChart } from '../components/charts/ScanFrequencyChart';
import api from '../lib/api';

export const Dashboard = () => {
  const { user } = useAuthStore();
  const [statistics, setStatistics] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [scanFrequency, setScanFrequency] = useState<any[]>([]);
  const [avgResponseTime, setAvgResponseTime] = useState('0.0');
  const [successRate, setSuccessRate] = useState('100.0');
  const [systemUptime, setSystemUptime] = useState('100.0');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch user statistics
      const statsResponse = await api.get('/api/statistics');
      setStatistics(statsResponse.data);

      // Fetch recent history
      const historyResponse = await api.get('/api/history?limit=5');
      setHistory(historyResponse.data.history || []);
      
      // Fetch scan frequency (last 7 days) - REAL DATA
      try {
        const frequencyResponse = await api.get('/api/scan-frequency?days=7');
        const frequencyData = frequencyResponse.data.frequency || [];
        
        // Format for chart
        const formattedFrequency = frequencyData.map((day: any) => ({
          date: new Date(day.scan_date).toLocaleDateString('en-US', { weekday: 'short' }),
          scans: day.total_scans || 0,
          threats: day.threats_detected || 0,
        }));
        setScanFrequency(formattedFrequency);
      } catch (error) {
        console.error('Error fetching scan frequency:', error);
        setScanFrequency([]);
      }
      
      // Fetch performance metrics - REAL DATA
      try {
        const perfResponse = await api.get('/api/performance?hours=24');
        const perfData = perfResponse.data.metrics || {};
        
        // Calculate average response time
        const textTime = perfData.text?.avg_response_time_ms || 0;
        const imageTime = perfData.image?.avg_response_time_ms || 0;
        const avgTime = textTime && imageTime ? (textTime + imageTime) / 2 : textTime || imageTime || 0;
        setAvgResponseTime((avgTime / 1000).toFixed(1)); // Convert to seconds
        
        // Calculate success rate
        const textSuccess = perfData.text?.success_rate || 100;
        const imageSuccess = perfData.image?.success_rate || 100;
        const avgSuccess = (textSuccess + imageSuccess) / 2;
        setSuccessRate(avgSuccess.toFixed(1));
      } catch (error) {
        console.error('Error fetching performance metrics:', error);
        setAvgResponseTime('0.0');
        setSuccessRate('100.0');
      }
      
      // Fetch system health - REAL DATA
      try {
        const healthResponse = await api.get('/api/system-health');
        const healthData = healthResponse.data;
        setSystemUptime(healthData.uptime_percentage?.toFixed(1) || '100.0');
      } catch (error) {
        console.error('Error fetching system health:', error);
        setSystemUptime('100.0');
      }
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Set defaults if API fails
      setStatistics({
        totalScans: 0,
        threatsDetected: 0,
        avgConfidence: 0,
        securityScore: 100,
      });
      setScanFrequency([]);
      setAvgResponseTime('0.0');
      setSuccessRate('100.0');
      setSystemUptime('100.0');
    } finally {
      setLoading(false);
    }
  };

  const recentAnalyses = history.slice(0, 3).map((item: any) => ({
    id: item.id,
    type: item.type,
    content: item.content,
    result: item.result,
    confidence: item.confidence,
    timestamp: new Date(item.timestamp).toLocaleString(),
    threat: item.threat_level,
  }));

  const stats = [
    {
      label: 'Total Scans',
      value: statistics?.totalScans?.toString() || '0',
      change: statistics?.totalScans > 0 ? `+${statistics.totalScans}` : '0',
      icon: <Activity className="w-5 h-5" />,
      color: 'cyber',
    },
    {
      label: 'Threats Blocked',
      value: statistics?.threatsDetected?.toString() || '0',
      change: statistics?.threatsDetected > 0 ? `+${statistics.threatsDetected}` : '0',
      icon: <Shield className="w-5 h-5" />,
      color: 'danger',
    },
    {
      label: 'Avg Confidence',
      value: `${statistics?.avgConfidence?.toFixed(1) || '0'}%`,
      change: statistics?.avgConfidence > 0 ? `${statistics.avgConfidence.toFixed(1)}%` : '0%',
      icon: <TrendingUp className="w-5 h-5" />,
      color: 'success',
    },
    {
      label: 'Response Time',
      value: `${avgResponseTime}s`,
      change: avgResponseTime !== '0.0' ? `${avgResponseTime}s` : '0s',
      icon: <Zap className="w-5 h-5" />,
      color: 'primary',
    },
  ];

  // REAL DATA - from API
  const threatDistribution = {
    high: statistics?.highRiskDetections || 0,
    medium: statistics?.mediumRiskDetections || 0,
    low: statistics?.lowRiskDetections || 0,
  };

  const quickActions = [
    {
      title: 'Analyze Text',
      description: 'Check suspicious messages',
      icon: <FileText className="w-6 h-6" />,
      link: '/analyze-text',
      gradient: 'from-cyber-500 to-primary-500',
    },
    {
      title: 'Scan Image',
      description: 'Detect fake media',
      icon: <ImageIcon className="w-6 h-6" />,
      link: '/analyze-image',
      gradient: 'from-primary-500 to-purple-500',
    },
  ];

  const getThreatColor = (threat: string) => {
    switch (threat) {
      case 'high':
        return 'text-danger-400 bg-danger-500/10';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10';
      case 'low':
        return 'text-green-400 bg-green-500/10';
      default:
        return 'text-slate-400 bg-slate-500/10';
    }
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="section-container py-8">
        {loading ? (
          <SkeletonDashboard />
        ) : (
          <>
            {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold mb-2">
            Welcome back, <span className="gradient-text">{user?.user_metadata?.name || 'User'}</span>
          </h1>
          <p className="text-slate-400">Here's your security overview for today</p>
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
                  <span className={`text-sm font-semibold ${stat.change.startsWith('+') || stat.change.includes('%') ? 'text-green-400' : 'text-cyber-400'}`}>
                    {stat.change}
                  </span>
                </div>
                <div className="text-3xl font-bold mb-1">{stat.value}</div>
                <div className="text-sm text-slate-400">{stat.label}</div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8"
        >
          <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {quickActions.map((action, index) => (
              <Link key={index} to={action.link}>
                <Card hover className="group">
                  <div className="flex items-center gap-4">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${action.gradient} flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform`}>
                      <div className="text-white">{action.icon}</div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold mb-1">{action.title}</h3>
                      <p className="text-slate-400">{action.description}</p>
                    </div>
                    <div className="text-slate-400 group-hover:text-cyber-400 transition-colors">
                      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </motion.div>

        {/* Security Score Widget */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-8"
        >
          <Card>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-semibold mb-1">Security Score</h3>
                <p className="text-slate-400">Your overall protection level</p>
              </div>
              <div className="text-4xl font-bold gradient-text">
                {statistics?.securityScore >= 90 ? 'A+' : statistics?.securityScore >= 80 ? 'A' : statistics?.securityScore >= 70 ? 'B' : statistics?.securityScore >= 60 ? 'C' : 'D'}
              </div>
            </div>
            <ProgressBar value={statistics?.securityScore || 100} color="cyber" showLabel />
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">{statistics?.threatsDetected || 0}</div>
                <div className="text-xs text-slate-400">Threats Blocked</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-cyber-400">{statistics?.totalScans || 0}</div>
                <div className="text-xs text-slate-400">Total Scans</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-400">{successRate}%</div>
                <div className="text-xs text-slate-400">Success Rate</div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Analytics Charts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Analytics Overview</h2>
            <Link to="/analytics">
              <button className="text-cyber-400 hover:text-cyber-300 text-sm font-semibold transition-colors flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                View Full Analytics
              </button>
            </Link>
          </div>
          <div className="grid lg:grid-cols-2 gap-6">
            <Card>
              <h3 className="text-lg font-semibold mb-4">Scan Frequency (Last 7 Days)</h3>
              {scanFrequency.length > 0 ? (
                <ScanFrequencyChart data={scanFrequency} />
              ) : (
                <div className="flex items-center justify-center h-64 text-slate-400">
                  <div className="text-center">
                    <Activity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p>No scan data yet</p>
                    <p className="text-sm">Perform some analyses to see your activity</p>
                  </div>
                </div>
              )}
            </Card>
            <Card>
              <h3 className="text-lg font-semibold mb-4">Threat Distribution</h3>
              <ThreatDistributionChart data={threatDistribution} />
            </Card>
          </div>
        </motion.div>

        {/* Recent Analyses */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Recent Analyses</h2>
            <button className="text-cyber-400 hover:text-cyber-300 text-sm font-semibold transition-colors">
              View All
            </button>
          </div>
          {recentAnalyses.length > 0 ? (
            <div className="space-y-4">
              {recentAnalyses.map((analysis) => (
                <Card key={analysis.id} hover>
                  <div className="flex items-start gap-4">
                    <div className={`p-3 rounded-xl ${analysis.type === 'text' ? 'bg-cyber-500/20' : 'bg-primary-500/20'}`}>
                      {analysis.type === 'text' ? (
                        <FileText className="w-5 h-5 text-cyber-400" />
                      ) : (
                        <ImageIcon className="w-5 h-5 text-primary-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <p className="text-slate-300 truncate mb-1">{analysis.content}</p>
                          <div className="flex items-center gap-3 text-sm">
                            <span className={`px-2 py-1 rounded-lg font-semibold ${getThreatColor(analysis.threat)}`}>
                              {analysis.result}
                            </span>
                            <span className="text-slate-400 flex items-center gap-1">
                              <Eye className="w-4 h-4" />
                              {analysis.confidence}% confidence
                            </span>
                          </div>
                        </div>
                        <span className="text-xs text-slate-500 flex items-center gap-1 whitespace-nowrap ml-4">
                          <Clock className="w-3 h-3" />
                          {analysis.timestamp}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <div className="flex items-center justify-center h-32 text-slate-400">
                <div className="text-center">
                  <Shield className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No analyses yet</p>
                  <p className="text-sm">Start analyzing text or images to see your history</p>
                </div>
              </div>
            </Card>
          )}
        </motion.div>

        {/* AI Status Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8"
        >
          <Card className="bg-gradient-to-r from-cyber-500/10 to-primary-500/10 border-cyber-500/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                  <div className="absolute inset-0 w-3 h-3 bg-green-400 rounded-full animate-ping" />
                </div>
                <div>
                  <div className="font-semibold">AI Systems Online</div>
                  <div className="text-sm text-slate-400">All detection models operational</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold gradient-text">{systemUptime}%</div>
                <div className="text-xs text-slate-400">Uptime</div>
              </div>
            </div>
          </Card>
        </motion.div>
      </>
    )}
      </div>
    </div>
  );
};
