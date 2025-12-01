# Algorithm definitions for calenderization simulation
# processes are defined as simple python lists, no additional classes needed to manipulate them for our use

def FCFS(processes):
    """First-Come, First-Served scheduling algorithm"""
    # sorts list by the arrival time (attribute is found within the class itself)
    processes.sort(key=lambda x: x.arrival)
    # to continue cuz i dont want to do this on my laptop
    global_time = 0
    for process in processes:
        # sets the global_time to whatever was last left off
        if global_time < process.arrival:
            global_time = process.arrival
        process.start_time = global_time
        global_time += process.burst
        # finish time is when the process is done executing
        process.finish_time = global_time
        # the standard calcs for turnaround and waiting time
        process.turnaround_time = process.finish_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        continue

# non preemptive algorithm
def SJF(processes):
    """Shortest Job First scheduling algorithm"""
    processes.sort(key=lambda x: x.burst)
    global_time = 0
    for process in processes:
        # sets the global_time to whatever was last left off
        if global_time < process.arrival:
            global_time = process.arrival
        process.start_time = global_time
        global_time += process.burst
        # finish time is when the process is done executing
        process.finish_time = global_time
        # the standard calcs for turnaround and waiting time
        process.turnaround_time = process.finish_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        pass


def SRTF(processes):
    # Make a working copy
    ready = processes.copy()
    global_time = 0

    # main loop
    while ready:
        available = [p for p in ready if p.arrival <= global_time]

        if not available:
            global_time += 1
            continue

        active = min(available, key=lambda p: p.remaining_time)

        # run only 1 unit (preemptive)
        active.remaining_time -= 1
        if active.start_time is None:
            active.start_time = global_time
        global_time += 1

        # finish condition
        if active.remaining_time == 0:
            active.finish_time = global_time
            active.turnaround_time = global_time - active.arrival
            active.waiting_time = active.turnaround_time - active.burst
            ready.remove(active)


def round_robin(processes, quantum):
    time = 0
    queue = processes[:]

    while queue:
        p = queue.pop(0)

        if p.remaining_time > quantum:
            time += quantum
            p.remaining_time -= quantum
            queue.append(p)

        else:
            time += p.remaining_time
            p.remaining_time = 0
            p.turnaround_time = time
            p.waiting_time = p.turnaround_time - p.burst_time


def Priority_NP(processes):
    """Non-preemptive Priority Scheduling"""
    # sort by arrival time first, then priority
    processes.sort(key=lambda p: (p.arrival, p.priority))

    global_time = 0
    completed = []

    # work on a copy because we'll pull processes from it
    ready = processes.copy()
    processes.clear()

    while ready:
        # fukter processes that have arrived
        available = [p for p in ready if p.arrival <= global_time]

        if not available:
            global_time += 1
            continue

        # pick the highest priority (lowest number)
        active = min(available, key=lambda p: p.priority)

        # run the entire burst (non-preemptive)
        if global_time < active.arrival:
            global_time = active.arrival

        active.start_time = global_time
        global_time += active.burst

        active.finish_time = global_time
        active.turnaround_time = active.finish_time - active.arrival
        active.waiting_time = active.turnaround_time - active.burst

        ready.remove(active)
        completed.append(active)

    # restore the list state
    processes.extend(completed)


def Priority_Preemptive(processes):
    """Preemptive Priority Scheduling"""
    global_time = 0

    while processes:
        # discriminate by considering processes that have arrived
        available = [p for p in processes if p.arrival <= global_time]

        if not available:
            global_time += 1
            continue

        # Pick highest priority (lowest priority number)
        active = min(available, key=lambda p: p.priority)

        active.remaining_time -= 1
        global_time += 1

        if active.start_time is None:
            active.start_time = global_time - 1

        # If completed:
        if active.remaining_time == 0:
            active.finish_time = global_time
            active.turnaround_time = global_time - active.arrival
            active.waiting_time = active.turnaround_time - active.burst
            processes.remove(active)
