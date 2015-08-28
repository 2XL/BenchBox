
from Diagnostics import PerformanceCounter
from MonitorResource import MonitorResource
import os
import threading


class DriveInfo():
    name = None
    IsReady = False
    def __init__(self):
        print ''

    def GetDrives(self):
        print ''

    def name(self):
        return 'c'

    def IsReady(self):
        return True

    def TotalFreeSpace(self):
        return 100



class DiskResource(MonitorResource):
    ''

    allDrives = DriveInfo() # DriveInfo
    diskValues = list() # list {float}

    def __init__(self):
        print 'constructor'

        self.allDrives.GetDrives()

    def prepareMonitoring(self):
        print 'DISK:prepareMonitor'
        self.diskValues = list() # float
        self.diskCounter = PerformanceCounter('Disk', 'Available MBytes', True)

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



if __name__ == '__main__':
    disk = DiskResource()
    for x in range(100):
        disk.captureValue()
        threading.sleep(100)

