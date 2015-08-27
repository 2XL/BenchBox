

from MemoryMonitor import MemoryMonitor
from DiskResource import DiskResource
from CPUMonitor import CPUMonitor

from time import sleep




class Monitor:
    def __init__(self):
        self.finish = False # Boolean
        self.interval = None# int, sleep interval
        self.filename = None# string
        self.processes = None# list{string}
        self.resources = None# list{MonitorResource}

    def ThreadProc(self): # aquesta funcio bucle infinit en un thread...
        print 'Started/ThreadProc'
        self.start()

    def start(self):
        print 'Started/MonitorCapture {}'.format((self.interval, self.resources, self.filename))
        self.finish = False
        while not self.finish:
            print 'sleep:{}'.format(self.interval)
            for resource in self.resources:
                print 'captureValue:{}'.format(resource)
                resource.captureValue()
            sleep(self.interval)

    def stop(self):
        self.finish = True
        for resource in self.resources:
            resource.saveResults(self.filename)

    def prepareMonitoring(self): # attribute setter...
        print 'Monitor:prepareMonitoring'
        self.resources = list() # list{MonitorResource}
        self.resources.append(MemoryMonitor())
        self.resources.append(DiskResource())
        self.resources.append(CPUMonitor(self.processes))
        x=0
        for resource in self.resources: # MonitorResource
            x+=1
            print x
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