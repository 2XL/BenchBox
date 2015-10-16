
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import time


class DiskMonitor(MonitorResource):

    diskValues = list()

    def __init__(self, diskPath, loggerId, hostname):
        print 'constructor'
        self.diskValues = list()
        pc = PerformanceCounter('Disk', 'Available MBytes', diskPath)
        pc.setMetricHeader('{}.{}.{}'.format('benchbox', hostname, diskPath, 'hdd'))

        self.diskCounter = pc
        self.loggerId = loggerId
        self.hostname = hostname

    def prepareMonitoring(self):
        print 'DISK:prepareMonitor'
        self.diskValues = list() # float

    def captureValue(self):
        self.diskValues.append(self.diskCounter.NextValue())

    def saveResults(self, filename):
        f = open('disk_' + filename, 'w+')
        for value in enumerate(self.diskValues):
            print value
            f.write(str(value[1])+'\n')
        f.close()
        self.diskCounter.clearExit()

    def pushToLogger(self):
        print 'Store to impala'
        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        sm.execute('use benchbox')
        for value in enumerate(self.diskValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_hdd values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], self.loggerId, self.hostname)
            sm.execute(insert_into_logger)
        sm.quit()

if __name__ == '__main__':
    disk = DiskMonitor('stacksync_folder')
    for x in range(100):
        disk.captureValue()
        time.sleep(2)

