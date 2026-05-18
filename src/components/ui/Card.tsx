import type { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export const Card = ({ children, className = '', hover = false, onClick }: CardProps) => {
  const Component = onClick ? motion.div : 'div';
  
  return (
    <Component
      className={`card ${hover ? 'card-hover' : ''} ${className}`}
      onClick={onClick}
      {...(onClick && {
        whileHover: { scale: 1.02, y: -4 },
        whileTap: { scale: 0.98 },
      })}
    >
      {children}
    </Component>
  );
};
