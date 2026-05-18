import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

interface ConfidenceTrendChartProps {
  data: Array<{
    date: string;
    avgConfidence: number;
    detectionRate: number;
  }>;
}

export const ConfidenceTrendChart = ({ data }: ConfidenceTrendChartProps) => {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass rounded-lg p-3 border border-slate-700/50">
          <p className="text-sm text-slate-400 mb-2">{label}</p>
          <div className="space-y-1">
            <p className="text-sm">
              <span className="text-primary-400 font-semibold">Avg Confidence:</span>{' '}
              <span className="text-slate-200">{payload[0].value}%</span>
            </p>
            <p className="text-sm">
              <span className="text-green-400 font-semibold">Detection Rate:</span>{' '}
              <span className="text-slate-200">{payload[1].value}%</span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
          <XAxis
            dataKey="date"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
            domain={[0, 100]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="top"
            height={36}
            iconType="line"
            formatter={(value) => (
              <span className="text-slate-300 text-sm">{value}</span>
            )}
          />
          <Line
            type="monotone"
            dataKey="avgConfidence"
            name="Avg Confidence"
            stroke="#8b5cf6"
            strokeWidth={3}
            dot={{ fill: '#8b5cf6', r: 4 }}
            activeDot={{ r: 6 }}
            animationDuration={1000}
          />
          <Line
            type="monotone"
            dataKey="detectionRate"
            name="Detection Rate"
            stroke="#10b981"
            strokeWidth={3}
            dot={{ fill: '#10b981', r: 4 }}
            activeDot={{ r: 6 }}
            animationDuration={1000}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
};
