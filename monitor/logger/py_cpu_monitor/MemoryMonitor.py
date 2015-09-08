
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading
import time

class MemoryMonitor(MonitorResource):
    ''
    ramCounter = None # PerformanceCounter
    ramValues = list()

    def __init__(self, processes):
        print 'constructor'
        self.processes = processes # string, LinkedList
        self.ramValues = list() # list {float}
        self.ramCounter = list()
        for process in self.processes:
            print 'CPUMonitor:{}'.format(process)
            self.ramCounter.append(PerformanceCounter('Memory', 'Available MBytes', process))

    def prepareMonitoring(self):
        print 'RAM:prepareMonitor'
        self.ramValues = list() # Floats

    def captureValue(self):
        for counter in self.ramCounter: # counter is  PerformanceCounter
            ram = counter.NextValue()
            self.ramValues.append(ram) # todo: has to be refactored

    def saveResults(self, filename):
        # open a file
        file = open('mem_' + filename, 'w+') # maybe it has to be append instead of crete and
        # write
        '''
        os.write(file, str(os.getpid()))
        for it in self.ramValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        '''
        for value in enumerate(self.ramValues):
            print value
            file.write(str(value[1])+'\n' )
        file.close()


if __name__ == '__main__':
    memory = MemoryMonitor(['StackSync'])
    for x in range(1000):
        memory.captureValue();
        time.sleep(1) # 1s


