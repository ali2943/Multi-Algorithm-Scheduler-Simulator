import React, { useState, useEffect } from 'react';
import './styles/App.css';
import ProcessInput from './components/ProcessInput';
import GanttChart from './components/GanttChart';
import Metrics from './components/Metrics';
import { simulateScheduling, getAlgorithms, getSampleProcesses } from './utils/api';

function App() {
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('fcfs');
  const [processes, setProcesses] = useState([]);
  const [timeQuantum, setTimeQuantum] = useState(2);
  const [preemptive, setPreemptive] = useState(false);
  const [timeQuantums, setTimeQuantums] = useState('2,4,8');
  const [ganttChart, setGanttChart] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Load algorithms
    getAlgorithms().then(algs => {
      setAlgorithms(algs);
    });
  }, []);

  const loadSampleData = () => {
    setProcesses(getSampleProcesses());
    setError('');
  };

  const runSimulation = async () => {
    if (processes.length === 0) {
      setError('Please add at least one process');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const tqs = timeQuantums.split(',').map(t => parseInt(t.trim()));
      const result = await simulateScheduling(selectedAlgorithm, processes, {
        timeQuantum,
        preemptive,
        timeQuantums: tqs,
      });

      if (result.success) {
        setGanttChart(result.ganttChart);
        setMetrics(result.metrics);
      } else {
        setError(result.error || 'Simulation failed');
      }
    } catch (err) {
      setError('Failed to run simulation. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const showTimeQuantum = selectedAlgorithm === 'rr';
  const showPreemptive = selectedAlgorithm === 'priority';
  const showTimeQuantums = selectedAlgorithm === 'mlq' || selectedAlgorithm === 'mlfq';

  return (
    <div className="App">
      <div className="header">
        <h1>🖥️ Multi-Algorithm CPU Scheduler Simulator</h1>
        <p>Visualize and Compare FCFS, SJF, SRTF, RR, Priority, MLQ, and MLFQ Scheduling Algorithms</p>
      </div>

      <div className="container">
        <div className="control-panel">
          <div className="control-group">
            <label>Scheduling Algorithm</label>
            <select
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
            >
              {algorithms.map(alg => (
                <option key={alg.id} value={alg.id}>
                  {alg.name} ({alg.abbr})
                </option>
              ))}
            </select>
          </div>

          {showTimeQuantum && (
            <div className="control-group">
              <label>Time Quantum</label>
              <input
                type="number"
                value={timeQuantum}
                onChange={(e) => setTimeQuantum(parseInt(e.target.value) || 1)}
                min="1"
              />
            </div>
          )}

          {showPreemptive && (
            <div className="control-group">
              <div className="checkbox-group">
                <input
                  type="checkbox"
                  checked={preemptive}
                  onChange={(e) => setPreemptive(e.target.checked)}
                  id="preemptive"
                />
                <label htmlFor="preemptive">Preemptive Mode</label>
              </div>
            </div>
          )}

          {showTimeQuantums && (
            <div className="control-group">
              <label>Time Quantums (comma-separated)</label>
              <input
                type="text"
                value={timeQuantums}
                onChange={(e) => setTimeQuantums(e.target.value)}
                placeholder="e.g., 2,4,8"
              />
            </div>
          )}
        </div>

        <ProcessInput processes={processes} setProcesses={setProcesses} />

        <div className="button-group">
          <button className="btn-primary" onClick={runSimulation} disabled={loading}>
            {loading ? 'Running...' : 'Run Simulation'}
          </button>
          <button className="btn-secondary" onClick={loadSampleData}>
            Load Sample Data
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {ganttChart && (
          <div className="results">
            <h2>Results</h2>
            <GanttChart ganttData={ganttChart} />
            <Metrics metrics={metrics} />
          </div>
        )}

        {!ganttChart && !loading && processes.length === 0 && (
          <div className="info-box">
            <strong>Getting Started:</strong>
            <ol style={{ marginTop: '10px', marginLeft: '20px' }}>
              <li>Click "Load Sample Data" to load example processes</li>
              <li>Or add your own processes using the form above</li>
              <li>Select a scheduling algorithm</li>
              <li>Configure algorithm-specific parameters if needed</li>
              <li>Click "Run Simulation" to see the results</li>
            </ol>
          </div>
        )}
      </div>

      <div style={{ textAlign: 'center', color: 'white', padding: '20px' }}>
        <p>Built with React | Python | Flask</p>
        <p style={{ fontSize: '0.9em', marginTop: '5px' }}>
          OS Project - CPU Scheduling Algorithm Simulator
        </p>
      </div>
    </div>
  );
}

export default App;
