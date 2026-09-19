import React from 'react';
import { AlertCircle, ArrowRight } from 'lucide-react';
import { useTraffic } from '../context/TrafficContext';

const ExplainabilityPanel = ({ nodeId, delta }) => {
  const { intersections } = useTraffic();
  const node = intersections?.find(i => i.id === nodeId);

  if (!node) return null;

  const getReasoning = () => {
    const reasons = [];
    if (delta > 0) {
      if (node.density > 0.6) reasons.push("Queue density exceeds critical threshold");
      if (node.queue > 20) reasons.push("Wait time impacting overall network throughput");
      reasons.push("Downstream capacity available for clearance");
    } else if (delta < 0) {
      if (node.density < 0.4) reasons.push("Low utilization relative to crossing traffic");
      if (node.queue < 10) reasons.push("Reallocating unused capacity to congested nodes");
    } else {
      reasons.push("Current timing is optimal for observed load");
    }
    return reasons;
  };

  return (
    <div className="bg-elevated border border-cyan/30 rounded p-4 text-sm mt-4">
      <div className="flex items-center space-x-2 text-cyan font-mono mb-2">
        <AlertCircle className="w-4 h-4" />
        <span className="font-bold">OPTIMIZATION INTELLIGENCE</span>
      </div>
      
      <p className="text-primary mb-2">
        WHY DID THE SYSTEM CHANGE THIS SIGNAL?
      </p>
      
      <p className="text-secondary mb-3 font-mono">
        <span className="text-primary font-bold">{nodeId}</span> green time {delta > 0 ? 'increased' : 'decreased'} by {Math.abs(delta)}s because:
      </p>
      
      <ul className="space-y-1">
        {getReasoning().map((reason, idx) => (
          <li key={idx} className="flex items-start space-x-2 text-muted">
            <ArrowRight className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span>{reason}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ExplainabilityPanel;
