#!/usr/bin/env python3
"""
CLI Interface for Multi-Algorithm Scheduler Simulator
"""

import argparse
import json
from scheduler import Scheduler, Process


def print_gantt_chart(gantt_chart):
    """Print Gantt chart in ASCII format"""
    print("\n=== Gantt Chart ===")
    print("Time: ", end="")
    for entry in gantt_chart:
        print(f"{entry['start']}", end="  ")
    if gantt_chart:
        print(f"{gantt_chart[-1]['end']}")
    
    print("Proc: ", end="")
    for entry in gantt_chart:
        width = entry['end'] - entry['start']
        print(f"P{entry['pid']}", end=" " * max(1, width))
    print()
    
    # Visual bar
    print("      ", end="")
    for entry in gantt_chart:
        width = entry['end'] - entry['start']
        print("|" + "-" * (width + 1), end="")
    print("|")
    print()


def print_metrics(metrics):
    """Print scheduling metrics"""
    print("=== Metrics ===")
    print(f"Average Waiting Time: {metrics['avg_waiting_time']}")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
    print(f"CPU Utilization: {metrics['cpu_utilization']}%")
    print(f"Total Processes: {metrics['total_processes']}")
    print()


def run_simulation(algorithm, processes_data, **kwargs):
    """Run scheduling simulation"""
    # Create process objects
    processes = []
    for p_data in processes_data:
        process = Process(
            pid=p_data.get('pid', len(processes) + 1),
            arrival_time=p_data.get('arrival_time', 0),
            burst_time=p_data.get('burst_time', 1),
            priority=p_data.get('priority', 0),
            queue_level=p_data.get('queue_level', 0)
        )
        processes.append(process)
    
    print(f"\n{'='*50}")
    print(f"Running {algorithm.upper()} Scheduling Algorithm")
    print(f"{'='*50}")
    
    # Run appropriate algorithm
    if algorithm == 'fcfs':
        gantt, metrics = Scheduler.fcfs(processes)
    elif algorithm == 'sjf':
        gantt, metrics = Scheduler.sjf(processes)
    elif algorithm == 'srtf':
        gantt, metrics = Scheduler.srtf(processes)
    elif algorithm == 'rr':
        tq = kwargs.get('time_quantum', 2)
        print(f"Time Quantum: {tq}")
        gantt, metrics = Scheduler.round_robin(processes, tq)
    elif algorithm == 'priority':
        preemptive = kwargs.get('preemptive', False)
        print(f"Preemptive: {preemptive}")
        gantt, metrics = Scheduler.priority_scheduling(processes, preemptive)
    elif algorithm == 'mlq':
        tqs = kwargs.get('time_quantums', [2, 4])
        print(f"Time Quantums: {tqs}")
        gantt, metrics = Scheduler.mlq(processes, tqs)
    elif algorithm == 'mlfq':
        tqs = kwargs.get('time_quantums', [2, 4, 8])
        print(f"Time Quantums: {tqs}")
        gantt, metrics = Scheduler.mlfq(processes, tqs)
    else:
        print(f"Unknown algorithm: {algorithm}")
        return
    
    print_gantt_chart(gantt)
    print_metrics(metrics)


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Algorithm CPU Scheduler Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # FCFS with sample processes
  python cli.py --algorithm fcfs --processes '[{"pid":1,"arrival_time":0,"burst_time":4},{"pid":2,"arrival_time":1,"burst_time":3}]'
  
  # Round Robin with time quantum 3
  python cli.py --algorithm rr --time-quantum 3 --processes '[{"pid":1,"arrival_time":0,"burst_time":5},{"pid":2,"arrival_time":2,"burst_time":3}]'
  
  # Priority scheduling (non-preemptive)
  python cli.py --algorithm priority --processes '[{"pid":1,"arrival_time":0,"burst_time":4,"priority":2},{"pid":2,"arrival_time":1,"burst_time":3,"priority":1}]'
        """
    )
    
    parser.add_argument(
        '--algorithm', '-a',
        choices=['fcfs', 'sjf', 'srtf', 'rr', 'priority', 'mlq', 'mlfq'],
        required=True,
        help='Scheduling algorithm to use'
    )
    
    parser.add_argument(
        '--processes', '-p',
        type=str,
        help='JSON array of process data'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='JSON file containing process data'
    )
    
    parser.add_argument(
        '--time-quantum', '-tq',
        type=int,
        default=2,
        help='Time quantum for RR (default: 2)'
    )
    
    parser.add_argument(
        '--preemptive',
        action='store_true',
        help='Use preemptive mode for priority scheduling'
    )
    
    parser.add_argument(
        '--time-quantums', '-tqs',
        type=str,
        help='JSON array of time quantums for MLQ/MLFQ (e.g., "[2,4,8]")'
    )
    
    args = parser.parse_args()
    
    # Load process data
    if args.file:
        with open(args.file, 'r') as f:
            processes_data = json.load(f)
    elif args.processes:
        processes_data = json.loads(args.processes)
    else:
        # Default sample processes
        print("No processes specified. Using default sample data.")
        processes_data = [
            {'pid': 1, 'arrival_time': 0, 'burst_time': 4, 'priority': 2, 'queue_level': 0},
            {'pid': 2, 'arrival_time': 1, 'burst_time': 3, 'priority': 1, 'queue_level': 0},
            {'pid': 3, 'arrival_time': 2, 'burst_time': 1, 'priority': 3, 'queue_level': 1},
            {'pid': 4, 'arrival_time': 3, 'burst_time': 5, 'priority': 2, 'queue_level': 0},
        ]
    
    # Prepare kwargs
    kwargs = {
        'time_quantum': args.time_quantum,
        'preemptive': args.preemptive
    }
    
    if args.time_quantums:
        kwargs['time_quantums'] = json.loads(args.time_quantums)
    
    # Run simulation
    run_simulation(args.algorithm, processes_data, **kwargs)


if __name__ == '__main__':
    main()
