import psutil
import datetime
import os


class PerformanceCounter:

    Type = None
    # have a live log appended
    processPid = None # process id to monitor
    processPidDynamic = None #
    diskPath = None # storage directory path
    isStatic = None

    def __init__(self, type, type_spec, processName):
        print '//constructor:PerformanceCounter {} {} {}'.format(type, type_spec, processName)
        self.Type = type # memory or processes or disk or network
        self.processName = processName
        self.log_file = self.Type + '_append.log'
        self.logger = open(self.log_file, 'w').close() # clear the log file for new session

        #if processName == 'StackSync':
        if processName == 'OwnCloud':
            isStatic = False
        else: # default they are static pid deamons
            isStatic = True


        if type == 'Process' or type == 'Memory':
            self.setProcId()
        if type == 'Disk':
            self.setDiskMonitorPath()

    def NextValue(self):
        to_execute = getattr(self, 'do'+self.Type)

        value = to_execute()
        print value
        with open(self.log_file, 'a') as file:
            file.write(value+'\n') # append text
        return value


    def doNetwork(self): # network traffic , in / out  {unit}
        print 'doNetwork'
        tstamp =  datetime.datetime.now().isoformat()
        net_io = psutil.net_io_counters(pernic=True)
        result=''
        for nic in net_io:
            if nic == self.processName:
                result+= '{} {}'.format(net_io[nic].bytes_sent,  net_io[nic].bytes_recv)

        return '{} {}'.format(tstamp, result)


    def doProcess(self): # cpu time %
        print 'doProcess'
        # en el de cristian se pilla de todos los cores por separado luego se juntan...
        tstamp =  datetime.datetime.now().isoformat()
        #print self.processPid

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
                return '{} {} {}'.format(tstamp, p.cpu_percent(interval=1),cpu_c)
            except Exception as e:
                print 'Exception {}'.format(e)
                return '{} {} {}'.format(tstamp, 0,cpu_c)


    def doDisk(self): # input output % time {write/read unit}
        print 'doDisk'
        # how to get the hdd usage??
        tstamp =  datetime.datetime.now().isoformat()
        #return '{} {} {}'.format(self.processName, tstamp, psutil.disk_usage('/').percent)

        return '{} {} {}'.format(tstamp, self.get_size(), psutil.disk_usage('/').used)



    def doMemory(self): # % memory usage : {units/%}
        print 'doMemory'
        # how to get the ram usage with psutil???
        #total = psutil.virtual_memory().total
        #active = psutil.virtual_memory().active
        #print active
        #print total
        #percent = (active*100/total)
        # todo check static process id generated by the stacksync or owncloud client and located at path /tmp/s.pid
        # overhead a reading a file... each time, should defined at class atribute level.
        tstamp =  datetime.datetime.now().isoformat()

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
                return '{} {} {}'.format(tstamp, p.memory_info().rss, ram_c)
            except Exception as e:
                print 'Exception {}'.format(e)
                return '{} {} {}'.format(tstamp, 0, ram_c)
        # rss : Resident set size


    def setProcId(self): # process and ram monitoring dependent
        # loop through all the process psutil and seek for its pid.
        # for p in psutil.get_process_list():
        #    print 'PID: {}'.format(self.processName)
        try :
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
        if self.processName  == 'StackSync':
            procCmd = 'java'
        elif self.processName == 'OwnCloud':
            procCmd = 'owncloudcmd'
        else:
            procCmd = None
        return [p.pid for p in psutil.process_iter() if procCmd in str(p.name)]

def getPidByName(procCmd = 'java'):
    return [p.pid for p in psutil.process_iter() if procCmd in str(p.name)]

if __name__ == '__main__':
    print 'Test main program returning values'
    home = os.path.expanduser("~")
    folder_path = home + '/stacksync_folder'
    # print 'Size: {} {} '.format(get_size(folder_path), 'Bytes')
    p =  getPidByName()
    print p
    print psutil.Process(p[0]).memory_info()
