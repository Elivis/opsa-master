#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from installed.models import *
from installed.cobbler_api import CobblerAPI
from installed.ipmi_api import IPMIAPI
from opsa.models import *
from opsa import settings
from config.models import *
import time
from installed.ipmi_api import IPMIAPI

def os_install(ip):
   os_install = False
   ret_data = SystemInstall.objects.filter(ip=ip)
   id = ret_data[0].id
   sroom_id = ret_data[0].sroom_id
   ip = ret_data[0].ip
   hostname = ret_data[0].hostname
   mac_add = ret_data[0].macaddress
   profile = str(ret_data[0].system_version)
   pv_type_id = ret_data[0].pv_type
       #install_date = ret_data[0].install_date
       #----------cobbler api-----------
   cobbler_apis = ConfigAPI.objects.filter(sroom_id = sroom_id,type = 'cobbler')
   for cobbler_api in cobbler_apis:
       cobbler_api_url = cobbler_api.url
       cobbler_api_user = cobbler_api.user
       cobbler_api_password = cobbler_api.password
       #cobbler_api_fqdn = cobbler_api.fqdn
   cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
   print pv_type_id            
   if pv_type_id == 1:
       power_address = ret_data[0].ipmi_ip
       power_user = ret_data[0].ipmi_user
       power_pass = ret_data[0].ipmi_passwd
       raid_type = ret_data[0].raid_type
       kopts = 'dhcpclass=anaconda' 
       print hostname
       try:
           ret1 = cobbler.del_system(hostname=hostname)
           os_install = True
       except Exception as e:
           SystemInstall.objects.filter(id=id).update(status='101')
           ret1['result'] = False
           os_install = False
           print e
   else:
       ret1['result'] = False
       os_install = True
   if ret1['result']:
       try:
           ret = cobbler.add_system(hostname=hostname,ip_add=ip,mac_add=mac_add,profile=profile,kopts=kopts)
           os_install = True
       except Exception as e:
           SystemInstall.objects.filter(id=id).update(status='102')
           ret['result'] = False
           os_install = False
           print e 
       if ret['result']:
           if( pv_type_id == 1 and power_address and power_user and power_pass ):
               #time.sleep(60)
               ipmi = IPMIAPI(url=power_address,user=power_user,password=power_pass)
               ipmi.ipmi_pxe()
               ipmi.ipmi_power()
               #SystemInstall.objects.filter(id=id).update(status='1')
               os_install = True
           else:
               os_install = False
   return os_install
               
def os_install_ipmi(ip):
    ret_data = SystemInstall.objects.filter(ip=ip)
    id = ret_data[0].id
    sroom_id = ret_data[0].sroom_id
    hostname = ret_data[0].hostname
    ret = False
    pv_type_id = ret_data[0].pv_type
    cobbler_apis = ConfigAPI.objects.filter(sroom_id = sroom_id,type = 'cobbler')
    for cobbler_api in cobbler_apis:
        cobbler_api_url = cobbler_api.url
        cobbler_api_user = cobbler_api.user
        cobbler_api_password = cobbler_api.password
       #cobbler_api_fqdn = cobbler_api.fqdn
    cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
    if pv_type_id == 1:
       power_address = ret_data[0].ipmi_ip
       power_user = ret_data[0].ipmi_user
       power_pass = ret_data[0].ipmi_passwd
       if( pv_type_id == 1 and power_address and power_user and power_pass ):
               #time.sleep(60)
               ipmi = IPMIAPI(url=power_address,user=power_user,password=power_pass)
               ret = ipmi.ipmi_disk()
               if ret:
                   #time.sleep(60)
                   #ipmi.ipmi_power()
                   #SystemInstall.objects.filter(id=id).update(status='5')                 
                   try:
                       cobbler_ret = cobbler.edi_system(hostname=hostname,netboot='False')
                   except Exception as e:
                       SystemInstall.objects.filter(id=id).update(status='51')
                       cobbler_ret['result'] = False                       
                       print e 
                   time.sleep(40)
                   if cobbler_ret['result']:
                       SystemInstall.objects.filter(id=id).update(status='5')
                   else:
                       SystemInstall.objects.filter(id=id).update(status='51')
                                                        
               else:
                   SystemInstall.objects.filter(id=id).update(status='50')               
    elif pv_type_id == 0:
        SystemInstall.objects.filter(id=id).update(status='5')
        try:
            cobbler_ret = cobbler.edi_system(hostname=hostname,netboot='False')
        except Exception as e:
            SystemInstall.objects.filter(id=id).update(status='51')
            cobbler_ret['result'] = False
            print e    
        time.sleep(30)
        if cobbler_ret['result']:
            SystemInstall.objects.filter(id=id).update(status='5')
        else:
            SystemInstall.objects.filter(id=id).update(status='51')

        