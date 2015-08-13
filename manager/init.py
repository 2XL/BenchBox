#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
__author__ = 'anna'


from argparse import ArgumentParser

def process_opt():
    parser = ArgumentParser()

    parser.add_argument("-h", dest="help", default="README.md", help="README")

    parser.add_argument("--hosts", dest="hosts", default="config.hosts.ini", help="Folder to output pcap files")

    parser.add_argument("--steps", dest="steps", default=15, type=int, help="Number of steps (default 24)")

    parser.add_argument("--seed", dest="seed", default=int(time.time()), type=int, help="Random seed (default unix_time)")

    parser.add_argument("--ftp", dest="ftp", default=None, help="FTP server where to send the file")

    opt = parser.parse_args()
    if not opt.ftp or not opt.user or not opt.passwd or not opt.output:
        parser.print_help()
        sys.exit(1)











    opt = parser.parse_args()

    return opt

