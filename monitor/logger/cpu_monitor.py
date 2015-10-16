'''
Created on 22 Sep 2014

@author: cotes
'''

import socket
import time
import sys

class CPUMonitor():

    sock = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    
    def start_monitor(self, interval, filename, process_name):
        msg = "start " + str(interval) + " " + str(filename) + " " + process_name +"<EOF>"
        self.send_something(msg)
        time.sleep(interval)
    
    def stop_monitor(self):
        msg = "stop <EOF>"
        self.send_something(msg)
        print 'sendStop_msg'
    
    def send_something(self, msg):
        self.connect()
        self.sock.sendall(msg)
        if msg != "stop <EOF>":
            try:
                while True:
                    data = self.sock.recv(1024)
                    if data:
                        print "recv: {}".format(data)

                    break
            except:
                print 'Exception Unhandled'
        self.sock.close()


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit()

    monitor = CPUMonitor(socket.gethostbyname(socket.gethostname()), 11000)
    if sys.argv[1] == "start":
        interval = 1    # seconds
        log_filename = "local.log"  # output suffix
        proc_name = "StackSync"
        monitor.start_monitor(interval, log_filename, proc_name)
    else:
        monitor.stop_monitor()