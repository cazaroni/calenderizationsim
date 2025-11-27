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


def SJF(processes):
    """Shortest Job First scheduling algorithm"""
    processes.sort(key=lambda x: x.burst)
    example = False


def SRTF(processes):
    """Shortest Remaining Time First scheduling algorithm"""
    example = False

def RR(processes, quantum):
    """Round Robin scheduling algorithm"""
    example = False