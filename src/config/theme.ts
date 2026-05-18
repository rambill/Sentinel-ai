/**
 * Premium Dual-Theme Configuration for SentinelAI
 * 
 * Dark Mode: "Midnight Intelligence"
 * Light Mode: "Clean Intelligence"
 */

export const themes = {
  dark: {
    name: 'Midnight Intelligence',
    colors: {
      // Backgrounds
      primaryBg: '#0B1120',
      secondaryBg: '#111827',
      cardBg: 'rgba(17, 24, 39, 0.75)',
      glassBorder: 'rgba(255, 255, 255, 0.08)',
      
      // Accents
      accentPrimary: '#3B82F6',
      accentSecondary: '#8B5CF6',
      success: '#10B981',
      danger: '#EF4444',
      
      // Text
      textPrimary: '#F9FAFB',
      textSecondary: '#9CA3AF',
      
      // Borders
      border: '#1F2937',
      
      // Gradients
      bgGradient: 'linear-gradient(135deg, #0B1120 0%, #111827 40%, #1E1B4B 100%)',
      buttonGradient: 'linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%)',
    },
  },
  light: {
    name: 'Clean Intelligence',
    colors: {
      // Backgrounds
      primaryBg: '#F8FAFC',
      secondaryBg: '#FFFFFF',
      cardBg: 'rgba(255, 255, 255, 0.8)',
      glassBorder: '#E2E8F0',
      
      // Accents
      accentPrimary: '#2563EB',
      accentSecondary: '#7C3AED',
      success: '#10B981',
      danger: '#EF4444',
      
      // Text
      textPrimary: '#0F172A',
      textSecondary: '#64748B',
      
      // Borders
      border: '#E2E8F0',
      
      // Gradients
      bgGradient: 'linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 50%, #FFFFFF 100%)',
      buttonGradient: 'linear-gradient(90deg, #2563EB 0%, #7C3AED 100%)',
    },
  },
};

export type Theme = 'dark' | 'light';
export type ThemeConfig = typeof themes.dark;
