
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
from StoreManager import StoreManager
import os
import threading
import time



class DiskMonitor(MonitorResource):
    ''

    diskValues = list() # list {float}

    def __init__(self, diskPath):
        print 'constructor'
        self.diskValues = list() # float
        self.diskCounter = PerformanceCounter('Disk', 'Available MBytes', diskPath)

    def prepareMonitoring(self):
        print 'DISK:prepareMonitor'
        self.diskValues = list() # float

    def captureValue(self):
        self.diskValues.append(self.diskCounter.NextValue())
        '''
        for d in self.allDrives: # DriveInfo
            if 'c' in d.Name: # en aquest cas ... xD ke faig???
                print 'success'
            if d.IsReady == True:
                self.diskValues.AddLast(d.TotalFreeSpace)
        '''
    def saveResults(self, filename):
        # open a file
        file = open('disk_' + filename, 'w+') # maybe it has to be append instead of crete and
        # write
        '''
        for it in self.diskValues: # float iterator
            while it:
                os.write(file, it.pop(1))
        '''
        for value in enumerate(self.diskValues):
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

        for value in enumerate(self.diskValues):
            print value
            items = value[1].split(' ')
            insert_into_logger = "insert into logger_hdd values ('{}', {}, {}, '{}', '{}')" \
                .format(items[0], items[1], items[2], items[3], items[4])
            # StackSync 2015-09-08T17:35:10.455244 475340800
            # ts,  data_write, data_read, logger_id, dummy_hostname
            sm.execute(insert_into_logger)



        sm.quit()


if __name__ == '__main__':
    disk = DiskMonitor('stacksync_folder')
    for x in range(100):
        disk.captureValue()
        time.sleep(2)

