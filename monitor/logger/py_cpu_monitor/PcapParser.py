#!/usr/bin/python
# -*- coding: iso-8859-1 -*-



import pcapy
import dpkt
import socket


class pcapDumper():

    def __init__(self):
        print 'pcapDumper to log datastore'


    def dumpToImpala(self, pcap_data,  src='/tmp/test.pcap'):
        print 'dumpToImpala'
        for idx, data in pcap_data:
            ts = '{},{}'.format(idx.getts()[0], idx.getts()[1] )
            ether =  dpkt.ethernet.Ethernet(data)
            if ether.type != dpkt.ethernet.ETH_TYPE_IP: raise
            ip = ether.data
            #print ip.data
            dst = socket.inet_ntoa(ip.dst)
            src = socket.inet_ntoa(ip.src)
            udp = ip.data
            print ts, src, udp.sport, dst, udp.dport, ip.v, ip.len




#-------------------------------------------------------------------------------
# Main - For testing purposes
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    p = '/tmp/test.pcap'
    pcapReader = dpkt.pcap.Reader(file((p),'rb'))
    for timestamp, data in pcapReader:
        print timestamp
        ether = dpkt.ethernet.Ethernet(data)
        if ether.type != dpkt.ethernet.ETH_TYPE_IP: raise
        ip = ether.data
        dst = socket.inet_ntoa(ip.dst)
        src = socket.inet_ntoa(ip.src)
        udp = ip.data
        print timestamp, src, udp.sport, dst, udp.dport, ip.v, ip.len


