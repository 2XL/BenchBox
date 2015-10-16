
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import threading
import time

class MemoryMonitor(MonitorResource):
    ramCounter = None
    ramValues = list()

    def __init__(self, processes, loggerId, hostname):
        print 'constructor'
        self.processes = processes
        self.ramValues = list()
        self.ramCounter = list()
        self.loggerId = loggerId
        self.hostname = hostname

        process = processes
        print 'CPUMonitor:{}'.format(process)
        pc = PerformanceCounter('Memory', 'Available MBytes', process)
        pc.setMetricHeader('{}.{}.{}'.format('benchbox', hostname, process, 'ram'))
        self.ramCounter.append(pc)


    def prepareMonitoring(self):
        print 'RAM:prepareMonitor'
        self.ramValues = list() # Floats

    def captureValue(self):
        for counter in self.ramCounter:
            ram = counter.NextValue()
            self.ramValues.append(ram)

    def saveResults(self, filename):

        f = open('mem_' + filename, 'w+')

        for value in enumerate(self.ramValues):
            print value
            f.write(str(value[1])+'\n')
        f.close()
        self.ramCounter.clearExit()

    def pushToLogger(self):
        print 'Store to impala'
        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        sm.execute('use benchbox')

        for value in enumerate(self.ramValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_ram values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], self.loggerId, self.hostname)
            sm.execute(insert_into_logger)
        sm.quit()


if __name__ == '__main__':
    memory = MemoryMonitor(['StackSync'])
    for x in range(10):
        memory.captureValue();
        time.sleep(1)
    memory.pushToLogger()


