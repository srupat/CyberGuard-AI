import React, { useMemo, useState } from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface ProtocolDistributionProps {
  data: any[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const ProtocolDistribution: React.FC<ProtocolDistributionProps> = ({ data }) => {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const protocolData = useMemo(() => {
    const protocols = data.reduce((acc: Record<string, number>, curr) => {
      const proto = curr.proto || 'unknown';
      acc[proto] = (acc[proto] || 0) + 1;
      return acc;
    }, {});

    return Object.entries(protocols)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 6); // Show top 6 protocols
  }, [data]);

  // Handler to update selectedIndex when a pie segment is clicked
  const handleClick = (index: number) => {
    setSelectedIndex(selectedIndex === index ? null : index); // Deselect if the same segment is clicked again
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-4">Protocol Distribution</h3>
      <div className="h-[300px]">
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={protocolData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
              onClick={(data, index) => handleClick(index)} // Bind click event to handleClick
            >
              {protocolData.map((_, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                  opacity={selectedIndex === null || selectedIndex === index ? 1 : 0.3} // Adjust opacity
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ProtocolDistribution;
