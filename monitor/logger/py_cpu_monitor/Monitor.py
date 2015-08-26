

from MemoryMonitor import MemoryMonitor
from DiskResource import DiskResource
from CPUMonitor import CPUMonitor

from time import sleep




class Monitor:
    def __init__(self):
        self.finish = False # Boolean
        self.interval # int, sleep interval
        self.filename # string
        self.processes # list{string}
        self.resources # list{MonitorResource}

    def ThreadProc(self):
        self.start()

    def start(self):
        self.finish = False
        while not self.finish:
            sleep(self.interval)
            for resource in self.resources:
                resource.caputureValue()

    def stop(self):
        self.finish = True
        for resource in self.resources:
            resource.saveResults(self.filename)

    def prepareMonitoring(self): # attribute setter...
        self.resources = [] # list{MonitorResource}
        self.resources += MemoryMonitor()
        self.resources += DiskResource()
        self.resources += CPUMonitor(self.processes)

        for resource in self.resources: # MonitorResource
            resource.prepareMonitoring()

    def setInterval(self, interval): # int
        self.interval = interval

    def setFilename(self, filename): # string
        self.filename = filename

    def setProcess(self, processes): # list{string}
        self.processes  = processes


    '''
    # test the class

    if __name__ = '__main__':

        monitor = CPUMonitor()
        # t = CPUMonitor.ThreadProc # declare a thread to be monitored
        t.Start() # start monitor the thread
        interval = 12000 # ms
        sleep(interval)
        monitor.end() # tell the monitor to quit



    '''