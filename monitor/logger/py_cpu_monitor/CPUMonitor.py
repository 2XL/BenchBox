

from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import threading
import time


class CPUMonitor(MonitorResource):
    'CPUMonitor class'
    processes = None # list of psutil.Process.iter_proc_list()

    def __init__(self, processes, loggerId, hostname):
        print 'constructor'
        self.processes = processes # string, LinkedList
        self.cpuValues = list() # list of floats
        self.cpuCounter = list() # list of performanceCounter
        self.loggerId = loggerId
        self.hostname = hostname

        process = processes
        #for process in self.processes:
        print 'CPUMonitor:{}'.format(process)
        pc = PerformanceCounter('Process', '% Process Time', process)
        pc.setMetricHeader('{}.{}.{}.{}'.format('benchbox', hostname, process, loggerId, 'cpu'))
        self.cpuCounter.append(pc)
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

        # run netcat here

        # write csv. header
        file.write('{} {} {}'.format('process','timestamp', 'usage'))
        for value in enumerate(self.cpuValues):
            print value
            file.write(str(value[1])+'\n' )
        file.close()
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
        # asume that there is a benchbox database in impala
        sm.execute('use benchbox')
        # create table if not exists

        for value in enumerate(self.cpuValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_cpu values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], self.loggerId, self.hostname)
            # StackSync 2015-09-08T17:35:10.455244 475340800
            # ts,  cpu_usage, cpu_count, logger_id, dummy_hostname
            sm.execute(insert_into_logger)
        sm.quit()



if __name__ == '__main__':
    monitor = CPUMonitor(['StackSync'])
    for x in range(1000):
        monitor.captureValue();
        time.sleep(1) # 1s









