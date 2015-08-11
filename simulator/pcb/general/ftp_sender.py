#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from ftplib import FTP
import traceback
import sys, os

#-------------------------------------------------------------------------------
# Upload a file to a remove ftp server
#-------------------------------------------------------------------------------
class ftp_sender():
    def __init__(self, ftp_host, ftp_port, ftp_user, ftp_pass, ftp_folder):
        self.ftp = FTP()
        self.ftp.connect(ftp_host, ftp_port)
        self.ftp.login(ftp_user, ftp_pass)
        self.ftp.cwd(ftp_folder)
        self.ftp_host = ftp_host

    def send(self, fname, new_name=None, sub_folder=None):
        if sub_folder:
            self.ftp.cwd(sub_folder)

        # Remove any path component
        remote_name = ""
        if new_name:
            remote_name = os.path.basename(new_name)
        else:
            remote_name = os.path.basename(fname)
        self.ftp.storbinary('STOR ' + remote_name, open(fname,'rb'))

        if sub_folder:
            self.ftp.cwd("..")

    def mkd(self, path):
        self.ftp.mkd(path)

    def rmd(self, path):
        try:
            self.ftp.rmd(path)
        except:
            # yes, there was an error...
            traceback.print_exc(file=sys.stderr)

    def delete(self, fname, sub_folder=None):
        try:
            if sub_folder:
                self.ftp.delete(sub_folder + "/" + os.path.basename(fname))
            else:
                try:
                    self.ftp.delete(os.path.basename(fname))
                except Exception as e:
                    print e.message
        except Exception as e:
            print e.message
            # yes, there was an error...
            traceback.print_exc(file=sys.stderr)

    def get(self, src, tgt):
        return self.ftp.retrbinary(src, tgt)

    def ls(self):
        return self.ftp.nlst()

    def close(self):
        self.ftp.close()

    def mv(self, src, tgt):
        self.ftp.rename(src, tgt)

    def move_down(self):
        self.ftp.cwd('..')
        
    def move_up(self, folder):
        self.ftp.cwd(folder)
    
    def get_ftp_host(self):
        return self.ftp_host
