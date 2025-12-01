def compute_metrics(processes):
    # Filter out any processes that never actually ran
    completed = [p for p in processes if p.finish_time is not None]

    if not completed:
        raise ValueError("No completed processes; the algorithm didn't run correctly.")

    n = len(completed)

    avg_wait = sum(p.waiting_time for p in completed) / n
    avg_turn = sum(p.turnaround_time for p in completed) / n
    avg_resp = sum((p.start_time - p.arrival) for p in completed) / n

    total_burst = sum(p.burst for p in completed)
    makespan = max(p.finish_time for p in completed)
    cpu_util = total_burst / makespan

    return {
        "avg_waiting_time": avg_wait,
        "avg_turnaround_time": avg_turn,
        "avg_response_time": avg_resp,
        "cpu_utilization": cpu_util,
    }
