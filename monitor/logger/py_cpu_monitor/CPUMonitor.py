

from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading
import time


class CPUMonitor(MonitorResource):
    'CPUMonitor class'
    processes = None # list of psutil.Process.iter_proc_list()

    def __init__(self, processes):
        print 'constructor'
        self.processes = processes # string, LinkedList
        self.cpuValues = list() # list of floats
        self.cpuCounter = list() # list of performanceCounter
        for process in self.processes:
            print 'CPUMonitor:{}'.format(process)
            self.cpuCounter.append(PerformanceCounter('Process', '% Process Time', process))
    # vale hay processes porque lo implementan para cada personal cloud. pero eso no deberia afectar el traffico??? nose

    def prepareMonitoring(self):
        print 'CPU:prepareMonitor'
        self.cpuValues = list() # list of floats


    def captureValue(self):
        for counter in self.cpuCounter: # counter is  PerformanceCounter
            cpu = counter.NextValue()
            self.cpuValues.append(cpu) # todo: has to be refactored



    def saveResults(self, filename):
        # open a file
        file = open('cpu_' + filename, 'w+') # maybe it has to be append instead of crete and write

        '''
        for it in self.cpuValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        '''
        # write csv. header
        file.write('{} {} {}'.format('process','timestamp', 'usage'))
        for value in enumerate(self.cpuValues):
            print value
            file.write(str(value[1])+'\n' )
        file.close()

    def setProcess(self, processes):
        self.processes = processes




if __name__ == '__main__':
    monitor = CPUMonitor(['StackSync'])
    for x in range(1000):
        monitor.captureValue();
        time.sleep(1) # 1s









