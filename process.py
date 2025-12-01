# establish class Process to simulate a process in an operating system

class Process:
    """Class definition of a process with an assigned priority, process ID, and user-defined name."""
    def __init__(self, pid, name, priority, burst, arrival):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.burst = burst
        self.arrival = arrival
        
        self.start_time = None
        self.finish_time = None
        self.waiting_time = None
        self.turnaround_time = None
        self.remaining_time = burst
         # example resource requirement
        self.resource_requirement = ["CPU", "DISK"]

    def display_info(self):
        return f"Process ID: {self.pid}, Name: {self.name}, Priority: {self.priority}"
    
    
# what's a good way to establish a resource requirement for these processes?