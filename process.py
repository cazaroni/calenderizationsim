# establish class Process to simulate a process in an operating system

class Process:
    """Class definition of a process with an assigned priority, process ID, and user-defined name."""
    def __init__(self, pid, name, priority):
        self.pid = pid
        self.name = name
        self.priority = priority

    resource_requirement = None
    def display_info(self):
        return f"Process ID: {self.pid}, Name: {self.name}, Priority: {self.priority}"
    
    
# what's a good way to establish a resource requirement for these processes?