
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import time
import threading


class NetworkMonitor(MonitorResource):
    ''
    networkCounter = None # PerformanceCounter
    networkValues = list()

    def __init__(self, nic):
        print 'constructor'
        self.networkCounter # Memory, Available MBytes, true
        self.networkValues = list() # list {float}
        self.networkCounter = PerformanceCounter('Network', 'UpAndDown bytes', nic)

    def prepareMonitoring(self):
        print 'NET:prepareMonitor'
        self.networkValues = list() # Floats

    def captureValue(self):
        self.networkValues.append(self.networkCounter.NextValue())

    def saveResults(self, filename):
        # open a file
        file = open('net_' + filename, 'w+') # maybe it has to be append instead of crete and
        # write
        '''
        os.write(file, str(os.getpid()))
        for it in self.ramValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        '''
        for value in enumerate(self.networkValues):
            print value
            file.write(str(value[1])+'\n' )
        file.close()


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

        for value in enumerate(self.networkValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_net values ('{}', '{}', '{}', {})".format(items[1], 'Memory', items[0], items[2])
            # StackSync 2015-09-08T17:35:10.455244 475340800
            sm.execute(insert_into_logger)
        sm.quit()

if __name__ == '__main__':
    network = NetworkMonitor('eth0')
    for x in range(10):
        network.captureValue();
        network.networkValues[len(network.networkValues)-1]
        time.sleep(1) # 1s
