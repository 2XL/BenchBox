import psutil
import datetime
import os
from GraphiteClient import GraphiteClient


class PerformanceCounter:

    Type = None
    processPid = None
    processPidDynamic = None
    diskPath = None
    isStatic = None
    metricHeader = None

    def __init__(self, type, type_spec, processName):
        print '//constructor:PerformanceCounter {} {} {}'.format(type, type_spec, processName)
        self.Type = type # memory or processes or disk or network
        self.processName = processName
        self.log_file = self.Type + '_append.log'
        self.logger = open(self.log_file, 'w').close() # clear the log file for new session
        graphiteUrl = '10.30.103.95' # has to be ip if we test with lab machines
        graphitePort = 22003
        self.gc = GraphiteClient(graphiteUrl, graphitePort)
        self.gc.initClient()

        if processName == 'OwnCloud':
            isStatic = False
        else:
            isStatic = True

        if type == 'Process' or type == 'Memory':
            self.setProcId()
        if type == 'Disk':
            self.setDiskMonitorPath()

    def setMetricHeader(self, str):
        self.metricHeader = str

    def NextValue(self):
        to_execute = getattr(self, 'do'+self.Type)
        value = to_execute()
        print value
        with open(self.log_file, 'a') as file:
            file.write(value+'\n') # append text
        return value

    def doNetwork(self):
        print 'doNetwork'
        tstamp = datetime.datetime.now().isoformat()
        net_io = psutil.net_io_counters(pernic=True)
        result = ''
        for nic in net_io:
            if nic == self.processName:
                result+= '{} {}'.format(net_io[nic].bytes_sent,  net_io[nic].bytes_recv)
                ts = self.gc.tsNow()
                self.gc.collect(self.metricHeader+'.bytes_sent', net_io[nic].bytes_sent, ts)
                self.gc.collect(self.metricHeader+'.bytes_recv', net_io[nic].bytes_recv, ts)
        return '{} {}'.format(tstamp, result)

    def doProcess(self): # cpu time %
        print 'doProcess'
        tstamp = datetime.datetime.now().isoformat()

        cpu_c = psutil.cpu_count()

        if self.isStatic:
            p = psutil.Process(self.processPid)
        else:
            pids = self.getPidByName()

        if len(pids) == 0:
            return '{} {} {}'.format(tstamp, 0, cpu_c)
        else:
            try:
                p = psutil.Process(pids[0])
                ts = self.gc.tsNow()
                cpu_usage = p.cpu_percent(interval=1)
                self.gc.collect(self.metricHeader+'.cpu_usage', cpu_usage, ts)
                return '{} {} {}'.format(tstamp,cpu_usage ,cpu_c)
            except Exception as e:
                print 'Exception {}'.format(e)
                return '{} {} {}'.format(tstamp, 0,cpu_c)

    def doDisk(self):
        print 'doDisk'
        tstamp = datetime.datetime.now().isoformat()
        ts = self.gc.tsNow()
        disk_usage = psutil.disk_usage('/').used
        self.gc.collect(self.metricHeader+'.disk_usage', disk_usage, ts)
        return '{} {} {}'.format(tstamp, self.get_size(), disk_usage)

    def doMemory(self):
        print 'doMemory'
        tstamp = datetime.datetime.now().isoformat()
        ram_c = psutil.virtual_memory().total
        if self.isStatic:
            p = psutil.Process(self.processPid)
        else:
            pids = self.getPidByName()
        if len(pids) == 0:
            return '{} {} {}'.format(tstamp, 0, ram_c)
        else:
            try:
                p = psutil.Process(pids[0])
                ts = self.gc.tsNow()
                memory_usage = p.memory_info().rss
                self.gc.collect(self.metricHeader+'.memory_usage', memory_usage, ts)
                return '{} {} {}'.format(tstamp, memory_usage, ram_c)
            except Exception as e:
                print 'Exception {}'.format(e)
                return '{} {} {}'.format(tstamp, 0, ram_c)

    def setProcId(self):
        try:
            with open('/tmp/'+self.processName+'.pid', 'r') as f:
                read_data = f.readline().splitlines()[0]
                print read_data
                self.processPid = int(read_data)
        except Exception as e:
            print 'handle exception: {}'.format(e)
        finally:
            print 'how to handle process with the same name?'

    def setDiskMonitorPath(self): # disc usage monitoring dependent
        path = '/stacksync_folder'
        home = os.path.expanduser("~")
        #folder_path = home + '/stacksync_folder'
        if self.processName == 'StackSync':
            path = '/stacksync_folder'
        elif self.processName == 'OwnCloud':
            path = '/owncloud_folder'
        self.diskPath = home + path

    def get_size(self, path = '.'):
        total_size = 0
        try:
            path = self.diskPath
        except:
            print 'diskPath not defined!'
            path = '.'

        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def getPidByName(self):
        if self.processName == 'StackSync':
            procCmd = 'java'
        elif self.processName == 'OwnCloud':
            procCmd = 'owncloudcmd'
        else:
            procCmd = None
        return [p.pid for p in psutil.process_iter() if procCmd in str(p.name)]

    def clearExit(self):
        self.gc.exitClient()


def getPidByName(procCmd = 'java'):
    return [p.pid for p in psutil.process_iter() if procCmd in str(p.name)]


if __name__ == '__main__':
    print 'Test main program returning values'
    home = os.path.expanduser("~")
    folder_path = home + '/stacksync_folder'
    p = getPidByName()
    print p
    print psutil.Process(p[0]).memory_info()
