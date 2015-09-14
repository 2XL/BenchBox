#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from threading import Thread
import netifaces as ni
import time, traceback, sys
import pcapy
import socket
from PcapParser import pcapDumper

#-------------------------------------------------------------------------------
# Thread to capture the packets
#-------------------------------------------------------------------------------
class pcap_capture(Thread):
    def __init__(self, iface = 'eth0', pcap_name = '/tmp/test.pcap'):
        Thread.__init__(self)

        #TODO: Parameters!
        #print ni.ifaddresses("eth0")[2]
        #print ni.ifaddresses("eth1")[2]
        ip = ni.ifaddresses(iface)[2][0]['addr']
        p = ["80", "443", "8080", "3128", "38088", "5672"]
        my_filter = "(port " + " || port ".join(p) + ") && (host " + ip + ")"

        self.stopit = False
        self.done = False
        self.bytes = 0
        self.packets = 0
        self.pcap = pcapy.open_live(iface, 1600, 1, 100)
        self.pcap.setfilter(my_filter)
        self.dumper = self.pcap.dump_open(pcap_name)
        self.dumper_list = list()
        self.pcap_dumper = pcapDumper()

    def stop_flag(self):
        return self.stopit

    def get_bytes(self):
        return self.bytes

    def get_packets(self):
        return self.packets

    def call_back(self, header, data):
        self.packets += 1
        self.bytes += header.getlen()
        self.dumper.dump(header, data)
        self.dumper_list.append((header, data))

    def capture(self):
        while not self.stopit:
            self.pcap.dispatch(1, self.call_back)
        self.done = True

    def run (self):
        self.capture()

    def stop(self):
        self.stopit = True
        return self.done


def dump(obj, name):
    for attr  in dir(obj):
        print "%s => obj.%s = %s" % (name, attr, getattr(obj, attr))
        #print obj.attr()

#-------------------------------------------------------------------------------
# Main - For testing purposes
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # start capturing the traffic
    worker = None
    try:
        p = "/tmp/test.pcap"
        worker = pcap_capture('wlan0' )
        worker.daemon = True
        worker.start()
        time.sleep(5)
        print "packets:", worker.get_packets(), "bytes:", worker.get_bytes()
    except:
        traceback.print_exc(file=sys.stderr)
    finally:
        while not worker.stop(): pass

    worker.join()
    worker.pcap_dumper.dumpToImpala(worker.dumper_list)