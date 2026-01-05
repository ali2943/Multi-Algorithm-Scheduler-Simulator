"""
Flask API for Multi-Algorithm Scheduler Simulator
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduler import Scheduler, Process

app = Flask(__name__)
CORS(app)


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run scheduling simulation"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'fcfs')
        processes_data = data.get('processes', [])
        time_quantum = data.get('timeQuantum', 2)
        preemptive = data.get('preemptive', False)
        time_quantums = data.get('timeQuantums', [2, 4, 8])
        
        # Create process objects
        processes = []
        for p_data in processes_data:
            process = Process(
                pid=p_data.get('pid', len(processes) + 1),
                arrival_time=p_data.get('arrivalTime', 0),
                burst_time=p_data.get('burstTime', 1),
                priority=p_data.get('priority', 0),
                queue_level=p_data.get('queueLevel', 0)
            )
            processes.append(process)
        
        # Run appropriate algorithm
        if algorithm == 'fcfs':
            gantt, metrics = Scheduler.fcfs(processes)
        elif algorithm == 'sjf':
            gantt, metrics = Scheduler.sjf(processes)
        elif algorithm == 'srtf':
            gantt, metrics = Scheduler.srtf(processes)
        elif algorithm == 'rr':
            gantt, metrics = Scheduler.round_robin(processes, time_quantum)
        elif algorithm == 'priority':
            gantt, metrics = Scheduler.priority_scheduling(processes, preemptive)
        elif algorithm == 'mlq':
            gantt, metrics = Scheduler.mlq(processes, time_quantums)
        elif algorithm == 'mlfq':
            gantt, metrics = Scheduler.mlfq(processes, time_quantums)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify({
            'ganttChart': gantt,
            'metrics': metrics,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get list of available algorithms"""
    algorithms = [
        {'id': 'fcfs', 'name': 'First Come First Serve', 'abbr': 'FCFS'},
        {'id': 'sjf', 'name': 'Shortest Job First', 'abbr': 'SJF'},
        {'id': 'srtf', 'name': 'Shortest Remaining Time First', 'abbr': 'SRTF'},
        {'id': 'rr', 'name': 'Round Robin', 'abbr': 'RR'},
        {'id': 'priority', 'name': 'Priority Scheduling', 'abbr': 'Priority'},
        {'id': 'mlq', 'name': 'Multi-Level Queue', 'abbr': 'MLQ'},
        {'id': 'mlfq', 'name': 'Multi-Level Feedback Queue', 'abbr': 'MLFQ'},
    ]
    return jsonify(algorithms)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
