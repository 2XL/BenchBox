#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import time

#-------------------------------------------------------------------------------
# create a log file to output experiment metadata
#-------------------------------------------------------------------------------
class logger():
    def __init__(self, fname, opt):
        try:
            opts = vars(opt)
        except Exception as e:
            opts = opt
        try:
            self.file = open(fname, "aw+")
        except Exception as e:
            print e
            print "Folder output not found!, Please Create it manually..."

        print >> self.file, "%.6f" % time.time(), { k : opts[k] for k in opts }
        self.file.flush()

    def write(self, message):
        print >> self.file, "%.6f" % time.time(), message , '\n'
        self.file.flush()

    def close(self):
        self.file.close()