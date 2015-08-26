#!/user/bin/env python
"""
Resolve the DNS/IP address of a given domain
data returned is in the format:
(name, aliaslist, addresslist)
@filename resolveDNS.py
@version 1.01 (python ver 2.7.3)
@author LoanWolffe
"""
import socket

def getIP(d):
    """
    This method returns the first IP address string
    that responds as the given domain name
    """
    try:
        data = socket.gethostbyname(d)
        ip = repr(data)
        return ip
    except Exception:
        # fail gracefully!
        return False
#
def getIPx(d):
    """
    This method returns an array containing
    one or more IP address strings that respond
    as the given domain name
    """
    try:
        data = socket.gethostbyname_ex(d)
        ipx = repr(data[2])
        return ipx
    except Exception:
        # fail gracefully!
        return False
#
def getHost(ip):
    """
    This method returns the 'True Host' name for a
    given IP address
    """
    try:
        data = socket.gethostbyaddr(ip)
        host = repr(data[0])
        return host
    except Exception:
        # fail gracefully
        return False
#
def getAlias(d):
    """
    This method returns an array containing
    a list of aliases for the given domain
    """
    try:
        data = socket.gethostbyname_ex(d)
        alias = repr(data[1])
        #print repr(data)
        return alias
    except Exception:
        # fail gracefully
        return False
#

# test it

x = raw_input("Domain name or IP address? > ")


a = getIP(x)
b = getIPx(x)
c = getHost(x)
d = getAlias(x)

print " IP ", a
print " IPx ", b
print " Host ", c
print " Alias ", d