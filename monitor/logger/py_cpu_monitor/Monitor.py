

from MemoryMonitor import MemoryMonitor
from DiskMonitor import DiskMonitor
from CPUMonitor import CPUMonitor
from NetworkMonitor import NetworkMonitor
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
                # print 'captureValue:{}'.format(resource)

                resource.captureValue()
                '''
                todo: refactor to none blocking, instead of blocking, due to cpu_percentatge and network bandwidth
                capture
                '''
            sleep(self.interval)

    def stop(self):
        print 'Stop/MonitorCapture {}'
        self.finish = True
        if self.resources is None:
            print 'Not Monitoring Anything...'
        else:
            for resource in self.resources:
                #resource.saveResults(self.filename)
                # print 'saveResults({})'.format(resource)
                resource.pushToLogger()



    def prepareMonitoring(self): # attribute setter...

        print 'Monitor:prepareMonitoring'
        self.resources = list() # list{MonitorResource}


        if self.processes[0] == 'StackSync':
            folder_sync_client = 'stacksync_folder'

        if self.processes[0] == 'OwnCloud':
            folder_sync_client = 'owncloud_folder'


        self.resources.append(MemoryMonitor(self.processes))
        self.resources.append(DiskMonitor(folder_sync_client))
        self.resources.append(CPUMonitor(self.processes))
        self.resources.append(NetworkMonitor('eth0'))

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
        self.processes = processes


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