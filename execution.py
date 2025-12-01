# execution.py

from process import Process
from algorithms import FCFS, SJF, SRTF, Priority_NP, Priority_Preemptive
from metrics import compute_metrics


def create_processes():
    return [
        Process(pid=1, name="P1", priority=2, burst=5, arrival=0),
        Process(pid=2, name="P2", priority=1, burst=3, arrival=2),
        Process(pid=3, name="P3", priority=3, burst=1, arrival=4),
        Process(pid=4, name="P4", priority=2, burst=7, arrival=6),
    ]


def print_results(processes, results):
    print("\n--- Process Table ---")
    print("PID | Arrival | Burst | Start | Finish | Wait | Turnaround")
    for p in processes:
        print(f"{p.pid:3} | {p.arrival:7} | {p.burst:5} | {p.start_time:5} | "
              f"{p.finish_time:6} | {p.waiting_time:4} | {p.turnaround_time:10}")

    print("\n--- Metrics ---")
    for key, value in results.items():
        print(f"{key}: {value:.2f}")


def pick_algorithm():
    print("\nChoose scheduling algorithm:")
    print("1. FCFS")
    print("2. SJF (Non-preemptive)")
    print("3. SRTF (Preemptive SJF)")
    print("4. Priority (Non-preemptive)")
    print("5. Priority (Preemptive)")

    choice = input("> ").strip()
    return choice


def run_simulation():
    processes = create_processes()
    choice = pick_algorithm()

    if choice == "1":
        FCFS(processes)
        algo_name = "FCFS"
    elif choice == "2":
        SJF(processes)
        algo_name = "SJF"
    elif choice == "3":
        SRTF(processes)
        algo_name = "SRTF"
    elif choice == "4":
        Priority_NP(processes)
        algo_name = "Priority (NP)"
    elif choice == "5":
        Priority_Preemptive(processes)
        algo_name = "Priority (Preemptive)"
    else:
        print("Invalid selection")
        return

    results = compute_metrics(processes)

    print(f"\n=== Results for {algo_name} ===")
    print_results(processes, results)
