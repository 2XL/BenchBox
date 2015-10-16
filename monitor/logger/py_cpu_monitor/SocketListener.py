
from Monitor import Monitor
from threading import Thread
import socket
import sys
import asyncore
import time
import SocketServer, subprocess

HOST = '192.168.56.101'
PORT = 11000


def worker():
    print 'This is a thread job'


class SocketListener():

    monitor = Monitor()
    monitorThread = None

    def __init__(self, monitor = None):
        print '__init__: SocketListener'
        # self.monitor = monitor

    def recv_data(self, sock):

        total_data=[]
        while True:
            data = sock.recv(1024)
            if not data: break
            total_data.append(data)
        return ''.join(total_data)

    End = '<EOF>' # something useable as an end marker

    def recv_end(self, the_socket):
        total_data=[]
        data=''
        while True:
            data=the_socket.recv(1024)
            if self.End in data:
                total_data.append(data[:data.find(self.End)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                last_pair=total_data[-2]+total_data[-1]
                if self.End in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(self.End)]
                    total_data.pop()
                    break
        return ''.join(total_data)

    def startListening(self):
        bytes  = list() # bytes of size 1024

        staticPort = PORT
        if socket.gethostname() == 'Jo':
            ipAddress = socket.gethostbyname(socket.gethostname())
        else:
            ipAddress = HOST
        localEndPoint = ipAddress, staticPort
        print localEndPoint

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            max_connections = 10
            listener.bind(localEndPoint)
            listener.listen(max_connections)

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
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        finally:
            listener.close()

        print 'SocketListener, QUIT!'


    def startMonitoring(self, command):
        # this...
        print 'Start Monitoring: {}'.format(command)

        command = command.replace('<EOF>', '')
        parameters = command.split(' ')
        interval = int(parameters[1])
        filename = str(parameters[2])
        processes = str(parameters[3])
        operations = str(parameters[4])
        profile = str(parameters[5])
        hostname = str(parameters[6])

        print parameters, interval, filename, processes

        self.monitor.setInterval(interval)
        self.monitor.setFilename(filename)
        self.monitor.setProcess(processes)
        self.monitor.setLoggerId(hostname, processes, profile, operations)

        self.monitor.prepareMonitoring()
        print 'DefineMonitorThread...'
        self.monitorThread = Thread(target=self.monitor.ThreadProc)
        print 'LaunchMonitorThread...'
        self.monitorThread.start()
        print 'MonitorThreadRunning!!'

    def stopMonitoring(self):
        print 'Stop Monitoring'
        self.monitor.stop()


if __name__ == '__main__':
    sl = SocketListener()
    sl.startListening()
