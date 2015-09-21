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
    
    def start_monitor(self, interval, filename, process_name, operations, profile, hostname):
        # (interval, log_filename, proc_name, opt.ops, opt.profile)
        msg = "start " + str(interval) +\
              " " + str(filename) + \
              " " + str(process_name) +\
              " " + str(operations) + \
              " " + str(profile)+\
              " " + str(hostname)+"<EOF>"
        self.send_something(msg)
        time.sleep(interval)
    
    def stop_monitor(self):
        msg = "stop <EOF>"
        self.send_something(msg)
        print 'sendStop_msg'
    
    def send_something(self, msg):
        self.connect()
        # send data
        self.sock.sendall(msg)
        # look for response
        if msg != "stop <EOF>":
            try:
                while True :
                    data = self.sock.recv(1024)
                    if data:
                        print "recv: {}".format(data)

                    break
            except:
                print 'Exception Unhandled'
        self.sock.close()

        
import sys
        
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit()
    
    #monitor = CPUMonitor('10.30.230.56', 11000)
    #monitor = CPUMonitor(socket.gethostbyname(socket.gethostname()), 11000)
    monitor = CPUMonitor('192.168.56.101', 11000) # sandBox ip
    if sys.argv[1] == "start":
        interval = 5 # segons
        log_filename = "local.txt"
        proc_name = "Python"
        monitor.start_monitor(interval, log_filename, proc_name)
    else:
        monitor.stop_monitor()