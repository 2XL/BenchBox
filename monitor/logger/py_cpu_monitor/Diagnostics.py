import psutil
import datetime
import os


class PerformanceCounter:

    Type = None
    # have a live log appended
    processPid = None # process id to monitor
    diskPath = None # storage directory path


    def __init__(self, type, type_spec, processName):
        print '//constructor:PerformanceCounter {} {} {}'.format(type, type_spec, processName)
        self.Type = type # memory or processes or disk or network
        self.processName = processName
        self.log_file = self.Type + '_append.log'
        self.logger = open(self.log_file, 'w').close() # clear the file
        self.setProcId()
        self.setDiskMonitorPath()

    def NextValue(self):
        to_execute = getattr(self, 'do'+self.Type)
        value = to_execute()
        print value
        with open(self.log_file, 'a') as file:
            file.write(value) # append text
            file.write('\n') # new line
        return value


    def doNetwork(self): # network traffic , in / out  {unit}
        print 'doNetwork'



    def doProcess(self): # cpu time %
        print 'doProcess'
        # en el de cristian se pilla de todos los cores por separado luego se juntan...
        tstamp =  datetime.datetime.now().isoformat()
        return '{} {} {}'.format(self.processName, tstamp, psutil.Process(self.processPid).cpu_percent())


    def doDisk(self): # input output % time {write/read unit}
        print 'doDisk'
        # how to get the hdd usage??
        tstamp =  datetime.datetime.now().isoformat()
        #return '{} {} {}'.format(self.processName, tstamp, psutil.disk_usage('/').percent)

        return '{} {} {}'.format(self.processName, tstamp, self.get_size())



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
        return '{} {} {}'.format(self.processName, tstamp, psutil.Process(self.processPid).memory_percent())


    def setProcId(self): # process and ram monitoring dependent
        # loop through all the process psutil and seek for its pid.
        # for p in psutil.get_process_list():
        #    print 'PID: {}'.format(self.processName)
        try :
            with open('/tmp/'+self.processName+'.pid', 'r') as f:
                read_data = f.read()
                print read_data
                self.processPid = read_data
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


if __name__ == '__main__':
    print 'Test main program returning values'
    home = os.path.expanduser("~")
    folder_path = home + '/stacksync_folder'
    # print 'Size: {} {} '.format(get_size(folder_path), 'Bytes')