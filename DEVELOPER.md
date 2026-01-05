# Developer Guide - Multi-Algorithm CPU Scheduler Simulator

## Project Overview

This project implements a comprehensive CPU scheduling algorithm simulator with:
- **Backend**: Python (Flask API + CLI)
- **Frontend**: React (Web GUI)
- **Algorithms**: FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ

## Architecture

### Backend Structure

```
backend/
├── scheduler.py      # Core algorithm implementations
├── api.py           # Flask REST API
├── cli.py           # Command-line interface
├── requirements.txt # Python dependencies
└── sample_processes.json # Test data
```

#### Key Classes

**Process**
- Represents a single process with attributes:
  - `pid`: Process ID
  - `arrival_time`: When process arrives
  - `burst_time`: CPU time needed
  - `remaining_time`: Time left to execute
  - `priority`: Priority level (lower = higher priority)
  - `queue_level`: Queue level for MLQ/MLFQ
  - Metrics: `waiting_time`, `turnaround_time`, `response_time`

**Scheduler**
- Static class with algorithm implementations
- Each algorithm returns: `(gantt_chart, metrics)`
- Gantt chart: List of `{pid, start, end}` entries
- Metrics: Dictionary with performance statistics

### Frontend Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── components/
│   │   ├── GanttChart.js    # Gantt chart visualization
│   │   ├── Metrics.js       # Metrics display
│   │   └── ProcessInput.js  # Process input form
│   ├── utils/
│   │   └── api.js           # API communication
│   ├── styles/
│   │   └── App.css          # Styling
│   ├── App.js               # Main component
│   └── index.js             # Entry point
└── package.json             # Dependencies
```

## Algorithm Implementations

### FCFS (First Come First Serve)
- **Type**: Non-preemptive
- **Implementation**: Sort by arrival time, execute in order
- **Time Complexity**: O(n log n)
- **Use Case**: Simple, fair for batch systems

### SJF (Shortest Job First)
- **Type**: Non-preemptive
- **Implementation**: Select process with shortest burst time
- **Time Complexity**: O(n²) worst case
- **Use Case**: Minimizes average waiting time

### SRTF (Shortest Remaining Time First)
- **Type**: Preemptive
- **Implementation**: Preempt if shorter job arrives
- **Time Complexity**: O(n * max_time)
- **Use Case**: Better response time than SJF

### Round Robin
- **Type**: Preemptive
- **Implementation**: Time quantum-based cycling
- **Time Complexity**: O(n * total_time / quantum)
- **Use Case**: Time-sharing systems, fair CPU distribution

### Priority Scheduling
- **Type**: Preemptive or Non-preemptive
- **Implementation**: Execute highest priority first
- **Time Complexity**: O(n²) worst case
- **Use Case**: Real-time systems, priority-based execution

### MLQ (Multi-Level Queue)
- **Type**: Preemptive
- **Implementation**: Fixed priority queues, RR within each
- **Time Complexity**: O(n * time)
- **Use Case**: Different process types need different scheduling

### MLFQ (Multi-Level Feedback Queue)
- **Type**: Preemptive
- **Implementation**: Dynamic queue movement based on behavior
- **Time Complexity**: O(n * time)
- **Use Case**: Adaptive scheduling, unknown process characteristics

## API Endpoints

### POST /api/simulate
Runs a scheduling simulation.

**Request:**
```json
{
  "algorithm": "fcfs|sjf|srtf|rr|priority|mlq|mlfq",
  "processes": [
    {
      "pid": 1,
      "arrivalTime": 0,
      "burstTime": 5,
      "priority": 2,
      "queueLevel": 0
    }
  ],
  "timeQuantum": 2,
  "preemptive": false,
  "timeQuantums": [2, 4, 8]
}
```

**Response:**
```json
{
  "success": true,
  "ganttChart": [
    {"pid": 1, "start": 0, "end": 5}
  ],
  "metrics": {
    "avg_waiting_time": 0,
    "avg_turnaround_time": 5,
    "cpu_utilization": 100.0,
    "total_processes": 1
  }
}
```

### GET /api/algorithms
Returns list of available algorithms.

## Adding New Algorithms

1. **Add to scheduler.py**:
```python
@staticmethod
def my_algorithm(processes: List[Process], **kwargs) -> Tuple[List[Dict], Dict]:
    processes = copy.deepcopy(processes)
    gantt_chart = []
    completed = []
    
    # Your implementation here
    
    metrics = Scheduler.calculate_metrics(completed)
    return gantt_chart, metrics
```

2. **Add to api.py**:
```python
elif algorithm == 'my_algorithm':
    gantt, metrics = Scheduler.my_algorithm(processes)
```

3. **Add to cli.py**:
```python
parser.add_argument(
    '--algorithm', '-a',
    choices=['fcfs', 'sjf', ..., 'my_algorithm'],
    # ...
)
```

4. **Update frontend** in `utils/api.js`:
```javascript
{ id: 'my_algorithm', name: 'My Algorithm', abbr: 'MA' }
```

## Testing

### Unit Testing (Backend)
Create `backend/test_scheduler.py`:
```python
import unittest
from scheduler import Scheduler, Process

class TestScheduler(unittest.TestCase):
    def test_fcfs(self):
        processes = [
            Process(1, 0, 4),
            Process(2, 1, 3)
        ]
        gantt, metrics = Scheduler.fcfs(processes)
        self.assertEqual(len(gantt), 2)
        self.assertGreater(metrics['cpu_utilization'], 0)
```

### Integration Testing
Test API endpoints:
```bash
# Test algorithms endpoint
curl http://localhost:5001/api/algorithms

# Test simulation
curl -X POST http://localhost:5001/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"algorithm":"fcfs","processes":[...]}'
```

### Manual Testing
```bash
# CLI testing
python cli.py -a fcfs -f sample_processes.json
python cli.py -a rr -tq 3 -f sample_processes.json

# Web testing
# 1. Start backend: python api.py
# 2. Open demo.html or start React app
# 3. Test each algorithm with various inputs
```

## Performance Optimization

### Backend Optimizations
1. **Use generators** for large process sets
2. **Implement caching** for repeated calculations
3. **Optimize sorting** algorithms
4. **Use numpy** for numeric operations

### Frontend Optimizations
1. **Memoize components** with React.memo
2. **Debounce input** for real-time updates
3. **Lazy load** algorithm implementations
4. **Virtual scrolling** for large Gantt charts

## Deployment

### Backend Deployment
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 api:app
```

### Frontend Deployment
```bash
# Build production bundle
cd frontend
npm run build

# Serve static files
# Use nginx, Apache, or any static file server
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
# Backend
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "api:app"]
```

## Common Issues

### Issue: Port Already in Use
```bash
# Find process using port
lsof -i :5001
# Kill it
kill <PID>
```

### Issue: CORS Errors
Ensure `flask-cors` is installed and enabled:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

### Issue: Process Metrics Wrong
- Check process arrival times are non-negative
- Verify burst times are positive
- Ensure completion time calculations are correct

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## Code Style

**Python**: Follow PEP 8
```bash
# Install formatter
pip install black
# Format code
black backend/
```

**JavaScript**: Follow Airbnb style guide
```bash
# Install ESLint
npm install --save-dev eslint
# Check code
npx eslint src/
```

## Resources

- [Operating Systems Concepts](https://www.os-book.com/)
- [CPU Scheduling Algorithms](https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)

## License

This project is for educational purposes as part of an Operating Systems course.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
