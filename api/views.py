#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

#包含以下模块 
from django.shortcuts import render_to_response 
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from installed.models import SystemInstall
from api.install_api import *

'''
#包含json模块 
try: 
    import json 
except ImportError,e: 
    import simplejson as json 
'''
#用来接收客户端服务器发送过来的数据 
@csrf_exempt
def install_status_collect(request): 
    req = request 
    if req.POST: 
        ip = req.POST.get('ip')
        mac = req.POST.get('mac')
        status = req.POST.get('status')
        ret = req.POST.get('ret')
        pv_raid = req.POST.get('pv')
        apiadmin = req.POST.get('admin')
        apipasswd = req.POST.get('passwd')
           
        
        if (apiadmin == 'admin' and apipasswd == 'passwd' and status == '1' ):
            os_install_ret = os_install(ip)             
            if os_install_ret:
                SystemInstall.objects.filter(ip=ip).update(status=status)
            else:
                SystemInstall.objects.filter(ip=ip).update(status=103)
            #ret="ok"
        elif(status == '5'):
            os_install_ipmi(ip)
            #SystemInstall.objects.filter(ip=ip).update(status=status)
            ret="OK"
        else:
            SystemInstall.objects.filter(ip=ip).update(status=status)
            #ret ="error"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        return HttpResponse("IP:%s , mac:%s ,status:%s ,ret:%s " %(ip,mac,status,ret))   #如果有结果，返回'ok'
    else: 
        return HttpResponse('no post data') 

