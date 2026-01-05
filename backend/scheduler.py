"""
Multi-Algorithm CPU Scheduler Simulator
Implements: FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ
"""

from typing import List, Dict, Tuple
import copy


class Process:
    """Process data structure"""
    def __init__(self, pid: int, arrival_time: int, burst_time: int, 
                 priority: int = 0, queue_level: int = 0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.queue_level = queue_level
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1


class Scheduler:
    """Base scheduler class with common functionality"""
    
    @staticmethod
    def calculate_metrics(processes: List[Process]) -> Dict:
        """Calculate scheduling metrics"""
        total_waiting = sum(p.waiting_time for p in processes)
        total_turnaround = sum(p.turnaround_time for p in processes)
        total_burst = sum(p.burst_time for p in processes)
        
        avg_waiting = total_waiting / len(processes)
        avg_turnaround = total_turnaround / len(processes)
        
        # CPU utilization
        if processes:
            max_completion = max(p.completion_time for p in processes)
            cpu_utilization = (total_burst / max_completion * 100) if max_completion > 0 else 0
        else:
            cpu_utilization = 0
            
        return {
            'avg_waiting_time': round(avg_waiting, 2),
            'avg_turnaround_time': round(avg_turnaround, 2),
            'cpu_utilization': round(cpu_utilization, 2),
            'total_processes': len(processes)
        }
    
    @staticmethod
    def fcfs(processes: List[Process]) -> Tuple[List[Dict], Dict]:
        """First Come First Serve scheduling"""
        processes = copy.deepcopy(processes)
        processes.sort(key=lambda p: p.arrival_time)
        
        gantt_chart = []
        current_time = 0
        
        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            process.start_time = current_time
            process.response_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            gantt_chart.append({
                'pid': process.pid,
                'start': current_time,
                'end': process.completion_time
            })
            
            current_time = process.completion_time
        
        metrics = Scheduler.calculate_metrics(processes)
        return gantt_chart, metrics
    
    @staticmethod
    def sjf(processes: List[Process]) -> Tuple[List[Dict], Dict]:
        """Shortest Job First (Non-preemptive) scheduling"""
        processes = copy.deepcopy(processes)
        gantt_chart = []
        current_time = 0
        completed = []
        remaining = processes.copy()
        
        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p.arrival_time <= current_time]
            
            if not available:
                current_time = min(p.arrival_time for p in remaining)
                continue
            
            # Select process with shortest burst time
            process = min(available, key=lambda p: p.burst_time)
            remaining.remove(process)
            
            process.start_time = current_time
            process.response_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            gantt_chart.append({
                'pid': process.pid,
                'start': current_time,
                'end': process.completion_time
            })
            
            current_time = process.completion_time
            completed.append(process)
        
        metrics = Scheduler.calculate_metrics(completed)
        return gantt_chart, metrics
    
    @staticmethod
    def srtf(processes: List[Process]) -> Tuple[List[Dict], Dict]:
        """Shortest Remaining Time First (Preemptive SJF) scheduling"""
        processes = copy.deepcopy(processes)
        gantt_chart = []
        current_time = 0
        completed = []
        remaining = processes.copy()
        current_process = None
        
        while remaining or current_process:
            # Get processes that have arrived
            available = [p for p in remaining if p.arrival_time <= current_time]
            
            if current_process:
                available.append(current_process)
            
            if not available:
                current_time = min(p.arrival_time for p in remaining)
                continue
            
            # Select process with shortest remaining time
            process = min(available, key=lambda p: p.remaining_time)
            
            if process != current_process:
                if current_process and len(gantt_chart) > 0:
                    gantt_chart[-1]['end'] = current_time
                current_process = process
                if process in remaining:
                    remaining.remove(process)
                if process.start_time == -1:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                gantt_chart.append({
                    'pid': process.pid,
                    'start': current_time,
                    'end': current_time
                })
            
            # Execute for 1 time unit
            current_time += 1
            process.remaining_time -= 1
            
            if process.remaining_time == 0:
                gantt_chart[-1]['end'] = current_time
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed.append(process)
                current_process = None
        
        metrics = Scheduler.calculate_metrics(completed)
        return gantt_chart, metrics
    
    @staticmethod
    def round_robin(processes: List[Process], time_quantum: int = 2) -> Tuple[List[Dict], Dict]:
        """Round Robin scheduling"""
        processes = copy.deepcopy(processes)
        gantt_chart = []
        current_time = 0
        completed = []
        queue = []
        remaining = sorted(processes, key=lambda p: p.arrival_time)
        
        while remaining or queue:
            # Add newly arrived processes to queue
            while remaining and remaining[0].arrival_time <= current_time:
                queue.append(remaining.pop(0))
            
            if not queue:
                if remaining:
                    current_time = remaining[0].arrival_time
                continue
            
            process = queue.pop(0)
            
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute for time quantum or remaining time
            exec_time = min(time_quantum, process.remaining_time)
            start = current_time
            current_time += exec_time
            process.remaining_time -= exec_time
            
            gantt_chart.append({
                'pid': process.pid,
                'start': start,
                'end': current_time
            })
            
            # Add newly arrived processes
            while remaining and remaining[0].arrival_time <= current_time:
                queue.append(remaining.pop(0))
            
            if process.remaining_time > 0:
                queue.append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed.append(process)
        
        metrics = Scheduler.calculate_metrics(completed)
        return gantt_chart, metrics
    
    @staticmethod
    def priority_scheduling(processes: List[Process], preemptive: bool = False) -> Tuple[List[Dict], Dict]:
        """Priority scheduling (lower number = higher priority)"""
        processes = copy.deepcopy(processes)
        
        if not preemptive:
            # Non-preemptive priority
            gantt_chart = []
            current_time = 0
            completed = []
            remaining = processes.copy()
            
            while remaining:
                available = [p for p in remaining if p.arrival_time <= current_time]
                
                if not available:
                    current_time = min(p.arrival_time for p in remaining)
                    continue
                
                # Select highest priority (lowest number)
                process = min(available, key=lambda p: (p.priority, p.arrival_time))
                remaining.remove(process)
                
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
                process.completion_time = current_time + process.burst_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                
                gantt_chart.append({
                    'pid': process.pid,
                    'start': current_time,
                    'end': process.completion_time
                })
                
                current_time = process.completion_time
                completed.append(process)
        else:
            # Preemptive priority
            gantt_chart = []
            current_time = 0
            completed = []
            remaining = processes.copy()
            current_process = None
            
            while remaining or current_process:
                available = [p for p in remaining if p.arrival_time <= current_time]
                if current_process:
                    available.append(current_process)
                
                if not available:
                    current_time = min(p.arrival_time for p in remaining)
                    continue
                
                process = min(available, key=lambda p: (p.priority, p.arrival_time))
                
                if process != current_process:
                    if current_process and len(gantt_chart) > 0:
                        gantt_chart[-1]['end'] = current_time
                    current_process = process
                    if process in remaining:
                        remaining.remove(process)
                    if process.start_time == -1:
                        process.start_time = current_time
                        process.response_time = current_time - process.arrival_time
                    gantt_chart.append({
                        'pid': process.pid,
                        'start': current_time,
                        'end': current_time
                    })
                
                current_time += 1
                process.remaining_time -= 1
                
                if process.remaining_time == 0:
                    gantt_chart[-1]['end'] = current_time
                    process.completion_time = current_time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    completed.append(process)
                    current_process = None
        
        metrics = Scheduler.calculate_metrics(completed)
        return gantt_chart, metrics
    
    @staticmethod
    def mlq(processes: List[Process], time_quantums: List[int] = [2, 4]) -> Tuple[List[Dict], Dict]:
        """Multi-Level Queue scheduling"""
        processes = copy.deepcopy(processes)
        
        # Separate processes by queue level
        queues = {}
        for process in processes:
            level = process.queue_level
            if level not in queues:
                queues[level] = []
            queues[level].append(process)
        
        gantt_chart = []
        current_time = 0
        all_completed = []
        
        # Process queues in order (0 = highest priority)
        for level in sorted(queues.keys()):
            queue_processes = queues[level]
            tq = time_quantums[level] if level < len(time_quantums) else time_quantums[-1]
            
            # Simulate Round Robin for this queue
            queue = []
            remaining = sorted(queue_processes, key=lambda p: p.arrival_time)
            completed = []
            
            # Adjust arrival times relative to current_time
            for p in remaining:
                if p.arrival_time < current_time:
                    p.arrival_time = current_time
            
            while remaining or queue:
                # Add newly arrived processes to queue
                while remaining and remaining[0].arrival_time <= current_time:
                    queue.append(remaining.pop(0))
                
                if not queue:
                    if remaining:
                        current_time = remaining[0].arrival_time
                    continue
                
                process = queue.pop(0)
                
                if process.start_time == -1:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                
                # Execute for time quantum or remaining time
                exec_time = min(tq, process.remaining_time)
                start = current_time
                current_time += exec_time
                process.remaining_time -= exec_time
                
                gantt_chart.append({
                    'pid': process.pid,
                    'start': start,
                    'end': current_time
                })
                
                # Add newly arrived processes
                while remaining and remaining[0].arrival_time <= current_time:
                    queue.append(remaining.pop(0))
                
                if process.remaining_time > 0:
                    queue.append(process)
                else:
                    process.completion_time = current_time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    completed.append(process)
            
            all_completed.extend(completed)
        
        metrics = Scheduler.calculate_metrics(all_completed)
        return gantt_chart, metrics
    
    @staticmethod
    def mlfq(processes: List[Process], time_quantums: List[int] = [2, 4, 8]) -> Tuple[List[Dict], Dict]:
        """Multi-Level Feedback Queue scheduling"""
        processes = copy.deepcopy(processes)
        gantt_chart = []
        current_time = 0
        completed = []
        
        # Initialize queues (3 levels by default)
        num_queues = len(time_quantums)
        queues = [[] for _ in range(num_queues)]
        remaining = sorted(processes, key=lambda p: p.arrival_time)
        
        while remaining or any(queues):
            # Add newly arrived processes to top queue
            while remaining and remaining[0].arrival_time <= current_time:
                process = remaining.pop(0)
                process.queue_level = 0
                queues[0].append(process)
            
            # Find highest priority non-empty queue
            current_queue = -1
            for i in range(num_queues):
                if queues[i]:
                    current_queue = i
                    break
            
            if current_queue == -1:
                if remaining:
                    current_time = remaining[0].arrival_time
                continue
            
            process = queues[current_queue].pop(0)
            
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute for time quantum or remaining time
            tq = time_quantums[current_queue]
            exec_time = min(tq, process.remaining_time)
            start = current_time
            current_time += exec_time
            process.remaining_time -= exec_time
            
            gantt_chart.append({
                'pid': process.pid,
                'start': start,
                'end': current_time
            })
            
            # Add newly arrived processes
            while remaining and remaining[0].arrival_time <= current_time:
                new_process = remaining.pop(0)
                new_process.queue_level = 0
                queues[0].append(new_process)
            
            if process.remaining_time > 0:
                # Move to lower priority queue
                next_level = min(current_queue + 1, num_queues - 1)
                process.queue_level = next_level
                queues[next_level].append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed.append(process)
        
        metrics = Scheduler.calculate_metrics(completed)
        return gantt_chart, metrics
