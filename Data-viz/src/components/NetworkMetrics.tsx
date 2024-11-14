import React, { useMemo } from 'react';
import { Network, Activity, Zap, Timer } from 'lucide-react';

interface NetworkMetricsProps {
  data: any[];
}

const NetworkMetrics: React.FC<NetworkMetricsProps> = ({ data }) => {
  const metrics = useMemo(() => {
    const validData = data.filter(item => item && typeof item === 'object');
    
    const totalBytes = validData.reduce((acc, curr) => {
      const sbytes = parseFloat(curr.sbytes) || 0;
      const dbytes = parseFloat(curr.dbytes) || 0;
      return acc + sbytes + dbytes;
    }, 0);

    const validRates = validData
      .map(item => parseFloat(item.rate))
      .filter(rate => !isNaN(rate));
    const avgRate = validRates.length > 0 
      ? validRates.reduce((acc, curr) => acc + curr, 0) / validRates.length 
      : 0;

    const validLatencies = validData
      .map(item => parseFloat(item.tcprtt))
      .filter(latency => !isNaN(latency));
    const avgLatency = validLatencies.length > 0
      ? validLatencies.reduce((acc, curr) => acc + curr, 0) / validLatencies.length
      : 0;

    const uniqueServices = new Set(
      validData
        .map(item => item.service)
        .filter(service => service && service !== '')
    ).size;

    return {
      totalTraffic: (totalBytes / (1024 * 1024)).toFixed(2), // Convert to MB
      averageRate: avgRate.toFixed(2),
      averageLatency: avgLatency.toFixed(2),
      uniqueServices: uniqueServices || 0,
    };
  }, [data]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard
        title="Total Traffic"
        value={`${metrics.totalTraffic} MB`}
        icon={<Network className="w-6 h-6 text-blue-500" />}
        color="blue"
      />
      <MetricCard
        title="Avg. Transfer Rate"
        value={`${metrics.averageRate} pkts/s`}
        icon={<Activity className="w-6 h-6 text-green-500" />}
        color="green"
      />
      <MetricCard
        title="Avg. Latency"
        value={`${metrics.averageLatency} ms`}
        icon={<Timer className="w-6 h-6 text-yellow-500" />}
        color="yellow"
      />
      <MetricCard
        title="Unique Services"
        value={metrics.uniqueServices}
        icon={<Zap className="w-6 h-6 text-purple-500" />}
        color="purple"
      />
    </div>
  );
};

const MetricCard = ({ title, value, icon, color }: { title: string; value: any; icon: React.ReactNode; color: string }) => (
  <div className={`bg-white p-6 rounded-lg shadow-lg border-l-4 border-${color}-500`}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
      </div>
      {icon}
    </div>
  </div>
);

export default NetworkMetrics;