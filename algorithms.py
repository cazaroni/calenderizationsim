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
        pass

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
    """Shortest Remaining Time First scheduling algorithm"""
    # more fuckery involved
    global_time = 0
    # while loop since we will probably have to jump back and forth between processes
    while processes:
        available_processes = {p for p in processes if p.arrival <= global_time}

        if not available_processes:
            global_time += 1
            continue

        if available_processes:
            active_process = min(available_processes, key=lambda x: x.remaining_time)
            # do the thing
            active_process.remaining_time -= 1
            global_time += 1
            
            if active_process.remaining_time == 0:
                active_process.finish_time = global_time
                active_process.turnaround_time = active_process.finish_time - active_process.arrival
                active_process.waiting_time = active_process.turnaround_time - active_process.burst
                # pop it bop it 
                processes.remove(active_process)

def RR(processes, quantum):
    """Round Robin scheduling algorithm"""
    example = False