
from MonitorResource import MonitorResource

class CPUMonitor(MonitorResource):
    'CPUMonitor class'

    def __init__(self, processes):
        print 'constructor'
        self.cpuValues # float, LinkedList
        self.processes = processes # string, LinkedList
        self.cpuCounter = PerformanceCounter() # PerformanceCounter, LinkedList

















