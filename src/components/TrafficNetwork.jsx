import React, { useMemo } from 'react';
import { useTraffic } from '../context/TrafficContext';
import { cn } from '../utils/format';

// Fixed layout grid for 8 nodes
const GRID_LAYOUT = {
  I1: { x: 20, y: 20 },
  I2: { x: 50, y: 20 },
  I3: { x: 80, y: 20 },
  I4: { x: 20, y: 50 },
  I5: { x: 50, y: 50 },
  I6: { x: 80, y: 50 },
  I7: { x: 50, y: 80 },
  I8: { x: 80, y: 80 },
};

const EDGES = [
  ['I1', 'I2'], ['I2', 'I3'],
  ['I1', 'I4'], ['I2', 'I5'], ['I3', 'I6'],
  ['I4', 'I5'], ['I5', 'I6'],
  ['I5', 'I7'], ['I6', 'I8'],
  ['I7', 'I8']
];

const getDensityColor = (density) => {
  if (density < 0.4) return 'text-go';
  if (density < 0.7) return 'text-warn';
  return 'text-stop';
};

const getSignalColor = (signal) => {
  if (signal === 'GREEN') return 'bg-go';
  if (signal === 'YELLOW') return 'bg-warn';
  return 'bg-stop';
};

const TrafficNetwork = ({ selectedNodeId, onNodeClick, compact = false }) => {
  const { intersections, emergency } = useTraffic();

  const edgeElements = useMemo(() => {
    return EDGES.map(([a, b]) => {
      const posA = GRID_LAYOUT[a];
      const posB = GRID_LAYOUT[b];
      
      const isEmergencyRoute = emergency?.active && emergency.route.includes(a) && emergency.route.includes(b);
      // Rough heuristic: if they are adjacent in route
      const idxA = emergency?.route?.indexOf(a);
      const idxB = emergency?.route?.indexOf(b);
      const isActuallyRoute = isEmergencyRoute && Math.abs(idxA - idxB) === 1;

      return (
        <g key={`${a}-${b}`}>
          {/* Base road */}
          <line
            x1={`${posA.x}%`} y1={`${posA.y}%`}
            x2={`${posB.x}%`} y2={`${posB.y}%`}
            className="stroke-border-subtle"
            strokeWidth={compact ? 4 : 8}
          />
          {/* Flow animation line */}
          <line
            x1={`${posA.x}%`} y1={`${posA.y}%`}
            x2={`${posB.x}%`} y2={`${posB.y}%`}
            className={cn(
              "stroke-cyan opacity-40",
              isActuallyRoute ? "stroke-warn opacity-100 animate-pulse" : ""
            )}
            strokeWidth={compact ? 2 : 4}
            strokeDasharray="4 8"
            style={{ animationDuration: '3s', animationTimingFunction: 'linear' }}
          >
             <animate attributeName="stroke-dashoffset" from="24" to="0" dur="2s" repeatCount="indefinite" />
          </line>
        </g>
      );
    });
  }, [emergency, compact]);

  if (!intersections || intersections.length === 0) return <div className="h-full flex items-center justify-center text-muted font-mono">LOADING NETWORK...</div>;

  return (
    <div className="relative w-full aspect-square md:aspect-video bg-panel rounded-lg border border-border-subtle overflow-hidden">
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        {edgeElements}
      </svg>
      
      {intersections.map(node => {
        const pos = GRID_LAYOUT[node.id];
        const isSelected = selectedNodeId === node.id;
        const isEmergency = emergency?.active && emergency.route.includes(node.id);

        return (
          <div
            key={node.id}
            onClick={() => onNodeClick && onNodeClick(node.id)}
            className={cn(
              "absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-150 rounded flex items-center justify-center font-mono",
              compact ? "w-8 h-8 text-[10px]" : "w-14 h-14 text-sm",
              isSelected ? "border-2 border-cyan bg-elevated shadow-[0_0_15px_rgba(34,211,238,0.2)]" : "border border-border-strong bg-base hover:border-cyan/50",
              isEmergency ? "border-warn shadow-[0_0_15px_rgba(234,179,8,0.3)]" : ""
            )}
            style={{ left: `${pos.x}%`, top: `${pos.y}%` }}
          >
            {/* Signal dot */}
            <div className={cn(
              "absolute -top-1 -right-1 rounded-full border border-base",
              compact ? "w-2 h-2" : "w-3 h-3",
              getSignalColor(node.signal)
            )} />
            
            <span className={cn(
              "font-bold",
              getDensityColor(node.density)
            )}>
              {node.id}
            </span>
            
            {!compact && (
              <div className="absolute -bottom-5 left-1/2 transform -translate-x-1/2 text-[10px] text-muted whitespace-nowrap">
                {Math.round(node.density * 100)}%
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default TrafficNetwork;
