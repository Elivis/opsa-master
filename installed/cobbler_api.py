#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-


import cobbler
import xmlrpclib 

class CobblerAPI(object):
    def __init__(self,url,user,password):
        self.cobbler_user = user
        self.cobbler_pass = password
        self.cobbler_url = url
    
    def add_system(self,hostname,ip_add,mac_add,profile,kopts):
        '''
        Add Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        
        remote = xmlrpclib.Server(self.cobbler_url)
        token = remote.login(self.cobbler_user,self.cobbler_pass) 
        print token
        system_id = remote.new_system(token) 
        remote.modify_system(system_id,"name",hostname,token) 
        remote.modify_system(system_id,"hostname",hostname,token) 
        remote.modify_system(system_id,'modify_interface', { 
            "macaddress-eth0" : mac_add, 
            "ipaddress-eth0" : ip_add, 
            "dnsname-eth0" : hostname, 
        }, token) 
        remote.modify_system(system_id,"profile",profile,token)
        #if kopts:
        remote.modify_system(system_id,"kopts",kopts,token) 
        remote.save_system(system_id, token) 
        try:
            remote.sync(token)
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret
    def edi_system(self,hostname,netboot):
        '''
        Add Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        
        remote = xmlrpclib.Server(self.cobbler_url)
        token = remote.login(self.cobbler_user,self.cobbler_pass) 
        print token
        system_id = remote.get_system_handle(hostname,token) 
        remote.modify_system(system_id,"netboot_enabled",netboot,token)        
        remote.save_system(system_id, token) 
        try:
            remote.sync(token)
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret
        
    def del_system(self,hostname):
        '''
        Del Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        
        remote = xmlrpclib.Server(self.cobbler_url)
        token = remote.login(self.cobbler_user,self.cobbler_pass) 
        print token        
        try:
            remote.remove_system(hostname,token)
            remote.sync(token)
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret
    def get_system(self,hostname):
        ret = {
            "result": True,
            "comment": [],
        }
        remote = xmlrpclib.Server(self.cobbler_url) 
        try:
            ret = remote.find_profile({"name":"*"})
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret
    
    def get_proflies(self):
        '''
        get cobbler profiles
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        remote = xmlrpclib.Server(self.cobbler_url)
        try:
            ret = remote.find_profile({"name":"*"})
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret
        
def main():
    cobbler = CobblerAPI(url,user,password,)
    ret = cobbler.add_system(hostname='test',ip_add='#',mac_add='#',profile='CentOS6.3-x86_64')
    print ret

if __name__ == '__main__':
    main()
