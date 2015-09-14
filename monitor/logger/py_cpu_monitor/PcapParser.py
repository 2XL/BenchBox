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



    '''

    drop table if EXISTS  logger_pcap;

    create table if not EXISTS logger_pcap (
    ts string,
    ip_src string,
    ip_tgt string,
    port_src int,
    port_tgt int,
    protocol int,
    len int
    ) stored as parquet;

    '''

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

        #print ip.keys()
        print timestamp, src, udp.sport, dst, udp.dport, ip.v, ip.len



'''
Ethernet(
src='\x00\x1a\xa0kUf',
dst='\x00\x13I\xae\x84,',
data=IP(
	src='\xc0\xa8\n\n',
	off=16384,
	dst='C\x17\x030',
	sum=25129,
	len=52,
	p=6,
	id=51105,
	data=
	TCP(seq=9632694,
		off_x2=128,
		ack=3382015884,
		win=54,
		sum=65372,
		flags=17,
		dport=80,
		sport=56145)))

'''




