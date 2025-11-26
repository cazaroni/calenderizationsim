# Algorithm definitions for calenderization simulation
# processes are defined as simple python lists, no additional classes needed to manipulate them for our use

def FCFS(processes):
    """First-Come, First-Served scheduling algorithm"""
    # sorts list by the arrival time (attribute is found within the class itself)
    processes.sort(key=lambda x: x.arrival)
    # to continue cuz i dont want to do this on my laptop



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