import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  Shield,
  Zap,
  Eye,
  Lock,
  TrendingUp,
  ArrowRight,
  Star,
  AlertTriangle,
  Brain,
  Sparkles,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { ThemeToggle } from '../components/ui/ThemeToggle';

export const Landing = () => {
  const features = [
    {
      icon: <Brain className="w-6 h-6" />,
      title: 'AI-Powered Detection',
      description: 'Advanced machine learning models analyze threats in real-time',
    },
    {
      icon: <Eye className="w-6 h-6" />,
      title: 'Deepfake Analysis',
      description: 'Detect manipulated images and videos with 99% accuracy',
    },
    {
      icon: <AlertTriangle className="w-6 h-6" />,
      title: 'Scam Text Scanner',
      description: 'Identify phishing attempts and fraudulent messages instantly',
    },
    {
      icon: <Lock className="w-6 h-6" />,
      title: 'Enterprise Security',
      description: 'Bank-grade encryption protects your data',
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Instant Results',
      description: 'Get threat analysis in under 2 seconds',
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Continuous Learning',
      description: 'Our AI improves daily with new threat patterns',
    },
  ];

  const stats = [
    { value: '10M+', label: 'Scams Detected' },
    { value: '99.8%', label: 'Accuracy Rate' },
    { value: '500K+', label: 'Protected Users' },
    { value: '<2s', label: 'Analysis Time' },
  ];

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Security Analyst',
      content: 'SentinelAI saved our company from a sophisticated phishing attack. The detection was instant and accurate.',
      rating: 5,
    },
    {
      name: 'Michael Rodriguez',
      role: 'Small Business Owner',
      content: 'I use SentinelAI daily to verify suspicious emails. It\'s like having a cybersecurity expert on call 24/7.',
      rating: 5,
    },
    {
      name: 'Emily Watson',
      role: 'Digital Marketer',
      content: 'The deepfake detection feature is incredible. It caught a fake video that could have damaged our brand.',
      rating: 5,
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navigation */}
      <nav className="fixed top-0 w-full glass border-b border-white/10 z-50">
        <div className="section-container">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyber-500 to-primary-500 flex items-center justify-center shadow-glow">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">SentinelAI</span>
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <Link to="/login">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link to="/signup">
                <Button variant="primary" size="sm">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-cyber-grid opacity-30" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyber-500/5 to-transparent" />
        
        <div className="section-container relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring' }}
              className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-6"
            >
              <Sparkles className="w-4 h-4 text-cyber-400" />
              <span className="text-sm text-slate-300">Powered by Advanced AI</span>
            </motion.div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Detect AI scams
              <br />
              <span className="gradient-text">before they destroy trust</span>
            </h1>

            <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
              SentinelAI uses cutting-edge artificial intelligence to protect you from
              deepfakes, phishing, and sophisticated scams in real-time.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/signup">
                <Button variant="primary" size="lg" icon={<ArrowRight className="w-5 h-5" />}>
                  Start Free Trial
                </Button>
              </Link>
              <Button variant="secondary" size="lg">
                Watch Demo
              </Button>
            </div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-20"
            >
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">
                    {stat.value}
                  </div>
                  <div className="text-sm text-slate-400">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 relative">
        <div className="section-container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Enterprise-grade <span className="gradient-text">protection</span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Comprehensive security features designed for the modern threat landscape
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card-hover group"
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-500/20 to-primary-500/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <div className="text-cyber-400">{feature.icon}</div>
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 relative">
        <div className="section-container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Trusted by <span className="gradient-text">security professionals</span>
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card"
              >
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-cyber-400 text-cyber-400" />
                  ))}
                </div>
                <p className="text-slate-300 mb-4">{testimonial.content}</p>
                <div>
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-sm text-slate-400">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative">
        <div className="section-container">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="glass rounded-3xl p-12 text-center relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyber-500/10 to-primary-500/10" />
            <div className="relative z-10">
              <h2 className="text-4xl md:text-5xl font-bold mb-4">
                Ready to protect yourself?
              </h2>
              <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
                Join thousands of users who trust SentinelAI to keep them safe from AI-powered threats
              </p>
              <Link to="/signup">
                <Button variant="primary" size="lg" icon={<ArrowRight className="w-5 h-5" />}>
                  Start Free Trial
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/10">
        <div className="section-container">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyber-500 to-primary-500 flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold gradient-text">SentinelAI</span>
            </div>
            <div className="text-sm text-slate-400">
              © 2026 SentinelAI. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};
