# Usage Guide - Multi-Algorithm CPU Scheduler Simulator

## Table of Contents
1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [Web GUI Usage](#web-gui-usage)
4. [CLI Usage](#cli-usage)
5. [Algorithm Details](#algorithm-details)
6. [Process Data Format](#process-data-format)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Running the Application

### Method 1: Web Application (React + Flask)

**Start the Backend:**
```bash
cd backend
python api.py
```
Backend will be available at: `http://localhost:5001`

**Start the Frontend (in a new terminal):**
```bash
cd frontend
npm start
```
Frontend will open automatically at: `http://localhost:3000`

### Method 2: Standalone HTML Demo

**Start the Backend:**
```bash
cd backend
python api.py
```

**Open the Demo:**
Open `demo.html` in your web browser. This provides a quick demo without needing to run npm.

### Method 3: Command Line Interface (CLI)

```bash
cd backend
python cli.py --algorithm <algorithm> [options]
```

## Web GUI Usage

### Step-by-Step Guide

1. **Select Algorithm**
   - Choose from: FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ
   - Algorithm-specific options will appear automatically

2. **Configure Parameters** (if applicable)
   - **Round Robin**: Set time quantum (default: 2)
   - **Priority**: Toggle preemptive mode
   - **MLQ/MLFQ**: Set time quantums for each queue level

3. **Add Processes**
   - Enter Process ID, Arrival Time, Burst Time, Priority, Queue Level
   - Click "Add Process" to add to the list
   - Or click "Load Sample Data" for example processes

4. **Run Simulation**
   - Click "Run Simulation" button
   - View the Gantt chart visualization
   - Review the calculated metrics

5. **Interpret Results**
   - **Gantt Chart**: Visual timeline of process execution
   - **Metrics**: Performance statistics

## CLI Usage

### Basic Syntax
```bash
python cli.py --algorithm <alg> --processes '<json>' [options]
```

### Options
- `--algorithm, -a`: Algorithm to use (required)
  - Choices: `fcfs`, `sjf`, `srtf`, `rr`, `priority`, `mlq`, `mlfq`
- `--processes, -p`: JSON array of process data
- `--file, -f`: JSON file containing process data
- `--time-quantum, -tq`: Time quantum for RR (default: 2)
- `--preemptive`: Use preemptive mode for priority scheduling
- `--time-quantums, -tqs`: JSON array of time quantums for MLQ/MLFQ

### CLI Examples

#### FCFS (First Come First Serve)
```bash
python cli.py --algorithm fcfs --processes '[
  {"pid":1,"arrival_time":0,"burst_time":4},
  {"pid":2,"arrival_time":1,"burst_time":3}
]'
```

#### SJF (Shortest Job First)
```bash
python cli.py --algorithm sjf --file sample_processes.json
```

#### Round Robin (Time Quantum = 3)
```bash
python cli.py --algorithm rr --time-quantum 3 --processes '[
  {"pid":1,"arrival_time":0,"burst_time":5},
  {"pid":2,"arrival_time":2,"burst_time":3},
  {"pid":3,"arrival_time":4,"burst_time":1}
]'
```

#### Priority Scheduling (Non-preemptive)
```bash
python cli.py --algorithm priority --processes '[
  {"pid":1,"arrival_time":0,"burst_time":4,"priority":2},
  {"pid":2,"arrival_time":1,"burst_time":3,"priority":1},
  {"pid":3,"arrival_time":2,"burst_time":1,"priority":3}
]'
```

#### Priority Scheduling (Preemptive)
```bash
python cli.py --algorithm priority --preemptive --processes '[
  {"pid":1,"arrival_time":0,"burst_time":4,"priority":2},
  {"pid":2,"arrival_time":1,"burst_time":3,"priority":1}
]'
```

#### MLFQ (Custom Time Quantums)
```bash
python cli.py --algorithm mlfq --time-quantums "[2,4,8]" --file sample_processes.json
```

## Algorithm Details

### FCFS (First Come First Serve)
- **Type**: Non-preemptive
- **Policy**: Processes executed in order of arrival
- **Advantages**: Simple, fair in arrival order
- **Disadvantages**: Can cause convoy effect

### SJF (Shortest Job First)
- **Type**: Non-preemptive
- **Policy**: Shortest burst time first
- **Advantages**: Minimizes average waiting time
- **Disadvantages**: Can cause starvation of long processes

### SRTF (Shortest Remaining Time First)
- **Type**: Preemptive (Preemptive SJF)
- **Policy**: Process with shortest remaining time runs
- **Advantages**: Better response time than SJF
- **Disadvantages**: More context switches, starvation risk

### Round Robin
- **Type**: Preemptive
- **Policy**: Each process gets fixed time quantum
- **Parameters**: Time quantum (configurable)
- **Advantages**: Fair, good response time
- **Disadvantages**: Performance depends on time quantum

### Priority Scheduling
- **Type**: Preemptive or Non-preemptive
- **Policy**: Highest priority (lowest number) first
- **Parameters**: Preemptive mode (toggle)
- **Advantages**: Important processes get CPU first
- **Disadvantages**: Starvation possible, priority inversion

### MLQ (Multi-Level Queue)
- **Type**: Preemptive
- **Policy**: Multiple queues with fixed priorities
- **Parameters**: Time quantum per queue level
- **Advantages**: Different scheduling for different process types
- **Disadvantages**: Inflexible, starvation in lower queues

### MLFQ (Multi-Level Feedback Queue)
- **Type**: Preemptive
- **Policy**: Processes move between queues based on behavior
- **Parameters**: Time quantum per level
- **Advantages**: Adaptive, balances response and turnaround
- **Disadvantages**: Complex, tuning required

## Process Data Format

### JSON Structure
```json
{
  "pid": 1,              // Process ID (integer > 0)
  "arrivalTime": 0,      // Arrival time (integer >= 0)
  "burstTime": 5,        // CPU burst time (integer > 0)
  "priority": 2,         // Priority level (integer >= 0, lower = higher priority)
  "queueLevel": 0        // Initial queue level for MLQ/MLFQ (integer >= 0)
}
```

### Python CLI Format (snake_case)
```json
{
  "pid": 1,
  "arrival_time": 0,
  "burst_time": 5,
  "priority": 2,
  "queue_level": 0
}
```

### Web API Format (camelCase)
```json
{
  "pid": 1,
  "arrivalTime": 0,
  "burstTime": 5,
  "priority": 2,
  "queueLevel": 0
}
```

## Examples

### Example 1: Comparing Algorithms

Create a file `test_processes.json`:
```json
[
  {"pid": 1, "arrival_time": 0, "burst_time": 8, "priority": 3},
  {"pid": 2, "arrival_time": 1, "burst_time": 4, "priority": 1},
  {"pid": 3, "arrival_time": 2, "burst_time": 2, "priority": 2},
  {"pid": 4, "arrival_time": 3, "burst_time": 1, "priority": 1}
]
```

Run different algorithms:
```bash
# FCFS
python cli.py -a fcfs -f test_processes.json

# SJF
python cli.py -a sjf -f test_processes.json

# SRTF
python cli.py -a srtf -f test_processes.json

# RR (quantum=2)
python cli.py -a rr -tq 2 -f test_processes.json

# Priority (non-preemptive)
python cli.py -a priority -f test_processes.json

# Priority (preemptive)
python cli.py -a priority --preemptive -f test_processes.json
```

### Example 2: Testing Round Robin with Different Time Quantums

```bash
# Time Quantum = 1
python cli.py -a rr -tq 1 -f test_processes.json

# Time Quantum = 2
python cli.py -a rr -tq 2 -f test_processes.json

# Time Quantum = 4
python cli.py -a rr -tq 4 -f test_processes.json
```

### Example 3: Multi-Level Feedback Queue

```bash
python cli.py -a mlfq -tqs "[1,2,4]" --processes '[
  {"pid":1,"arrival_time":0,"burst_time":10},
  {"pid":2,"arrival_time":2,"burst_time":5},
  {"pid":3,"arrival_time":4,"burst_time":3}
]'
```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :5001
# Kill it
kill <PID>
# Or change port in api.py
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**npm install fails:**
```bash
# Clear cache
npm cache clean --force
# Try again
npm install
```

**Can't connect to backend:**
- Ensure backend is running on port 5001
- Check CORS settings
- Verify API_URL in `frontend/src/utils/api.js`

### CLI Issues

**JSON parse error:**
- Check JSON syntax (quotes, commas)
- Use a JSON validator
- Try using a file instead: `--file processes.json`

**No module named 'scheduler':**
```bash
# Make sure you're in the backend directory
cd backend
python cli.py ...
```

## Performance Tips

1. **Time Quantum Selection (RR)**
   - Too small: Excessive context switching
   - Too large: Becomes like FCFS
   - Typical: 10-100ms in real systems

2. **Priority Levels**
   - Use 0-10 range for clarity
   - Lower number = higher priority
   - Avoid too many levels (3-5 is typical)

3. **Queue Levels (MLQ/MLFQ)**
   - Usually 3-4 levels
   - Increase quantum as level decreases
   - Example: [2, 4, 8] or [1, 2, 4, 8]

## Additional Resources

- Operating Systems Concepts (Silberschatz, Galvin, Gagne)
- Modern Operating Systems (Tanenbaum)
- [GitHub Repository](https://github.com/ali2943/Multi-Algorithm-Scheduler-Simulator)
