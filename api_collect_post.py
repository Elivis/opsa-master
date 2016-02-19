#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-
#fileencoding:utf-8

URL = 'http://localhost/api/install_status_collect/'
import sys
import urllib
import urllib2
import socket
def Get_local_ip():
 """
 Returns the actual ip of the local machine.
 This code figures out what source address would be used if some traffic
 were to be sent out to some well known address on the Internet. In this
 case, a Google DNS server is used, but the specific address does not
 matter much. No traffic is actually sent.
 """
 try:
  csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  csock.connect(('localhost', 80))
  (addr, port) = csock.getsockname()
  csock.close()
  return addr
 except socket.error:
  return "127.0.0.1"
#def postdata(ip,status):

def Get_mac_address():
    import uuid
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])

def postdata(status):
     ip = Get_local_ip()
     print ip
     mac = Get_mac_address()
     print mac
     data = {'ip' : ip,'mac' : mac , 'status' : status}
     body = urllib.urlencode(data)
     print body
     request = urllib2.Request(URL,body)
     urldata = urllib2.urlopen(request)
     b = urldata.read()
     print b
if __name__=='__main__':
     #postdata(sys.argv[1],sys.argv[2])
     postdata(sys.argv[1])
