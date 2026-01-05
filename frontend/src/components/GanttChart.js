import React from 'react';
import { generateColor } from '../utils/api';

const GanttChart = ({ ganttData }) => {
  if (!ganttData || ganttData.length === 0) {
    return null;
  }

  // Calculate total time
  const maxTime = Math.max(...ganttData.map(block => block.end));
  
  // Get unique process IDs and assign colors
  const processIds = [...new Set(ganttData.map(block => block.pid))];
  const colorMap = {};
  processIds.forEach((pid, index) => {
    colorMap[pid] = generateColor(index);
  });

  // Calculate time labels
  const timePoints = [0];
  ganttData.forEach(block => {
    if (!timePoints.includes(block.end)) {
      timePoints.push(block.end);
    }
  });
  timePoints.sort((a, b) => a - b);

  return (
    <div className="gantt-chart">
      <h3>Gantt Chart</h3>
      
      <div className="gantt-timeline">
        {ganttData.map((block, index) => {
          const width = ((block.end - block.start) / maxTime) * 100;
          return (
            <div
              key={index}
              className="gantt-block"
              style={{
                width: `${width}%`,
                backgroundColor: colorMap[block.pid],
                minWidth: '60px',
              }}
              title={`P${block.pid}: ${block.start} - ${block.end}`}
            >
              <span>P{block.pid}</span>
              <small style={{ fontSize: '0.75em', marginTop: '4px' }}>
                {block.end - block.start}
              </small>
            </div>
          );
        })}
      </div>
      
      <div className="gantt-labels" style={{ marginTop: '10px' }}>
        {timePoints.map((time, index) => (
          <div
            key={index}
            style={{
              width: index < timePoints.length - 1 
                ? `${((timePoints[index + 1] - time) / maxTime) * 100}%`
                : '0%',
              position: 'relative',
              minWidth: index === 0 ? '20px' : '0',
            }}
          >
            <span style={{ position: 'absolute', left: '-5px', fontWeight: '600' }}>
              {time}
            </span>
          </div>
        ))}
        <span style={{ fontWeight: '600' }}>{maxTime}</span>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h4 style={{ marginBottom: '10px', color: '#555' }}>Process Legend</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
          {processIds.map(pid => (
            <div key={pid} style={{ display: 'flex', alignItems: 'center' }}>
              <div
                style={{
                  width: '20px',
                  height: '20px',
                  backgroundColor: colorMap[pid],
                  marginRight: '8px',
                  borderRadius: '4px',
                }}
              />
              <span style={{ fontWeight: '500' }}>Process {pid}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GanttChart;
