import psutil




class PerformanceCounter:

    Type = None


    def __init__(self, type, spec, bool):
        print '//constructor:PerformanceCounter'
        self.Type = type # memory or processes or disk or network


    def NextValue(self):
        to_execute = getattr(self, 'do'+self.Type)
        to_execute()


    def doNetwork(self): # network traffic , in / out  {unit}
        print 'doNetwork'


    def doProcesses(self): # cpu time %
        print 'doProcesses'


    def doDisk(self): # input output % time {write/read unit}
        print 'doDisk'


    def doMemory(self): # % memory usage : {units/%}
        print 'doMemory'




if __name__ == '__main__':
    print 'Test main program returning values'