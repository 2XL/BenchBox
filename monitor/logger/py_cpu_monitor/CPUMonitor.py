

from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading


class CPUMonitor(MonitorResource):
    'CPUMonitor class'
    processes = None # list of psutil.Process.iter_proc_list()

    def __init__(self, processes):
        print 'constructor'
        self.cpuValues = None# float, LinkedList
        self.processes = processes # string, LinkedList
        self.cpuCounter = None # PerformanceCounter, LinkedList


    # vale hay processes porque lo implementan para cada personal cloud. pero eso no deberia afectar el traffico??? nose

    def prepareMonitoring(self):
        print 'CPU:prepareMonitor'
        self.cpuValues = list() # list of floats
        self.cpuCounter = list() # list of performanceCounter

        for process in self.processes:
            self.cpuCounter.append(PerformanceCounter('Process', '% Process Time', process))


    def captureValue(self):
        cpu = 0;
        for counter in self.cpuCounter: # counter is  PerformanceCounter
            cpu += counter.NextValue()
        self.cpuValues.AddLast(cpu)



    def saveResults(self, filename):
        # open a file
        file = os.open('cpu_' + filename, os.O_APPEND|os.O_CREAT) # maybe it has to be append instead of crete and write
        os.write(file, str(os.getpid()))
        for it in self.cpuValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        os.close(file)

    def setProcess(self, processes):
        self.processes = processes




if __name__ == '__main__':
    monitor = CPUMonitor()
    t = threading.Thread()
    t.start()
    threading.sleep(1) # 1s
    monitor.end()









