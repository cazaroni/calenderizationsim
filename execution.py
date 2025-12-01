# execution.py

from process import Process
from algorithms import FCFS, SJF, SRTF, Priority_NP, Priority_Preemptive, Round_Robin
from metrics import compute_metrics


def create_processes():
    # ask the user to define a process (once at a time)
    processes = []
    while True:
        print("\nDefine a new process, or type 'done' to finish:")
        name = input("Process name: ").strip()
        if name.lower() == 'done':
            break
        try:
            pid = len(processes) + 1
            priority = int(input("Priority (lower number = higher priority): ").strip())
            burst = int(input("Burst time (CPU time required): ").strip())
            arrival = int(input("Arrival time: ").strip())
        except ValueError:
            print("Invalid input. Please enter numeric values for priority, burst time, and arrival time.")
            continue

        process = Process(pid=pid, name=name, priority=priority, burst=burst, arrival=arrival)
        processes.append(process)
        print(f"Process {name} added.")
    
    return processes

def lazy_processes():
    """
    for running tests quickly
    """
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
def main_menu():
    """
    Simple looped main menu that doesn't lose any local states for processes and results
    """
    processes = []
    results = {}
    while True:
        print("\n--- Main Menu ---")
        print("1. Create Processes")
        print("2. Select Scheduling Algorithm and Run Simulation")
        print("3. Show results")
        print("4. Skidaddle")
        print("5. (Hidden) Load Lazy Test Processes")

        menu_choice = input("> ").strip()

        if menu_choice == "1":
            processes = create_processes()
            continue
        elif menu_choice == "2":
            # if someone decides to not create a list of processes, we kick them out
            proc_res = run_simulation(processes if processes else None)
            if proc_res:
                processes, results = proc_res
            continue
        elif menu_choice == "3":
            if not processes:
                print("No processes available. Create processes first (option 1) or run a simulation (option 2).")
            elif not results:
                print("No results available. Run a simulation first (option 2).")
            else:
                print_results(processes, results)
            continue
        elif menu_choice == "4":
            print("Exiting.")
            return
        elif menu_choice == "5":
            processes = lazy_processes()
            print("Lazy test processes have been loaded for you, lazyass")
            continue
        else:
            print("Invalid selection")
            continue



def pick_algorithm():
    print("\nChoose scheduling algorithm:")
    print("1. FCFS")
    print("2. SJF (Non-preemptive)")
    print("3. SRTF (Preemptive SJF)")
    print("4. Priority (Non-preemptive)")
    print("5. Priority (Preemptive)")
    print("6. Round Robin (quantum=2)")

    choice = input("> ").strip()
    return choice


def run_simulation(processes=None):
    """
    Run simulation on provided processes or prompt to create them if None.
    Returns a tuple (processes, results) on success, or (None, None) on invalid selection.
    """
    if processes is None:
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
    elif choice == "6":
        # example for round robin with quantum 2
        Round_Robin(processes, quantum=2)
        algo_name = "Round Robin (quantum=2)"
    else:
        print("Invalid selection")
        return None, None

    results = compute_metrics(processes)

    print(f"\n=== Results for {algo_name} ===")
    print_results(processes, results)
    return processes, results
