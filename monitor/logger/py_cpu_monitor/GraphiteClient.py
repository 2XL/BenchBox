import time
import socket
import random
#import wget
import urllib2
import json

class GraphiteClient():
    def __init__(self, host='localhost', portstr=22003, portpickle=22004):
        self.hostname = host
        self.portstr = portstr
        self.portpickle = portpickle
        self.session = None

    def collect_string(self, name, value, timestamp):
        sock = socket.socket()
        sock.connect((self.hostname, self.portstr))
        sock.send("%s %s %d\n" % (name, value, timestamp))

        sock.close()

    def collect_pickle(self, name, value, timestamp):
        sock = socket.socket()
        sock.connect((self.hostname, self.portpickle))
        sock.send("%s %d %d\n" % (name, value, timestamp))
        sock.close()

    def initClient(self):
        self.session = socket.socket()
        self.session.connect((self.hostname, self.portstr))

    def exitClient(self):
        self.session.close()

    def collect(self, name, value, ts):
        str = '{} {} {}\n'.format(name, value, ts)
        print str
        self.session.send(str)



    def tsNow(self):
        return int(time.time())

    def strDate(self):
        return time.strftime("%H:%M:%S")

    def randValue(self):
        return random.randint(0, 100)
