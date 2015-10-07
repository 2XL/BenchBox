
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import threading
import time

class MemoryMonitor(MonitorResource):
    ''
    ramCounter = None # PerformanceCounter
    ramValues = list()

    def __init__(self, processes, loggerId, hostname):
        print 'constructor'
        self.processes = processes # string, LinkedList
        self.ramValues = list() # list {float}
        self.ramCounter = list()
        self.loggerId = loggerId
        self.hostname = hostname

        #for process in self.processes:
        process = processes
        print 'CPUMonitor:{}'.format(process)
        self.ramCounter.append(PerformanceCounter('Memory', 'Available MBytes', process)
                               .setMetricHeader('{}.{}.{}.{}'
                                                .format('benchbox', hostname, process, loggerId, 'ram')))

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
        self.ramCounter.clearExit()

    def pushToLogger(self):
        print 'Store to impala'
        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        # asume that there is a benchbox database in impala
        sm.execute('use benchbox')
        # create table if not exists

        for value in enumerate(self.ramValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_ram values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], self.loggerId, self.hostname)
            # StackSync 2015-09-08T17:35:10.455244 475340800
            # ts, ram_usage, ram_count, logger_id, dummy_hostname
            sm.execute(insert_into_logger)
        sm.quit()


if __name__ == '__main__':
    memory = MemoryMonitor(['StackSync'])
    for x in range(10):
        memory.captureValue();
        time.sleep(1) # 1s
    memory.pushToLogger()


