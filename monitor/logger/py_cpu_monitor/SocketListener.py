
from Monitor import Monitor
import threading
import socket
import sys
import asyncore


def worker():
    print 'This is a thread job'


class SocketListener():

    #monitor = Monitor()
    monitorThread = threading.Thread(target=worker, args=None)

    def __init__(self, monitor = None):
        self.monitor = monitor

    def data(self): # incoming data from the client
        return None

    def startListening(self):
        # data buffer for the incoming data
        bytes  = list() # bytes of size 1024

        # establish the local endpoint for the socked
        # dns.gethostname return the name of the host running the application
        staticPort = 11000
        ipHostInfo = socket.gethostname()
        ipAddress =  socket.gethostbyname(ipHostInfo)
        localEndPoint = ipAddress, staticPort
        print localEndPoint

        # create a TCP/IP socket
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket to the local endpoint and listen for incomming connections
        try:
            max_connections = 10
            listener.bind(localEndPoint)
            listener.listen(max_connections)


            while True:
                print 'Waiting for a connection...'
                handler = listener.accept()
                data = None

                # an incomming connection needs to be processed
                while True:
                    bytes = bytes(1024)
                    bytesRec = handler.rec


        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


    def startMonitoring(self):
        # this...
        print 'Start Monitoring'


    def stopMonitoring(self):
        print 'Stop Monitoring'
        self.monitor.stop()


if __name__ == '__main__':
    sl = SocketListener()
    sl.startListening()
