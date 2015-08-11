#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import time, sys
from capture import pcap_capture

#-------------------------------------------------------------------------------
# aesthetics: humanize byte numbers
#-------------------------------------------------------------------------------
def humanize(bytes, precision=0):
    abbrevs = (
        (1<<50L, u'PB'),
        (1<<40L, u'TB'),
        (1<<30L, u'GB'),
        (1<<20L, u'MB'),
        (1<<10L, u'kB'),
        (1, 'b')
    )
    if bytes == 1:
        return u'1'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

#-------------------------------------------------------------------------------
# Class to monitor amount of traffic on the interface and produce nice output
#-------------------------------------------------------------------------------
class interface_monitor():
    def __init__(self, step, capture, interval=60, threshold=2048):
        # Assuming interface will be silent when the transfer is done
        self.threshold = threshold

        # Number of seconds without traffic to move to the next test
        self.intervals = interval

        # for logging purposes
        self.step = step

        # capture thread, to inform about the amount of traffic
        self.capture = capture

#-------------------------------------------------------------------------------
# Message
#-------------------------------------------------------------------------------
    def say(self, msg):
        print >> sys.stdout, \
            "[STEP " + str(self.step) + "]\t" + msg + (' '*60) + "\r",
        sys.stdout.flush()

#-------------------------------------------------------------------------------
# Sleep
#-------------------------------------------------------------------------------
    def sleep(self, t=60):
        count = 0
        while count < t:
            self.say("sleeping... " + str(t-count))
            time.sleep(1)
            count += 1

#-------------------------------------------------------------------------------
# Calculate usage
#-------------------------------------------------------------------------------
    def calculate_interface_usage(self, interval):
        s = self.capture.get_bytes()
        time.sleep(interval)
        e = self.capture.get_bytes()
        return 1.0*(e-s)/interval

#-------------------------------------------------------------------------------
# wait for the command to finish
#-------------------------------------------------------------------------------
    def wait_transfer(self):
        #self.sleep(50)
        #return
        count = 0
        started = False
        while True:
            traffic = self.calculate_interface_usage(1)
            small_rate = (traffic < self.threshold)
            if not started:
                started = not small_rate
                self.say("waiting transfer...")
            else:
                if small_rate:
                    if count == self.intervals:
                        break
                    else:
                        self.say("rate: " + humanize(traffic) + "/s " + \
                            "(" + str(self.intervals-(count+1)) + "s to go)")
                        count += 1
                else:
                    count = 0
                    self.say("rate: " + humanize(traffic) + "/s " + \
                        "(transferring)")
        print >> sys.stdout, ""
        sys.stdout.flush()
