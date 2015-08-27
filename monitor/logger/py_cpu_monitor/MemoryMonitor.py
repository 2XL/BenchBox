
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading


class MemoryMonitor(MonitorResource):
    ''
    ramCounter = None # PerformanceCounter
    ramValues = list()

    def __init__(self):
        print 'constructor'
        self.ramCounter # Memory, Available MBytes, true
        self.ramValues = list() # list {float}
        self.ramCounter = PerformanceCounter('Memory', 'Available MBytes', True)

    def prepareMonitoring(self):
        print 'RAM:prepareMonitor'
        self.ramValues = list() # Floats

    def captureValue(self):

        self.ramValues.append(self.ramCounter.NextValue())

    def saveResults(self, filename):
        # open a file
        file = os.open('mem_' + filename, os.O_APPEND|os.O_CREAT) # maybe it has to be append instead of crete and
        # write
        os.write(file, str(os.getpid()))
        for it in self.ramValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        os.close(file)


if __name__ == '__main__':
    memory = MemoryMonitor()
    for x in range(1000):
        memory.captureValue();
        threading.sleep(10) # 1s


