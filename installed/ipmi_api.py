#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-


import os
class IPMIAPI(object):
    def __init__(self,url,user,password):
        self.power_user = user
        self.power_pass = password
        self.power_address = url
    
    def ipmi_power(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
             
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power status" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            print status
            if ('on' in status):
                cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power reset" % (power_address, power_user, power_pass)
            elif ('off' in status):
                cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power on" % (power_address, power_user, power_pass)
            else:
                return error_page(request, "can not get power status.")
            if (os.system(cmd)): 
                return error_page(request, "power system on/reset failed.") 
    
    def ipmi_power_off(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
             
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power status" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            #print status
            if ('on' in status):
                cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power off" % (power_address, power_user, power_pass)
            else:
                return error_page(request, "get power is off.")
            if (os.system(cmd)): 
                return error_page(request, "power system off failed.") 
        
    def ipmi_power_status(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
        ret = {
            "result": True,
            "comment": [],
        }   
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power status" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            if ('on' in status):
                status = 'on'
            elif ('off' in status):
                status = 'yes'
            else:
                status = False
            return status
                
    def ipmi_pxe(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
        
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s chassis bootdev pxe" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            print status
            if ('pxe' in status):
                result = "setting pxe success."      
            else:
                result = "can not set pxe failed."
            #print result
            return result
    
    def ipmi_bios(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
        
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s chassis bootdev bios" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            print status
            if ('bios' in status):
                result = "setting bios success."      
            else:
                result = "can not set bios failed."
            #print result
            return result
    def ipmi_disk(self):
        power_address = self.power_address
        power_user = self.power_user
        power_pass = self.power_pass
        
        if (power_address and power_user and power_pass):
            # power on or reset node
            cmd = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s chassis bootdev disk" % (power_address, power_user, power_pass)
            output = os.popen(cmd)    
            status = output.read()
            output.close()
            print status
            if ('disk' in status):
                result = True      
            else:
                result = False
            #print result
            return result