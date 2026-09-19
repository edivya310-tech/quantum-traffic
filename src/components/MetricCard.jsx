import React, { useEffect, useState } from 'react';
import { cn } from '../utils/format';

export const useCountUp = (value, duration = 1000) => {
  const [current, setCurrent] = useState(value);

  useEffect(() => {
    let startTimestamp = null;
    const startValue = current;
    const endValue = value;
    if (startValue === endValue) return;

    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      
      setCurrent(Math.floor(progress * (endValue - startValue) + startValue));
      
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        setCurrent(endValue);
      }
    };
    
    window.requestAnimationFrame(step);
  }, [value, duration]); // Intentionally omitting current

  return current;
};

const MetricCard = ({ label, value, unit, icon: Icon, trend, inverse = false, highlight = false }) => {
  const animatedValue = useCountUp(typeof value === 'number' ? value : 0);
  const displayValue = typeof value === 'number' ? animatedValue : value;

  // Determine trend color
  let trendColor = 'text-muted';
  if (trend) {
    if (trend < 0) trendColor = inverse ? 'text-go' : 'text-stop';
    if (trend > 0) trendColor = inverse ? 'text-stop' : 'text-go';
  }

  return (
    <div className={cn(
      "bg-panel border rounded p-4 flex flex-col justify-between transition-colors duration-150",
      highlight ? "border-cyan/50 bg-cyan/5" : "border-border-subtle"
    )}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-[11px] uppercase tracking-[0.15em] text-muted font-semibold">{label}</span>
        {Icon && <Icon className="w-4 h-4 text-secondary" />}
      </div>
      <div className="flex items-baseline space-x-1">
        <span className="text-3xl font-bold font-mono text-primary">
          {displayValue}
        </span>
        {unit && <span className="text-sm font-mono text-muted">{unit}</span>}
      </div>
      
      {trend !== undefined && (
        <div className="mt-2 text-xs font-mono flex items-center space-x-1">
          <span className={trendColor}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
          <span className="text-muted">vs baseline</span>
        </div>
      )}
    </div>
  );
};

export default MetricCard;
