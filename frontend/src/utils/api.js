// Utility functions for scheduler simulator

export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * Simulate scheduling algorithm
 */
export const simulateScheduling = async (algorithm, processes, options = {}) => {
  try {
    const response = await fetch(`${API_URL}/api/simulate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        algorithm,
        processes,
        timeQuantum: options.timeQuantum || 2,
        preemptive: options.preemptive || false,
        timeQuantums: options.timeQuantums || [2, 4, 8],
      }),
    });

    if (!response.ok) {
      throw new Error('Simulation failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Error simulating scheduling:', error);
    throw error;
  }
};

/**
 * Get list of available algorithms
 */
export const getAlgorithms = async () => {
  try {
    const response = await fetch(`${API_URL}/api/algorithms`);
    if (!response.ok) {
      throw new Error('Failed to fetch algorithms');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching algorithms:', error);
    return [
      { id: 'fcfs', name: 'First Come First Serve', abbr: 'FCFS' },
      { id: 'sjf', name: 'Shortest Job First', abbr: 'SJF' },
      { id: 'srtf', name: 'Shortest Remaining Time First', abbr: 'SRTF' },
      { id: 'rr', name: 'Round Robin', abbr: 'RR' },
      { id: 'priority', name: 'Priority Scheduling', abbr: 'Priority' },
      { id: 'mlq', name: 'Multi-Level Queue', abbr: 'MLQ' },
      { id: 'mlfq', name: 'Multi-Level Feedback Queue', abbr: 'MLFQ' },
    ];
  }
};

/**
 * Generate random color for process
 */
export const generateColor = (index) => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788'
  ];
  return colors[index % colors.length];
};

/**
 * Validate process data
 */
export const validateProcess = (process) => {
  const errors = [];
  
  if (!process.pid || process.pid < 1) {
    errors.push('Process ID must be a positive number');
  }
  
  if (process.arrivalTime < 0) {
    errors.push('Arrival time cannot be negative');
  }
  
  if (!process.burstTime || process.burstTime < 1) {
    errors.push('Burst time must be at least 1');
  }
  
  if (process.priority < 0) {
    errors.push('Priority cannot be negative');
  }
  
  if (process.queueLevel < 0) {
    errors.push('Queue level cannot be negative');
  }
  
  return errors;
};

/**
 * Get sample processes
 */
export const getSampleProcesses = () => {
  return [
    { pid: 1, arrivalTime: 0, burstTime: 5, priority: 2, queueLevel: 0 },
    { pid: 2, arrivalTime: 1, burstTime: 3, priority: 1, queueLevel: 0 },
    { pid: 3, arrivalTime: 2, burstTime: 8, priority: 3, queueLevel: 1 },
    { pid: 4, arrivalTime: 3, burstTime: 6, priority: 2, queueLevel: 0 },
  ];
};
