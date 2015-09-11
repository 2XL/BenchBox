#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from threading import Thread
import netifaces as ni
import time, traceback, sys
import pcapy
import pyshark

#-------------------------------------------------------------------------------
# Thread to capture the packets
#-------------------------------------------------------------------------------
class pcap_capture(Thread):
    def __init__(self, iface, pcap_name):
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

        snaplen = 1600
        promsc = 1
        to_ms = 100

        self.pcap = pcapy.open_live(iface, snaplen, promsc, to_ms)
        self.pcap.setfilter(my_filter)
        self.dumper = self.pcap.dump_open(pcap_name)

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

    def capture(self):
        while not self.stopit:
            self.pcap.dispatch(1, self.call_back)
        self.done = True

    def run (self):
        self.capture()

    def stop(self):
        self.stopit = True
        return self.done

    def show_results(self):
        print 'Show Results'

#-------------------------------------------------------------------------------
# Main - For testing purposes
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # start capturing the traffic
    # have to give superuser permission to capture
    worker = None

    try:
        filename = "/tmp/test.cap"
        worker = pcap_capture('wlan0', filename)
        worker.daemon = True
        worker.start()
        time.sleep(5)
        print "packets:", worker.get_packets(), "bytes:", worker.get_bytes()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    while not worker.stop(): pass
    print 'Post process'

    worker.join()
    cap = pyshark.FileCapture(filename, only_summaries=True)
    print cap
    num = len(cap)
    # num of packets captured
    print num
    print 'show packets'
    for pkt in cap:
        print pkt
    print 'finish packets'






