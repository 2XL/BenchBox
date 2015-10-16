

from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import threading
import time


class CPUMonitor(MonitorResource):
    processes = None

    def __init__(self, processes, loggerId, hostname):
        print 'constructor'
        self.processes = processes
        self.cpuValues = list()
        self.cpuCounter = list()
        self.loggerId = loggerId
        self.hostname = hostname

        process = processes
        print 'CPUMonitor:{}'.format(process)
        pc = PerformanceCounter('Process', '% Process Time', process)
        pc.setMetricHeader('{}.{}.{}'.format('benchbox', hostname, process, 'cpu'))
        self.cpuCounter.append(pc)

    def prepareMonitoring(self):
        print 'CPU:prepareMonitor'
        self.cpuValues = list()

    def captureValue(self):
        for counter in self.cpuCounter:
            cpu = counter.NextValue()
            self.cpuValues.append(cpu)

    def saveResults(self, filename):
        f = open('cpu_' + filename, 'w+')

        f.write('{} {} {}'.format('process', 'timestamp', 'usage'))
        for value in enumerate(self.cpuValues):
            print value
            f.write(str(value[1])+'\n')
        f.close()
        self.cpuCounter.clearExit()

    def setProcess(self, processes):
        self.processes = processes

    def pushToLogger(self):
        print 'Store to impala'
        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        sm.execute('use benchbox')

        for value in enumerate(self.cpuValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_cpu values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], self.loggerId, self.hostname)
            sm.execute(insert_into_logger)
        sm.quit()

if __name__ == '__main__':
    monitor = CPUMonitor(['StackSync'])
    for x in range(1000):
        monitor.captureValue();
        time.sleep(1) # 1s









