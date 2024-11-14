import React, { useMemo } from 'react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, Legend, ZAxis } from 'recharts';

interface AnomalyDetectionProps {
  data: any[];
}

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-2 border rounded shadow">
        <p className="font-semibold">{`State: ${payload[0].payload.state}`}</p>
        <p>{`Source Load: ${payload[0].value.toFixed(2)}`}</p>
        <p>{`Destination Load: ${payload[1].value.toFixed(2)}`}</p>
      </div>
    );
  }
  return null;
};

const AnomalyDetection: React.FC<AnomalyDetectionProps> = ({ data }) => {
  const scatterData = useMemo(() => {
    return data
      .filter(item => item && typeof item === 'object')
      .map(item => ({
        sload: parseFloat(item.sload) || 0,
        dload: parseFloat(item.dload) || 0,
        state: item.state || 'unknown'
      }))
      .filter(item => 
        !isNaN(item.sload) && 
        !isNaN(item.dload) && 
        item.sload < 1000 && // Filter out extreme outliers
        item.dload < 1000
      );
  }, [data]);

  if (scatterData.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4">Load Pattern Analysis</h3>
        <p className="text-gray-600">No valid data available for visualization</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-4">Load Pattern Analysis</h3>
      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <XAxis 
              type="number" 
              dataKey="sload" 
              name="Source Load"
              label={{ value: 'Source Load (bytes/s)', position: 'bottom' }}
              domain={['auto', 'auto']}
            />
            <YAxis 
              type="number" 
              dataKey="dload" 
              name="Destination Load"
              label={{ value: 'Destination Load (bytes/s)', angle: -90, position: 'left' }}
              domain={['auto', 'auto']}
            />
            <ZAxis range={[50, 50]} />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              verticalAlign="top" // Position legend at the top
              align="center"
              wrapperStyle={{ paddingBottom: 10 }}
            />
            <Scatter 
              name="Network Load Distribution" 
              data={scatterData} 
              fill="#8884d8"
              opacity={0.6}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-sm text-gray-600">
        <p>This scatter plot visualizes the relationship between source and destination loads.</p>
        <p>Clusters indicate normal behavior, while isolated points may represent anomalies.</p>
      </div>
    </div>
  );
};

export default AnomalyDetection;
