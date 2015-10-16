#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import pcapy
import dpkt
import socket
from StoreManager import StoreManager
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class pcapDumper():

    def __init__(self):
        print 'pcapDumper to log datastore'


    def dumpToImpala(self, pcap_data,  src='/tmp/test.pcap'):
        print 'dumpToImpala'


        sm = StoreManager('ast12.recerca.intranet.urv.es',
                          21050,
                          'lab144',
                          'lab144')
        sm.connect()
        sm.execute('use benchbox')

        for idx, data in pcap_data:
            ts = '{},{}'.format(idx.getts()[0], idx.getts()[1] )
            ether =  dpkt.ethernet.Ethernet(data)
            if ether.type != dpkt.ethernet.ETH_TYPE_IP: raise
            ip = ether.data
            #print ip.data
            dst = socket.inet_ntoa(ip.dst)
            src = socket.inet_ntoa(ip.src)
            udp = ip.data
            line = (ts, src, udp.sport, dst, udp.dport, ip.v, ip.len)
            insert_into_logger = "insert into logger_pcap values ('{}', '{}', '{}', {}, {}, {}, {})".format(ts,
                                                                                                              src,
                                                                                                              dst,
                                                                                                              udp.sport,
                                                                                                              udp.dport,
                                                                                                              ip.v,
                                                                                                              ip.len)
            sm.execute(insert_into_logger)
        sm.quit()


def print_obj_attr(an):
    attrs = vars(an)
    print ', '.join("%s: %s" % item for item in attrs.items())
    print attrs

#-------------------------------------------------------------------------------
# Main - For testing purposes
#-------------------------------------------------------------------------------

if __name__ == '__main__':

    p = '/tmp/test.pcap'
    pcapReader = dpkt.pcap.Reader(file((p),'rb'))
    for timestamp, data in pcapReader:
        # print timestamp
        ether = dpkt.ethernet.Ethernet(data)

        if ether.type != dpkt.ethernet.ETH_TYPE_IP: raise
        ip = ether.data
        dst = socket.inet_ntoa(ip.dst)
        src = socket.inet_ntoa(ip.src)
        udp = ip.data
        if hasattr(udp, 'flags'):
            print udp.flags
        if hasattr(udp, 'off_x2'):
            print udp.off_x2

        print timestamp, src, udp.sport, dst, udp.dport, ip.v, ip.len




