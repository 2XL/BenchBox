
from Monitor import Monitor
from threading import Thread
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

    monitor = Monitor()
    monitorThread = None  # = threading.Thread(target=worker, args=None)

    def __init__(self, monitor = None):
        print '__init__: SocketListener'
        # self.monitor = monitor

    def recv_data(self, sock): # incoming data from the client
        total_data=[]
        while True:
            data = sock.recv(1024)
            if not data: break
            total_data.append(data)
        return ''.join(total_data)

    End = '<EOF>' # something useable as an end marker
    def recv_end(self, the_socket):
        total_data=[];data=''
        while True:
            data=the_socket.recv(1024)
            if self.End in data:
                total_data.append(data[:data.find(self.End)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if self.End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(self.End)]
                    total_data.pop()
                    break
        return ''.join(total_data)

    def startListening(self):
        # data buffer for the incoming data
        bytes  = list() # bytes of size 1024

        # establish the local endpoint for the socked
        # dns.gethostname return the name of the host running the application
        staticPort = 11000
        #ipHostInfo = socket.gethostname()
        #ipAddress =  socket.gethostbyname(ipHostInfo)
        ipAddress =  '192.168.56.101'
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

                data = self.recv_end(conn)
                conn.sendall(data)

                time.sleep(1)

                print 'Text recv: {}'.format(data)

                print 'dataBuffer'
                print data

                if 'start' in data:
                    print 'StartMonitoring'
                    self.startMonitoring(data)
                elif 'stop' in data:
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
        print 'Start Monitoring: {}'.format(command)
        # start monitoring a specific process
        command = command.replace('<EOF>', '')
        parameters = command.split(' ')
        interval = int(parameters[1])
        filename = str(parameters[2])
        processes = list()

        for i in range(3, len(parameters)):
            processes.append(parameters[i])


        print parameters, interval, filename, processes

        self.monitor.setInterval(interval)
        self.monitor.setFilename(filename)
        self.monitor.setProcess(processes)
        self.monitor.prepareMonitoring()

        print 'DefineMonitorThread...'
        self.monitorThread = Thread(target=self.monitor.ThreadProc)
        print 'LaunchMonitorThread...'
        self.monitorThread.start() # aqui perd lo control <-- bug linea anterior xD
        print 'MonitorThreadRunning!!'



    def stopMonitoring(self):
        print 'Stop Monitoring'
        self.monitor.stop()
        #


if __name__ == '__main__':
    sl = SocketListener()
    sl.startListening()
