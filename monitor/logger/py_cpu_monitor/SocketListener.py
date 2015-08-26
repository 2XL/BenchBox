
from Monitor import Monitor
import threading
import socket
import sys
import asyncore
import time
import SocketServer, subprocess

HOST = ''
PORT = 11000


def worker():
    print 'This is a thread job'



# http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/, THIS IS TO BE DONE TOMMOROW

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

        # bind the socket to the local endpoint and
        # listen for incoming connections.
        try:
            max_connections = 10
            listener.bind(localEndPoint)
            listener.listen(max_connections)

            # start listening for connections
            while True:
                print 'Waiting for a connection...'
                conn, client_addr = listener.accept()
                print 'Connection from: {}'.format(client_addr)
                dataBuffer = []
                while True:
                    data = conn.recv(1024)
                    if '<EOF>' not in data:
                        print 'recv: {}'.format(data)
                        # send back data to client
                        conn.sendall(data)
                    else:

                        print 'recv: {} END'.format(data)
                        break
                    dataBuffer.append(str(data))
                    time.sleep(1)

                print 'Text recv: {}'.format(dataBuffer)

                print 'dataBuffer'
                print dataBuffer

                if 'start' in dataBuffer:
                    print 'StartMonitoring'
                    # self.startMonitoring()
                elif 'stop' in dataBuffer:
                    print 'StopMonitoring'
                    self.stopMonitoring()
                        # an incomming connection needs to be processed
                #while True:
                #    bytes = listener.recv(1024)
                #    print bytes

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        finally:
            # clean up the connection
            listener.close()



        print 'SocketListener, QUIT!'


    def startMonitoring(self, command):
        # this...
        print 'Start Monitoring'
        # start monitoring a specific process
        command = command.replace('<EOF>', '')
        parameters = command.split(' ')
        interval = int(parameters[1])
        filename = str(parameters[2])
        processes = list()

        for i in range(3, len(parameters)):
            processes.append(parameters[i])

        self.monitor.setInterval(interval)
        self.monitor.setFilename(filename)
        self.monitor.setProcess(processes)
        self.monitor.prepareMonitoring()

        self.monitorThread = threading(processes=self.monitor)
        self.monitorThread.start()



    def stopMonitoring(self):
        print 'Stop Monitoring'
        self.monitor.stop()


if __name__ == '__main__':
    sl = SocketListener()
    sl.startListening()
