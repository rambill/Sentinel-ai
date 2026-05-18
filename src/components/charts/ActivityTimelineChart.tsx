import { motion } from 'framer-motion';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface ActivityTimelineChartProps {
  data: Array<{
    hour: string;
    activity: number;
  }>;
}

export const ActivityTimelineChart = ({ data }: ActivityTimelineChartProps) => {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass rounded-lg p-3 border border-slate-700/50">
          <p className="text-sm text-slate-400 mb-1">{label}</p>
          <p className="text-lg font-bold text-cyber-400">
            {payload[0].value} scans
          </p>
        </div>
      );
    }
    return null;
  };

  // Color bars based on activity level
  const getColor = (value: number) => {
    if (value > 15) return '#06b6d4'; // High activity - cyan
    if (value > 8) return '#8b5cf6'; // Medium activity - purple
    return '#64748b'; // Low activity - slate
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
          <XAxis
            dataKey="hour"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar
            dataKey="activity"
            radius={[8, 8, 0, 0]}
            animationDuration={1000}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.activity)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  );
};
