import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Image as ImageIcon,
  Upload,
  X,
  AlertTriangle,
  CheckCircle,
  Info,
  Shield,
  Eye,
  Sparkles,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { ProgressBar } from '../components/ui/ProgressBar';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';
import { compressImage, formatFileSize } from '../utils/performance';

interface ImageAnalysisResult {
  isFake: boolean;
  confidence: number;
  threatLevel: 'low' | 'medium' | 'high';
  explanation: string;
  manipulationTypes: string[];
  recommendation: string;
  technicalDetails: {
    resolution: string;
    format: string;
    aiGenerated: boolean;
    deepfakeScore: number;
  };
}

export const AnalyzeImage = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<ImageAnalysisResult | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      toast.error('Please upload an image file');
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    
    // Compress if larger than 2MB
    if (file.size > 2 * 1024 * 1024) {
      try {
        toast.loading('Compressing image...', { id: 'compress' });
        const compressed = await compressImage(file);
        const compressedFile = new File([compressed], file.name, { type: file.type });
        
        toast.success(
          `Compressed from ${formatFileSize(file.size)} to ${formatFileSize(compressedFile.size)}`,
          { id: 'compress' }
        );
        
        file = compressedFile;
      } catch (error) {
        toast.error('Failed to compress image', { id: 'compress' });
      }
    }

    if (file.size > maxSize) {
      toast.error('Image size must be less than 10MB');
      return;
    }

    setSelectedImage(file);
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      toast.error('Please select an image first');
      return;
    }

    setAnalyzing(true);
    setResult(null);

    try {
      // Call REAL backend API
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await fetch(`${API_URL}/api/analyze-image`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      
      // Map backend response to frontend format
      const analysisResult: ImageAnalysisResult = {
        isFake: data.isFake,
        confidence: data.confidence,
        threatLevel: data.threatLevel,
        explanation: data.explanation,
        manipulationTypes: data.manipulationTypes || data.indicators || [],
        recommendation: data.recommendation,
        technicalDetails: {
          resolution: data.technicalDetails?.resolution || 'Unknown',
          format: data.technicalDetails?.format || selectedImage.type.split('/')[1].toUpperCase(),
          aiGenerated: data.technicalDetails?.aiGenerated || false,
          deepfakeScore: data.technicalDetails?.deepfakeScore || 0,
        },
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

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResult(null);
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
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center shadow-glow">
              <ImageIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Fake Image Detector</h1>
              <p className="text-slate-400">Detect AI-generated and manipulated images</p>
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-6"
          >
            {/* Upload Area */}
            <Card>
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-primary-400" />
                <h2 className="text-xl font-semibold">Upload Image</h2>
              </div>

              {!imagePreview ? (
                <div
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                    dragActive
                      ? 'border-primary-500 bg-primary-500/10'
                      : 'border-slate-700 hover:border-slate-600'
                  }`}
                >
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileInput}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="pointer-events-none">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500/20 to-purple-500/20 flex items-center justify-center mx-auto mb-4">
                      <Upload className="w-8 h-8 text-primary-400" />
                    </div>
                    <h3 className="text-lg font-semibold mb-2">
                      {dragActive ? 'Drop image here' : 'Drag & drop your image'}
                    </h3>
                    <p className="text-slate-400 text-sm mb-4">or click to browse</p>
                    <p className="text-xs text-slate-500">
                      Supports: JPG, PNG, WebP (Max 10MB)
                    </p>
                  </div>
                </div>
              ) : (
                <div className="relative">
                  <div className="w-full rounded-xl bg-slate-900/50 overflow-hidden" style={{ height: '400px' }}>
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-full h-full object-cover rounded-xl"
                      style={{ objectFit: 'contain' }}
                    />
                  </div>
                  <button
                    onClick={clearImage}
                    className="absolute top-2 right-2 p-2 bg-slate-900/90 hover:bg-slate-800 rounded-lg transition-colors backdrop-blur-sm"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              )}

              {selectedImage && !analyzing && !result && (
                <div className="mt-4 space-y-3">
                  <div className="text-sm text-slate-400 text-center">
                    {selectedImage.name} ({(selectedImage.size / 1024 / 1024).toFixed(2)} MB)
                  </div>
                  <Button 
                    onClick={handleAnalyze} 
                    icon={<Shield className="w-5 h-5" />}
                    className="w-full"
                  >
                    Analyze Image
                  </Button>
                </div>
              )}
            </Card>

            {/* Info Card */}
            <Card className="bg-primary-500/5 border-primary-500/20">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-primary-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold mb-2">Detection Capabilities:</h3>
                  <ul className="text-sm text-slate-400 space-y-1">
                    <li>• AI-generated images (DALL-E, Midjourney, Stable Diffusion)</li>
                    <li>• Deepfake detection</li>
                    <li>• Photo manipulation and editing</li>
                    <li>• Face swap and morphing</li>
                  </ul>
                </div>
              </div>
            </Card>
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
                  <Card className="h-full flex items-center justify-center min-h-[500px]">
                    <div className="text-center">
                      <LoadingSpinner size="lg" />
                      <p className="mt-4 text-slate-400">Analyzing image with AI...</p>
                      <p className="text-sm text-slate-500 mt-2">Running deepfake detection</p>
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
                  {/* Threat Level */}
                  <Card className={`${getThreatColor(result.threatLevel).bg} border-2 ${getThreatColor(result.threatLevel).border}`}>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        {result.isFake ? (
                          <AlertTriangle className={`w-8 h-8 ${getThreatColor(result.threatLevel).text}`} />
                        ) : (
                          <CheckCircle className="w-8 h-8 text-green-400" />
                        )}
                        <div>
                          <h3 className="text-xl font-bold">
                            {result.isFake ? 'Fake/Manipulated' : 'Appears Authentic'}
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
                          {result.isFake ? 'Manipulation Confidence' : 'Authenticity Confidence'}
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
                        <Info className="w-4 h-4 text-primary-400 flex-shrink-0 mt-0.5" />
                        <div className="text-sm">
                          <p className="font-semibold text-slate-300 mb-1">Trust Guidance:</p>
                          <p className="text-slate-400">
                            {result.confidence >= 75 ? (
                              result.isFake ? (
                                <span className="text-danger-400">⚠️ <strong>Very High Confidence</strong> - This image is very likely fake or manipulated. Do NOT trust it as authentic.</span>
                              ) : (
                                <span className="text-green-400">✅ <strong>Very High Confidence</strong> - This image appears very authentic, but always verify source and context.</span>
                              )
                            ) : result.confidence >= 55 ? (
                              result.isFake ? (
                                <span className="text-yellow-400">⚠️ <strong>High Confidence</strong> - Strong signs of manipulation. Verify through reverse image search.</span>
                              ) : (
                                <span className="text-green-400">✅ <strong>High Confidence</strong> - Image appears genuine, but verify origin and context.</span>
                              )
                            ) : result.confidence >= 35 ? (
                              <span className="text-yellow-400">⚡ <strong>Moderate Confidence</strong> - Some suspicious elements. Use reverse image search and verify source.</span>
                            ) : (
                              <span className="text-slate-400">ℹ️ <strong>Low Confidence</strong> - Inconclusive. Verify image source independently and check for prior usage online.</span>
                            )}
                          </p>
                        </div>
                      </div>
                    </div>
                  </Card>

                  {/* Technical Details */}
                  <Card>
                    <h3 className="font-semibold mb-3">Technical Analysis</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-sm text-slate-400">Resolution</div>
                        <div className="font-semibold">
                          {result.technicalDetails.resolution !== 'Unknown' 
                            ? result.technicalDetails.resolution 
                            : selectedImage ? `${Math.round(selectedImage.size / 1024)} KB` : 'Unknown'}
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-400">Format</div>
                        <div className="font-semibold">{result.technicalDetails.format}</div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-400">AI Generated</div>
                        <div className="font-semibold">
                          {result.technicalDetails.aiGenerated ? (
                            <span className="text-danger-400">Yes</span>
                          ) : (
                            <span className="text-green-400">No</span>
                          )}
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-400">Deepfake Score</div>
                        <div className="font-semibold">
                          {result.technicalDetails.deepfakeScore > 0 ? (
                            <span className={result.technicalDetails.deepfakeScore > 70 ? 'text-danger-400' : result.technicalDetails.deepfakeScore > 40 ? 'text-yellow-400' : 'text-green-400'}>
                              {result.technicalDetails.deepfakeScore}%
                            </span>
                          ) : (
                            <span className="text-green-400">0%</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </Card>

                  {/* Explanation */}
                  <Card>
                    <div className="flex items-center gap-2 mb-3">
                      <Eye className="w-5 h-5 text-primary-400" />
                      <h3 className="font-semibold">Analysis</h3>
                    </div>
                    <p className="text-slate-300">{result.explanation}</p>
                  </Card>

                  {/* Detection Details */}
                  {result.manipulationTypes && result.manipulationTypes.length > 0 && (
                    <Card>
                      <h3 className="font-semibold mb-3">Detection Details</h3>
                      <ul className="space-y-2">
                        {result.manipulationTypes.map((type, index) => (
                          <li key={index} className="flex items-start gap-2 text-slate-300">
                            <span className={`w-1.5 h-1.5 rounded-full ${result.isFake ? 'bg-danger-400' : 'bg-green-400'} mt-2 flex-shrink-0`} />
                            <span>{type}</span>
                          </li>
                        ))}
                      </ul>
                    </Card>
                  )}

                  {/* Recommendation */}
                  <Card className="bg-primary-500/10 border-primary-500/30">
                    <div className="flex items-center gap-2 mb-3">
                      <Shield className="w-5 h-5 text-primary-400" />
                      <h3 className="font-semibold">Recommendation</h3>
                    </div>
                    <p className="text-slate-300">{result.recommendation}</p>
                  </Card>

                  {/* Actions */}
                  <div className="flex gap-3">
                    <Button variant="secondary" className="flex-1" onClick={clearImage}>
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
                  <Card className="h-full flex items-center justify-center min-h-[500px]">
                    <div className="text-center max-w-sm">
                      <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500/20 to-purple-500/20 flex items-center justify-center mx-auto mb-4">
                        <ImageIcon className="w-10 h-10 text-primary-400" />
                      </div>
                      <h3 className="text-xl font-semibold mb-2">Ready to Analyze</h3>
                      <p className="text-slate-400">
                        Upload an image to detect AI-generated content and manipulation
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
