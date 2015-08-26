
from MonitorResource import MonitorResource


class MemoryMonitor(MonitorResource):
    ''
    ramCounter = None # PerformanceCounter
    ramValues = list()

    def __init__(self):
        print 'constructor'
        self.ramCounter # Memory, Available MBytes, true

    def prepareMonitoring(self):
        self.ramValues = list()

    def captureValue(self):
        self.ramValues += ramCounter.NextValue()
