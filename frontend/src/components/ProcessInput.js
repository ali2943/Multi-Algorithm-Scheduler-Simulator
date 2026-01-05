import React, { useState } from 'react';
import { validateProcess } from '../utils/api';

const ProcessInput = ({ processes, setProcesses }) => {
  const [newProcess, setNewProcess] = useState({
    pid: processes.length + 1,
    arrivalTime: 0,
    burstTime: 1,
    priority: 0,
    queueLevel: 0,
  });
  
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProcess({
      ...newProcess,
      [name]: parseInt(value) || 0,
    });
  };

  const addProcess = () => {
    const errors = validateProcess(newProcess);
    if (errors.length > 0) {
      setError(errors.join(', '));
      return;
    }
    
    // Check for duplicate PID
    if (processes.some(p => p.pid === newProcess.pid)) {
      setError('Process ID already exists');
      return;
    }
    
    setError('');
    setProcesses([...processes, { ...newProcess }]);
    setNewProcess({
      pid: newProcess.pid + 1,
      arrivalTime: 0,
      burstTime: 1,
      priority: 0,
      queueLevel: 0,
    });
  };

  const removeProcess = (pid) => {
    setProcesses(processes.filter(p => p.pid !== pid));
  };

  const clearAll = () => {
    setProcesses([]);
    setNewProcess({
      pid: 1,
      arrivalTime: 0,
      burstTime: 1,
      priority: 0,
      queueLevel: 0,
    });
  };

  return (
    <div className="process-input">
      <h2>Process Input</h2>
      
      {error && <div className="error">{error}</div>}
      
      <div className="process-form">
        <div className="form-group">
          <label>Process ID</label>
          <input
            type="number"
            name="pid"
            value={newProcess.pid}
            onChange={handleInputChange}
            min="1"
          />
        </div>
        
        <div className="form-group">
          <label>Arrival Time</label>
          <input
            type="number"
            name="arrivalTime"
            value={newProcess.arrivalTime}
            onChange={handleInputChange}
            min="0"
          />
        </div>
        
        <div className="form-group">
          <label>Burst Time</label>
          <input
            type="number"
            name="burstTime"
            value={newProcess.burstTime}
            onChange={handleInputChange}
            min="1"
          />
        </div>
        
        <div className="form-group">
          <label>Priority</label>
          <input
            type="number"
            name="priority"
            value={newProcess.priority}
            onChange={handleInputChange}
            min="0"
          />
        </div>
        
        <div className="form-group">
          <label>Queue Level</label>
          <input
            type="number"
            name="queueLevel"
            value={newProcess.queueLevel}
            onChange={handleInputChange}
            min="0"
          />
        </div>
      </div>
      
      <div className="button-group">
        <button className="btn-success" onClick={addProcess}>
          Add Process
        </button>
        <button className="btn-danger" onClick={clearAll}>
          Clear All
        </button>
      </div>

      {processes.length > 0 && (
        <div className="process-table">
          <table>
            <thead>
              <tr>
                <th>PID</th>
                <th>Arrival Time</th>
                <th>Burst Time</th>
                <th>Priority</th>
                <th>Queue Level</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {processes.map((process) => (
                <tr key={process.pid}>
                  <td>P{process.pid}</td>
                  <td>{process.arrivalTime}</td>
                  <td>{process.burstTime}</td>
                  <td>{process.priority}</td>
                  <td>{process.queueLevel}</td>
                  <td>
                    <button
                      className="btn-danger"
                      onClick={() => removeProcess(process.pid)}
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ProcessInput;
