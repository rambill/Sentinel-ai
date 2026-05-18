import { motion } from 'framer-motion';

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string;
  height?: string;
  animation?: boolean;
}

export const Skeleton = ({
  className = '',
  variant = 'rectangular',
  width,
  height,
  animation = true,
}: SkeletonProps) => {
  const baseClasses = 'bg-slate-800/50 animate-pulse';
  
  const variantClasses = {
    text: 'rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-lg',
  };

  const style = {
    width: width || '100%',
    height: height || (variant === 'text' ? '1em' : '100%'),
  };

  if (animation) {
    return (
      <motion.div
        initial={{ opacity: 0.5 }}
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        className={`${baseClasses} ${variantClasses[variant]} ${className}`}
        style={style}
      />
    );
  }

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={style}
    />
  );
};

// Skeleton Card
export const SkeletonCard = () => (
  <div className="glass rounded-xl p-6 space-y-4">
    <div className="flex items-center justify-between">
      <Skeleton variant="circular" width="48px" height="48px" />
      <Skeleton variant="text" width="60px" height="20px" />
    </div>
    <Skeleton variant="text" width="80px" height="32px" />
    <Skeleton variant="text" width="120px" height="16px" />
  </div>
);

// Skeleton Chart
export const SkeletonChart = () => (
  <div className="glass rounded-xl p-6">
    <Skeleton variant="text" width="150px" height="24px" className="mb-6" />
    <div className="h-[300px] flex items-end justify-between gap-2">
      {[...Array(8)].map((_, i) => (
        <Skeleton
          key={i}
          variant="rectangular"
          width="100%"
          height={`${Math.random() * 60 + 40}%`}
        />
      ))}
    </div>
  </div>
);

// Skeleton Table Row
export const SkeletonTableRow = () => (
  <div className="glass rounded-lg p-4 flex items-center gap-4">
    <Skeleton variant="circular" width="40px" height="40px" />
    <div className="flex-1 space-y-2">
      <Skeleton variant="text" width="60%" height="16px" />
      <Skeleton variant="text" width="40%" height="14px" />
    </div>
    <Skeleton variant="rectangular" width="80px" height="32px" />
  </div>
);

// Skeleton Dashboard
export const SkeletonDashboard = () => (
  <div className="space-y-8">
    {/* Header */}
    <div className="space-y-2">
      <Skeleton variant="text" width="300px" height="36px" />
      <Skeleton variant="text" width="200px" height="20px" />
    </div>

    {/* Stats Grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>

    {/* Charts */}
    <div className="grid lg:grid-cols-2 gap-6">
      <SkeletonChart />
      <SkeletonChart />
    </div>

    {/* Recent Activity */}
    <div className="space-y-4">
      <Skeleton variant="text" width="200px" height="24px" />
      {[...Array(3)].map((_, i) => (
        <SkeletonTableRow key={i} />
      ))}
    </div>
  </div>
);
