'''
Created on 22 Sep 2014

@author: cotes
'''

import socket
import time

class CPUMonitor():
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect ((self.host, self.port))
    
    def start_monitor(self, interval, filename, process_name):
        msg = "start " + str(interval) + " " + str(filename) + " " + process_name +"<EOF>"
        self.send_something(msg)
        time.sleep(5)
    
    def stop_monitor(self):
        msg = "stop<EOF>"
        self.send_something(msg)
    
    def send_something(self, msg):
        self.connect()
        self.sock.sendall(msg)
        
import sys
        
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit()
    
    monitor = CPUMonitor('10.30.230.56', 11000)
    if sys.argv[1] == "start":
        monitor.start_monitor(100, "local.txt", "Dropbox")
    else:
        monitor.stop_monitor()