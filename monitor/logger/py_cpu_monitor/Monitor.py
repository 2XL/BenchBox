

from MemoryMonitor import MemoryMonitor
from DiskMonitor import DiskMonitor
from CPUMonitor import CPUMonitor
from NetworkMonitor import NetworkMonitor
from time import sleep
from PcapCapture import pcap_capture
from time import time
from StoreManager import StoreManager


class Monitor:

    def __init__(self):
        self.finish = False # Boolean
        self.interval = None# int, sleep interval
        self.filename = None# string
        self.processes = None# list{string}
        self.resources = None# list{MonitorResource}
        self.pcapCapturer = pcap_capture('eth0')
        self.pcapCapturer.daemon = True
        self.logger_id = None

    def ThreadProc(self):
        print 'Started/ThreadProc'
        self.start()

    def start(self):
        print 'Started/MonitorCapture {}'.format((self.interval, self.resources, self.filename))

        self.pcapCapturer.start()
        self.finish = False

        while not self.finish:
            print 'sleep:{}'.format(self.interval)
            for resource in self.resources:
                resource.captureValue()
            sleep(self.interval)

    def stop(self):
        print 'Stop/MonitorCapture {}'
        self.finish = True
        if self.resources is None:
            print 'Not Monitoring Anything...'
        else:
            for resource in self.resources:
                resource.pushToLogger()

        while not self.pcapCapturer.stop(): pass

        self.pcapCapturer.join()
        self.pcapCapturer.pcap_dumper.dumpToImpala(self.pcapCapturer.dumper_list)


    def prepareMonitoring(self): # attribute setter...

        print 'Monitor:prepareMonitoring'
        self.resources = list() # list{MonitorResource}


        if self.processes == 'StackSync':
            folder_sync_client = 'stacksync_folder'

        if self.processes == 'OwnCloud':
            folder_sync_client = 'owncloud_folder'

        print "loggerId: ".format(self.logger_id)

        self.resources.append(MemoryMonitor(self.processes, self.logger_id, self.hostname))
        self.resources.append(DiskMonitor(folder_sync_client, self.logger_id, self.hostname))
        self.resources.append(CPUMonitor(self.processes, self.logger_id, self.hostname))
        self.resources.append(NetworkMonitor('eth0', self.logger_id, self.hostname))
        self.pcapCapturer = pcap_capture()

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

    def setLoggerId(self, dummy_hostname, pc_server_name, profile, test_definition):
        self.logger_id = time()
        self.hostname = dummy_hostname
        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        sm.execute('use benchbox')

        insert_into_logger = "insert into logger_id values ('{}', '{}', '{}', '{}', '{}')" \
                .format(self.logger_id, dummy_hostname, pc_server_name, profile, test_definition)
        sm.execute(insert_into_logger)
        sm.quit()

if __name__ == '__main__':

    monitor = CPUMonitor()
    # t = CPUMonitor.ThreadProc # declare a thread to be monitored
    t.Start() # start monitor the thread
    interval = 12000 # ms
    sleep(interval)
    monitor.end() # tell the monitor to quit


