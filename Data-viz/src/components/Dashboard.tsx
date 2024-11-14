import React from 'react';
import NetworkMetrics from './NetworkMetrics';
import TrafficAnalysis from './TrafficAnalysis';
import ProtocolDistribution from './ProtocolDistribution';
import AnomalyDetection from './AnomalyDetection';

interface DashboardProps {
  data: any[];
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  if (!data.length) return null;

  return (
    <div className="space-y-6">
      <NetworkMetrics data={data} />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TrafficAnalysis data={data} />
        <ProtocolDistribution data={data} />
      </div>
      <AnomalyDetection data={data} />
    </div>
  );
};

export default Dashboard;