# Quick Start Guide

Get started with the Multi-Algorithm CPU Scheduler Simulator in 5 minutes!

## 🚀 Fastest Way: Standalone Demo

1. **Start the Backend**
```bash
cd backend
pip install flask flask-cors
python api.py
```

2. **Open the Demo**
- Open `demo.html` in your web browser
- Or navigate to: `http://localhost:8080/demo.html` if serving via HTTP

3. **Run Your First Simulation**
- Click "Run Simulation" to use the default data
- Or modify the JSON data and try different algorithms

**That's it!** You now have a working CPU scheduler simulator.

---

## 📊 CLI Quick Start

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run FCFS with default data
python cli.py --algorithm fcfs

# Run Round Robin with custom time quantum
python cli.py --algorithm rr --time-quantum 3 --file sample_processes.json

# Compare all algorithms
for alg in fcfs sjf srtf rr priority mlq mlfq; do
  echo "=== $alg ==="
  python cli.py -a $alg -f sample_processes.json
done
```

---

## 🌐 Full React App (Optional)

If you want the complete React experience:

1. **Terminal 1 - Backend**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

2. **Terminal 2 - Frontend**
```bash
cd frontend
npm install
npm start
```

3. **Open Browser**
- Navigate to `http://localhost:3000`
- Enjoy the full-featured interface!

---

## 📝 Example: Custom Process Data

Create `my_processes.json`:
```json
[
  {"pid": 1, "arrival_time": 0, "burst_time": 8, "priority": 1},
  {"pid": 2, "arrival_time": 1, "burst_time": 4, "priority": 2},
  {"pid": 3, "arrival_time": 2, "burst_time": 2, "priority": 1}
]
```

Run it:
```bash
python cli.py --algorithm sjf --file my_processes.json
```

---

## 🎯 Try Different Algorithms

### FCFS (First Come First Serve)
```bash
python cli.py -a fcfs -f sample_processes.json
```

### Round Robin (Time Quantum = 4)
```bash
python cli.py -a rr -tq 4 -f sample_processes.json
```

### Priority (Preemptive)
```bash
python cli.py -a priority --preemptive -f sample_processes.json
```

### MLFQ (Multi-Level Feedback Queue)
```bash
python cli.py -a mlfq -tqs "[1,2,4]" -f sample_processes.json
```

---

## 🔧 Common Commands

```bash
# View help
python cli.py --help

# Use inline JSON
python cli.py -a fcfs -p '[{"pid":1,"arrival_time":0,"burst_time":5}]'

# Compare Round Robin with different time quantums
python cli.py -a rr -tq 2 -f sample_processes.json > rr_tq2.txt
python cli.py -a rr -tq 4 -f sample_processes.json > rr_tq4.txt
```

---

## 📈 Understanding Output

### Gantt Chart
```
Time: 0  4  7  8  13
Proc: P1    P2   P3 P4     
      |-----|----|--|------|
```
- Shows when each process (P1, P2, etc.) runs
- Time markers show the timeline

### Metrics
- **Avg Waiting Time**: How long processes wait in queue
- **Avg Turnaround Time**: Total time from arrival to completion
- **CPU Utilization**: % of time CPU is busy

---

## 🐛 Troubleshooting

**"Port already in use"**
```bash
# Kill process on port 5001
lsof -i :5001
kill <PID>
```

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Can't connect to backend"**
- Make sure `python api.py` is running
- Check it's on port 5001: `http://localhost:5001/api/algorithms`

---

## 📚 Next Steps

- Read the full [USAGE.md](USAGE.md) for detailed documentation
- Check [DEVELOPER.md](DEVELOPER.md) for implementation details
- Experiment with different algorithms and parameters
- Compare performance metrics across algorithms

---

## 💡 Pro Tips

1. **Compare Algorithms**: Run the same process set through different algorithms to see performance differences

2. **Time Quantum Matters**: For Round Robin, try quantum values from 1 to 10 and observe the impact

3. **Priority Starvation**: Create a scenario with low-priority processes to see starvation in action

4. **Export Results**: Redirect CLI output to files for analysis
   ```bash
   python cli.py -a fcfs -f data.json > results.txt
   ```

5. **Automation**: Create bash scripts to run batch simulations
   ```bash
   #!/bin/bash
   for alg in fcfs sjf srtf; do
     python cli.py -a $alg -f test.json >> comparison.txt
   done
   ```

---

**Happy Scheduling!** 🎉

For questions or issues, please check the main [README.md](README.md) or open an issue on GitHub.
