import psutil




class PerformanceCounter:

    Type = None


    def __init__(self, type, spec, bool):
        print '//constructor:PerformanceCounter'
        self.Type = type # memory or processes or disk or network


    def NextValue(self):
        to_execute = getattr(self, 'do'+self.Type)
        value = to_execute()
        print value
        return value


    def doNetwork(self): # network traffic , in / out  {unit}
        print 'doNetwork'



    def doProcess(self): # cpu time %
        print 'doProcess'
        # en el de cristian se pilla de todos los cores por separado luego se juntan...
        return psutil.cpu_percent(interval=None, percpu=False)


    def doDisk(self): # input output % time {write/read unit}
        print 'doDisk'
        # how to get the hdd usage??
        return psutil.disk_usage('/').percent



    def doMemory(self): # % memory usage : {units/%}
        print 'doMemory'
        # how to get the ram usage with psutil???
        #total = psutil.virtual_memory().total
        #active = psutil.virtual_memory().active
        #print active
        #print total
        #percent = (active*100/total)
        return psutil.virtual_memory().percent




if __name__ == '__main__':
    print 'Test main program returning values'