import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

interface TrafficAnalysisProps {
  data: any[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-2 border rounded shadow">
        <p className="font-semibold">{`Flow #${label}`}</p>
        {payload.map((pld: any) => (
          <p key={pld.name} style={{ color: pld.color }}>
            {`${pld.name}: ${pld.value.toFixed(2)}`}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const TrafficAnalysis: React.FC<TrafficAnalysisProps> = ({ data }) => {
  const chartData = data
    .filter(item => item && typeof item === 'object')
    .slice(0, 100)
    .map((item, index) => ({
      id: index,
      sourcePackets: parseFloat(item.spkts) || 0,
      destPackets: parseFloat(item.dpkts) || 0,
      sourceBytes: parseFloat(item.sbytes) || 0,
      destBytes: parseFloat(item.dbytes) || 0,
    }))
    .filter(item =>
      !isNaN(item.sourcePackets) &&
      !isNaN(item.destPackets) &&
      !isNaN(item.sourceBytes) &&
      !isNaN(item.destBytes)
    );

  if (chartData.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4">Traffic Flow Analysis</h3>
        <p className="text-gray-600">No valid data available for visualization</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-4">Traffic Flow Analysis</h3>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis
              dataKey="dur"
              label={{ value: 'Duration (s)', position: 'bottom' }}
            />
            <YAxis label={{ value: 'Packets', angle: -90, position: 'insideLeft' }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend verticalAlign="top" height={36} />
            <Line
              type="monotone"
              dataKey="sourcePackets"
              stroke="#8884d8"
              name="Source Packets"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="destPackets"
              stroke="#82ca9d"
              name="Destination Packets"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TrafficAnalysis;