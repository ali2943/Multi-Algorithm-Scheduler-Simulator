# Multi-Algorithm CPU Scheduler Simulator

A comprehensive CPU scheduling algorithm simulator with both **Web GUI** (React) and **CLI** interfaces. This project implements and visualizes multiple scheduling algorithms with interactive Gantt charts and automated metrics calculation.

## 🎯 Features

### Scheduling Algorithms Implemented
1. **FCFS** - First Come First Serve
2. **SJF** - Shortest Job First (Non-preemptive)
3. **SRTF** - Shortest Remaining Time First (Preemptive SJF)
4. **RR** - Round Robin (configurable time quantum)
5. **Priority** - Priority Scheduling (preemptive and non-preemptive)
6. **MLQ** - Multi-Level Queue
7. **MLFQ** - Multi-Level Feedback Queue

### Key Features
- 📊 **Interactive Gantt Charts** - Visual timeline of process execution
- 📈 **Automated Metrics** - Average waiting time, turnaround time, CPU utilization
- 🌐 **Web GUI** - Beautiful, responsive React-based interface
- 💻 **CLI Interface** - Command-line tool for automation and scripting
- ⚙️ **Configurable Parameters** - Time quantum, priorities, queue levels
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

## 💻 Usage

### Web GUI

1. **Start the Backend Server:**
```bash
cd backend
python api.py
```
The API server will start at `http://localhost:5000`

2. **Start the Frontend Development Server:**
```bash
cd frontend
npm start
```
The web interface will open at `http://localhost:3000`

3. **Use the Interface:**
   - Add processes with their arrival time, burst time, priority, and queue level
   - Select a scheduling algorithm
   - Configure algorithm-specific parameters (time quantum, preemptive mode, etc.)
   - Click "Run Simulation" to see the Gantt chart and metrics

### CLI Interface

Run simulations from the command line:

```bash
cd backend
python cli.py --algorithm <algorithm> --processes '<json_data>'
```

#### CLI Examples

**FCFS:**
```bash
python cli.py --algorithm fcfs --processes '[{"pid":1,"arrival_time":0,"burst_time":4},{"pid":2,"arrival_time":1,"burst_time":3}]'
```

**Round Robin with Time Quantum 3:**
```bash
python cli.py --algorithm rr --time-quantum 3 --processes '[{"pid":1,"arrival_time":0,"burst_time":5},{"pid":2,"arrival_time":2,"burst_time":3}]'
```

**Priority Scheduling (Non-preemptive):**
```bash
python cli.py --algorithm priority --processes '[{"pid":1,"arrival_time":0,"burst_time":4,"priority":2},{"pid":2,"arrival_time":1,"burst_time":3,"priority":1}]'
```

**Priority Scheduling (Preemptive):**
```bash
python cli.py --algorithm priority --preemptive --processes '[{"pid":1,"arrival_time":0,"burst_time":4,"priority":2},{"pid":2,"arrival_time":1,"burst_time":3,"priority":1}]'
```

**Using a JSON file:**
```bash
python cli.py --algorithm sjf --file processes.json
```

**MLFQ with custom time quantums:**
```bash
python cli.py --algorithm mlfq --time-quantums "[2,4,8]" --processes '[{"pid":1,"arrival_time":0,"burst_time":10}]'
```

## 📊 Metrics Calculated

The simulator automatically calculates:

- **Average Waiting Time** - Average time processes wait in ready queue
- **Average Turnaround Time** - Average time from arrival to completion
- **CPU Utilization** - Percentage of time CPU is actively executing processes
- **Individual Process Metrics** - Waiting time, turnaround time, response time per process

## 🏗️ Project Structure

```
Multi-Algorithm-Scheduler-Simulator/
├── backend/
│   ├── scheduler.py       # Core scheduling algorithms implementation
│   ├── api.py            # Flask REST API server
│   ├── cli.py            # Command-line interface
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html    # HTML template
│   ├── src/
│   │   ├── components/   # React components
│   │   │   ├── GanttChart.js
│   │   │   ├── Metrics.js
│   │   │   └── ProcessInput.js
│   │   ├── utils/        # Utility functions
│   │   │   └── api.js
│   │   ├── styles/       # CSS stylesheets
│   │   │   └── App.css
│   │   ├── App.js        # Main React component
│   │   └── index.js      # React entry point
│   └── package.json      # Node.js dependencies
└── README.md             # This file
```

## 🎓 Concepts Covered

### CPU Scheduling
- Non-preemptive vs Preemptive scheduling
- Context switching
- Process states and transitions
- Scheduling criteria (CPU utilization, throughput, waiting time, etc.)

### Data Structures
- Process Control Block (PCB)
- Ready queues
- Multi-level queues
- Priority queues

### Simulation
- Discrete event simulation
- Gantt chart generation
- Performance metrics calculation

## 🔧 Configuration

### Time Quantum (Round Robin)
Adjustable via GUI slider or `--time-quantum` CLI flag. Default: 2

### Priority Levels
Lower numbers indicate higher priority. Range: 0-∞

### Queue Levels (MLQ/MLFQ)
Queue 0 = highest priority. Configure time quantums per queue.

## 📱 Screenshots

The web interface features:
- Clean, modern design with gradient backgrounds
- Interactive process input forms
- Real-time Gantt chart visualization
- Color-coded process blocks
- Metric cards with key performance indicators

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more scheduling algorithms
- Improve the UI/UX
- Add more metrics
- Enhance visualizations
- Add unit tests

## 📝 License

This project is for educational purposes as part of an Operating Systems course.

## 👨‍💻 Author

OS Project - Multi-Algorithm Scheduler Simulator

## 🙏 Acknowledgments

- Operating Systems concepts and algorithms
- React and Flask frameworks
- CPU scheduling theory and implementation
