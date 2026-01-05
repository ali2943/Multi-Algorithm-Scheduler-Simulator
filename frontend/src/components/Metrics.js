import React from 'react';

const Metrics = ({ metrics }) => {
  if (!metrics) {
    return null;
  }

  return (
    <div className="metrics">
      <div className="metric-card">
        <h3>Average Waiting Time</h3>
        <div className="value">{metrics.avg_waiting_time}</div>
        <small>time units</small>
      </div>
      
      <div className="metric-card">
        <h3>Average Turnaround Time</h3>
        <div className="value">{metrics.avg_turnaround_time}</div>
        <small>time units</small>
      </div>
      
      <div className="metric-card">
        <h3>CPU Utilization</h3>
        <div className="value">{metrics.cpu_utilization}%</div>
        <small>efficiency</small>
      </div>
      
      <div className="metric-card">
        <h3>Total Processes</h3>
        <div className="value">{metrics.total_processes}</div>
        <small>processes</small>
      </div>
    </div>
  );
};

export default Metrics;
