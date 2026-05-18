import { motion } from 'framer-motion';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <motion.button
      onClick={toggleTheme}
      className="relative w-14 h-7 rounded-full glass border border-white/10 dark:border-white/10 light:border-slate-300 transition-all duration-300 hover:shadow-glow"
      whileTap={{ scale: 0.95 }}
    >
      {/* Background gradient */}
      <div className={`absolute inset-0 rounded-full transition-all duration-300 ${
        theme === 'dark' 
          ? 'bg-gradient-to-r from-accent-blue to-accent-purple' 
          : 'bg-gradient-to-r from-accent-blue-light to-accent-purple-light'
      }`} />
      
      {/* Slider */}
      <motion.div
        className="absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-lg flex items-center justify-center"
        animate={{
          left: theme === 'dark' ? '2px' : 'calc(100% - 26px)',
        }}
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      >
        {theme === 'dark' ? (
          <Moon className="w-4 h-4 text-accent-blue" />
        ) : (
          <Sun className="w-4 h-4 text-accent-blue-light" />
        )}
      </motion.div>
    </motion.button>
  );
};
