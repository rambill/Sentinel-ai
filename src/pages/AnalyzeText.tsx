import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  AlertTriangle,
  CheckCircle,
  Info,
  Sparkles,
  Shield,
  TrendingUp,
  Eye,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { ProgressBar } from '../components/ui/ProgressBar';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';

interface AnalysisResult {
  isScam: boolean;
  confidence: number;
  threatLevel: 'low' | 'medium' | 'high';
  explanation: string;
  indicators: string[];
  recommendation: string;
}

export const AnalyzeText = () => {
  const [text, setText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      toast.error('Please enter some text to analyze');
      return;
    }

    setAnalyzing(true);
    setResult(null);

    try {
      // Call REAL backend API
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/analyze-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      
      // Map backend response to frontend format
      const analysisResult: AnalysisResult = {
        isScam: data.isScam,
        confidence: data.confidence,
        threatLevel: data.threatLevel,
        explanation: data.explanation,
        indicators: data.indicators || [],
        recommendation: data.recommendation,
      };

      setResult(analysisResult);
      toast.success('Analysis complete!');
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Analysis failed. Make sure the backend is running on port 8000.');
    } finally {
      setAnalyzing(false);
    }
  };

  const getThreatColor = (level: string) => {
    switch (level) {
      case 'high':
        return { bg: 'bg-danger-500/20', text: 'text-danger-400', border: 'border-danger-500/50' };
      case 'medium':
        return { bg: 'bg-yellow-500/20', text: 'text-yellow-400', border: 'border-yellow-500/50' };
      case 'low':
        return { bg: 'bg-green-500/20', text: 'text-green-400', border: 'border-green-500/50' };
      default:
        return { bg: 'bg-slate-500/20', text: 'text-slate-400', border: 'border-slate-500/50' };
    }
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="section-container py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-500 to-primary-500 flex items-center justify-center shadow-glow">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Text Scam Analyzer</h1>
              <p className="text-slate-400">Detect phishing and fraudulent messages</p>
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-cyber-400" />
                <h2 className="text-xl font-semibold">Enter Suspicious Text</h2>
              </div>
              <p className="text-slate-400 text-sm mb-4">
                Paste any suspicious email, SMS, or message below for AI-powered analysis
              </p>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your suspicious message here...&#10;&#10;Example:&#10;URGENT: Your account has been compromised! Click here immediately to verify your identity and prevent account closure."
                className="w-full h-64 px-4 py-3 glass rounded-lg border border-slate-700/50 focus:border-cyber-500 focus:ring-2 focus:ring-cyber-500/20 transition-all duration-300 outline-none text-slate-100 placeholder-slate-500 resize-none"
              />
              <div className="flex items-center justify-between mt-4">
                <span className="text-sm text-slate-400">
                  {text.length} characters
                </span>
                <Button
                  onClick={handleAnalyze}
                  loading={analyzing}
                  disabled={!text.trim() || analyzing}
                  icon={<Shield className="w-5 h-5" />}
                >
                  Analyze Text
                </Button>
              </div>
            </Card>

            {/* Example Messages */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mt-6"
            >
              <Card className="bg-primary-500/5 border-primary-500/20">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-primary-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold mb-2">Tips for best results:</h3>
                    <ul className="text-sm text-slate-400 space-y-1">
                      <li>• Include the entire message with headers if available</li>
                      <li>• Don't modify or clean up the text</li>
                      <li>• Include any links (they won't be clicked)</li>
                    </ul>
                  </div>
                </div>
              </Card>
            </motion.div>
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <AnimatePresence mode="wait">
              {analyzing ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <Card className="h-full flex items-center justify-center min-h-[400px]">
                    <div className="text-center">
                      <LoadingSpinner size="lg" />
                      <p className="mt-4 text-slate-400">Analyzing with AI...</p>
                      <p className="text-sm text-slate-500 mt-2">This may take a few seconds</p>
                    </div>
                  </Card>
                </motion.div>
              ) : result ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="space-y-6"
                >
                  {/* Threat Level Card */}
                  <Card className={`${getThreatColor(result.threatLevel).bg} border-2 ${getThreatColor(result.threatLevel).border}`}>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        {result.isScam ? (
                          <AlertTriangle className={`w-8 h-8 ${getThreatColor(result.threatLevel).text}`} />
                        ) : (
                          <CheckCircle className="w-8 h-8 text-green-400" />
                        )}
                        <div>
                          <h3 className="text-xl font-bold">
                            {result.isScam ? 'Potential Scam Detected' : 'Appears Legitimate'}
                          </h3>
                          <p className={`text-sm ${getThreatColor(result.threatLevel).text} font-semibold uppercase`}>
                            {result.threatLevel} Risk
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span className="text-slate-400">
                          {result.isScam ? 'Scam Confidence' : 'Legitimacy Confidence'}
                        </span>
                        <span className="font-semibold">{result.confidence}%</span>
                      </div>
                      <ProgressBar
                        value={result.confidence}
                        color={result.threatLevel === 'high' ? 'danger' : result.threatLevel === 'medium' ? 'primary' : 'success'}
                        showLabel={false}
                      />
                    </div>
                    
                    {/* Trust Guidance */}
                    <div className="mt-4 p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
                      <div className="flex items-start gap-2">
                        <Info className="w-4 h-4 text-cyber-400 flex-shrink-0 mt-0.5" />
                        <div className="text-sm">
                          <p className="font-semibold text-slate-300 mb-1">Trust Guidance:</p>
                          <p className="text-slate-400">
                            {result.confidence >= 80 ? (
                              result.isScam ? (
                                <span className="text-danger-400">⚠️ <strong>Very High Confidence</strong> - This is almost certainly a scam. Do NOT interact with it.</span>
                              ) : (
                                <span className="text-green-400">✅ <strong>Very High Confidence</strong> - This message appears very safe, but always verify sender identity.</span>
                              )
                            ) : result.confidence >= 60 ? (
                              result.isScam ? (
                                <span className="text-yellow-400">⚠️ <strong>High Confidence</strong> - Strong indicators of a scam. Exercise extreme caution.</span>
                              ) : (
                                <span className="text-green-400">✅ <strong>High Confidence</strong> - Message appears legitimate, but stay vigilant.</span>
                              )
                            ) : result.confidence >= 40 ? (
                              <span className="text-yellow-400">⚡ <strong>Moderate Confidence</strong> - Some suspicious elements detected. Verify through official channels before taking action.</span>
                            ) : (
                              <span className="text-slate-400">ℹ️ <strong>Low Confidence</strong> - Inconclusive results. Use your judgment and verify sender independently.</span>
                            )}
                          </p>
                        </div>
                      </div>
                    </div>
                  </Card>

                  {/* Explanation */}
                  <Card>
                    <div className="flex items-center gap-2 mb-3">
                      <Eye className="w-5 h-5 text-cyber-400" />
                      <h3 className="font-semibold">Analysis</h3>
                    </div>
                    <p className="text-slate-300">{result.explanation}</p>
                  </Card>

                  {/* Indicators */}
                  <Card>
                    <div className="flex items-center gap-2 mb-3">
                      <TrendingUp className="w-5 h-5 text-cyber-400" />
                      <h3 className="font-semibold">Key Indicators</h3>
                    </div>
                    <ul className="space-y-2">
                      {result.indicators.map((indicator, index) => (
                        <li key={index} className="flex items-start gap-2 text-slate-300">
                          <span className={`w-1.5 h-1.5 rounded-full ${result.isScam ? 'bg-danger-400' : 'bg-green-400'} mt-2 flex-shrink-0`} />
                          <span>{indicator}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>

                  {/* Recommendation */}
                  <Card className="bg-cyber-500/10 border-cyber-500/30">
                    <div className="flex items-center gap-2 mb-3">
                      <Shield className="w-5 h-5 text-cyber-400" />
                      <h3 className="font-semibold">Recommendation</h3>
                    </div>
                    <p className="text-slate-300">{result.recommendation}</p>
                  </Card>

                  {/* Action Buttons */}
                  <div className="flex gap-3">
                    <Button
                      variant="secondary"
                      className="flex-1"
                      onClick={() => {
                        setText('');
                        setResult(null);
                      }}
                    >
                      Analyze Another
                    </Button>
                    <Button variant="primary" className="flex-1">
                      Save Report
                    </Button>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <Card className="h-full flex items-center justify-center min-h-[400px]">
                    <div className="text-center max-w-sm">
                      <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyber-500/20 to-primary-500/20 flex items-center justify-center mx-auto mb-4">
                        <FileText className="w-10 h-10 text-cyber-400" />
                      </div>
                      <h3 className="text-xl font-semibold mb-2">Ready to Analyze</h3>
                      <p className="text-slate-400">
                        Enter suspicious text in the input field and click "Analyze Text" to get started
                      </p>
                    </div>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
