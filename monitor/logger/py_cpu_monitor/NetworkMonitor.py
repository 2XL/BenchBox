
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading


class NetworkMonitor(MonitorResource):
    ''
    networkCounter = None # PerformanceCounter
    networkValues = list()

    def __init__(self):
        print 'constructor'
        self.networkCounter # Memory, Available MBytes, true
        self.networkValues = list() # list {float}
        self.networkCounter = PerformanceCounter('Network', 'UpAndDown MBytes', True)

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
        for value in enumerate(self.netValues):
            print value
            file.write(str(value[1])+'\n' )
        file.close()


if __name__ == '__main__':
    network = NetworkMonitor()
    for x in range(10):
        network.captureValue();
        print network.networkValues
        threading.sleep(10) # 1s
