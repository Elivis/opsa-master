#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from installed.models import *
from asset.models import HostList
from installed.form import SystemInstallForm
from installed.cobbler_api import CobblerAPI
from installed.ipmi_api import IPMIAPI
from opsa.models import *
from opsa.mysql import db_operate
from opsa import settings
from config.models import *
import time
from UserManage.views.permission import PermissionVerify
#test ipmi
import os
@login_required
@PermissionVerify()
def system_install_managed(request,id=None):
    """
    Management host to be installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        user_ip = request.META['REMOTE_ADDR'] 
    if id:
        system_install = get_object_or_404(SystemInstall, pk=id)
        pv_type_id = system_install.pv_type
        hostname = system_install.hostname
        action = 'edit'
        page_name = '编辑主机'
    else:
        system_install = SystemInstall()
        pv_type_id = 0
        action = 'add'
        page_name = '添加主机'
    if request.method == 'POST': 
        operate = request.POST.get('operate')        
        form = SystemInstallForm(request.POST,instance=system_install)
        #["pv_type"]=request.POST.get("pv_type")
        form.fields["system_version"].queryset = ConfigOS.objects.filter(isActivated=1)       
        if form.is_valid():
            if operate:
                if operate == 'update':                 
                    form.save()
                    Message.objects.create(type='installed', action='update', action_ip=user_ip, username=user, content='update %s info' %(hostname))
                    return HttpResponseRedirect(reverse('install_list'))
                elif operate == 'add':
                    hostname = request.POST.get('hostname') 
                    form.save()                    
                    Message.objects.create(type='installed', action='add', action_ip=user_ip, username=user, content='add %s info' % (hostname))
                    return HttpResponseRedirect(reverse('install_list'))					
                else:
					pass
    else:
        if id:
            form = SystemInstallForm(instance=system_install)
            form.fields["system_version"].queryset = ConfigOS.objects.filter(isActivated=1)
        else:
            form = SystemInstallForm(initial={'ipmi_user':'root','ipmi_passwd':'ipmipasswd','raid_type':'None',},instance=system_install)
            form.fields["system_version"].queryset = ConfigOS.objects.filter(isActivated=1)        
    
    return render_to_response('install_manage.html',
           {"form": form,
            "pv_type_id":pv_type_id,
            "page_name": page_name,
			"action": action,            
            "request":request,},context_instance=RequestContext(request))   

@login_required
@PermissionVerify()
def system_install_list(request):
    """
    List all waiting for the host operating system is installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR'] 

    #获取待装机的信息,从数据库中查询是否存在，未存在的插入到列表
    result = HostList.objects.filter(status='待装机')
    install_list = []
    for i in range(len(result)):
        ip = str(result[i]).split()[0]
        hostname = str(result[i]).split()[2]
        ret = SystemInstall.objects.filter(ip=ip)
        if ret:
            message = ip + ' already in database'
        else:
            data = {'ip': ip, 'hostname': hostname}
            install_list.append(data)
    
    #列表数据插入数据库 
    for i in range(len(install_list)):
        p = SystemInstall(ip=install_list[i]['ip'],hostname=install_list[i]['hostname'])
        p.save()

    #all_system_list = SystemInstall.objects.all()
    all_system_list = SystemInstall.objects.filter(status='0')
    paginator = Paginator(all_system_list,20)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_system_list = paginator.page(page)
    except :
        all_system_list = paginator.page(paginator.num_pages)

    return render_to_response('install_list.html', {'all_system_list': all_system_list, 'page': page, 'paginator':paginator,'request':request})

@login_required
@PermissionVerify()
def system_install_status(request):
    """
    List all waiting for the host operating system is installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        user_ip = request.META['REMOTE_ADDR'] 
    
    if request.method == 'GET':
        operate = request.GET.get('op')
        ip  =   request.GET.get('ip')
        if (operate == "cancel"):
            ret = SystemInstall.objects.filter(ip = ip)
            for i in ret:
                power_address = i.ipmi_ip
                power_user = i.ipmi_user
                power_pass = i.ipmi_passwd
                sroom_id =  i.sroom_id
                hostname = i.hostname
                pv_type = i.pv_type
            cobbler_apis = ConfigAPI.objects.filter(sroom_id = sroom_id,type = 'cobbler')
            for cobbler_api in cobbler_apis:
                cobbler_api_url = cobbler_api.url
                cobbler_api_user = cobbler_api.user
                cobbler_api_password = cobbler_api.password
            cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
            ret = cobbler.del_system(hostname=hostname)
            if ret['result']:
                if (power_address and power_user and power_pass and pv_type == 1):
                    try:
                        ipmi = IPMIAPI(url=power_address,user=power_user,password=power_pass)
                        ipmi.ipmi_power_off()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})           
            SystemInstall.objects.filter(ip=ip).update(status='0')
            Message.objects.create(type='installed', action='cancel', action_ip=user_ip, username=user, content='cancel %s install ' %(hostname))                     
    all_system_list = SystemInstall.objects.exclude(status__in = ['0','99'])
    paginator = Paginator(all_system_list,20)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_system_list = paginator.page(page)
    except :
        all_system_list = paginator.page(paginator.num_pages)

    return render_to_response('install_status.html', {'all_system_list': all_system_list, 'page': page, 'paginator':paginator,'request':request})

@login_required
@PermissionVerify()
def ipmi_c(request):
      user = request.user
      if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
      else:
        user_ip = request.META['REMOTE_ADDR'] 
    
      if request.method == 'GET':
         power_address = request.GET.get('pip')
         power_user = request.GET.get('pu')
         power_pass = request.GET.get('pp')
         power_operate   = request.GET.get('op') 
                  
         if (power_address and power_user and power_pass and power_operate):
              if power_operate:
                ipmi = IPMIAPI(url=power_address,user=power_user,password=power_pass)
                if power_operate == 'pxe':
                    try:
                        ipmi.ipmi_pxe()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
                elif power_operate == 'power_on':
                    try:
                        ipmi.ipmi_power()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})               
                elif power_operate == 'power_status':
                    try:
                        ipmi.ipmi_power_status()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})             
                elif power_operate == 'power_off': 
                    try:
                        ipmi.ipmi_power_off()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
                elif power_operate == 'bios':
                    try:
                        ipmi.ipmi_bios()
                    except Exception as e:
                        ret_err = 'IPMI有问题，请检查IPMI网络，用户名等配置'
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})                    
                else:
                    pass
         return HttpResponseRedirect(reverse('install_status'))    

@login_required
@PermissionVerify()            
def system_install(request):
    """
    1.Add Some Info to Cobbler System
    2.Remote starting up
    3.screen put in System Install process 
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        user_ip = request.META['REMOTE_ADDR']
        
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            ret_data = SystemInstall.objects.filter(id=id)
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
                cobbler_api_fqdn = cobbler_api.fqdn
            cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
            
            if pv_type_id == 1:
                power_address = ret_data[0].ipmi_ip
                power_user = ret_data[0].ipmi_user
                power_pass = ret_data[0].ipmi_passwd
                raid_type = ret_data[0].raid_type
                '''is it config raid'''
                if "noraid" in str(raid_type):
                    profile = str(ret_data[0].system_version)                    
                else:
                    profile = "DTK4.4-x86_64"
                                        
                if "Select" not in str(raid_type) and "noraid" not in str(raid_type):
                    kopts = 'share_script=%s.sh tftp_ip=%s share_type=tftp share_location=/raidcfg' % (raid_type,cobbler_api_fqdn)
                elif "noraid" in str(raid_type):
                    kopts = 'dhcpclass=anaconda'
                else:
                    ret_err = "物理服务器请输入具体的raid类型或不选择raid创建"
                    return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
                #ret = add_system(hostname=hostname,ip_add=ip,mac_add=mac_add,profile=profile,kopts=kopts)
                if power_address == "":
                    ret_err = "物理服务器请输入ipmi的IP地址或选择虚拟机模式来安装物理机"
                    return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
                elif(power_address and power_user and power_pass ): 
                    ipmi_ret = True                 
                    ipmi = IPMIAPI(url=power_address,user=power_user,password=power_pass)                    
                    ipmi_ret = ipmi.ipmi_power_status()
                    if not(ipmi_ret):
                        ret_err = '无法获取主机电源状态，请检查IPMI配置，若ipmi确有问题可以手动安装，模式选择虚拟机' 
                        return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
            else:
                kopts = 'dhcpclass=anaconda'
            try:
                ret = cobbler.add_system(hostname=hostname,ip_add=ip,mac_add=mac_add,profile=profile,kopts=kopts)
            except Exception as e:
                ret_err = '无法加入cobbler,请检查配置信息是否正确' 
                ret_e = e    
                return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'ret_e':ret_e,'request':request})
            if ret['result']:
                if( pv_type_id == 1):
                    ipmi.ipmi_pxe()
                    ipmi.ipmi_power()
                    if "noraid" in str(raid_type):
                        SystemInstall.objects.filter(id=id).update(status='1')
                    else:
                        SystemInstall.objects.filter(id=id).update(status='0.5') 
                else:
                    SystemInstall.objects.filter(id=id).update(status='1')     #主机信息加入cobbler system，主机列表的状态变更为已使用状态，不再是待装机状态！
                Message.objects.create(type='installed', action='installing', action_ip=user_ip, username=user, content=' %s is starting to install ' %(hostname))                     
            else:
                ret_err = '无法加入cobbler,请检查配置信息是否正确'                
                return render_to_response('error_ret.html', {'title':hostname,'ret_err': ret_err,'request':request})
    return HttpResponseRedirect(reverse('install_status'))
def install_logs(request):
    """
    1.Add Some Info to Cobbler System
    2.Remote starting up
    3.screen put in System Install process 
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        user_ip = request.META['REMOTE_ADDR']
    if request.method == 'GET':
       id = request.GET.get('id')
       ret_data = SystemInstall.objects.filter(id=id)   
       sroom_id = ret_data[0].sroom_id
       ip = ret_data[0].ip
       hostname = ret_data[0].hostname    
       try:
           f=open('/var/log/cobbler/anamon/%s/anaconda.log' %(hostname),'r')
           data=f.read()
           f.close
       except:
           data="The file /etc/salt/master is not exist"
       return render_to_response('install_logs.html', {'title':hostname,'data': data,'host_data':ret_data,'request':request})
@login_required
@PermissionVerify()
def system_install_finish(request):
     user = request.user
     if request.method == 'GET':
       sroom_id = request.GET.get('idc')
       ip = request.GET.get('ip')
       hostname = request.GET.get('host')
       mac_add = request.GET.get('mac')
       profile = request.GET.get('ver')
       action = request.GET.get('action')
       cobbler_apis = ConfigAPI.objects.filter(sroom_id = sroom_id,type = 'cobbler')
       for cobbler_api in cobbler_apis:
            cobbler_api_url = cobbler_api.url
            cobbler_api_user = cobbler_api.user
            cobbler_api_password = cobbler_api.password
       cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
       try:
           ret = cobbler.del_system(hostname=hostname)
       except ValueError:
            ret = "pls. del cobbler"
       if ret['result']:
           data = SystemInstall.objects.filter(ip=ip)
           install_date = str(data[0]).split('--')[1].strip()
           InstallRecord.objects.create(hostname=hostname,sroom_id=sroom_id,username=user,ip=ip,system_version=profile,install_date=install_date)
           SystemInstall.objects.filter(ip=ip).update(status='99')     #主机信息加入cobbler system，主机列表的状态变更为已使用状态，不再是待装机状态！
           #SystemInstall.objects.filter(ip=ip).delete()               #安装后，装机列表此IP信息删除，转让到安装记录里供审计
           Message.objects.create(type='install', action='finish', action_ip=ip, content='主机已经完成安装')
       if action == 'init':
           return HttpResponseRedirect(reverse('install_init'))
       elif action == 'reinstall':
           SystemInstall.objects.filter(ip=ip).update(status='0')
           return HttpResponseRedirect(reverse('install_status'))
       else:
           SystemInstall.objects.filter(ip=ip).delete()
           return HttpResponseRedirect(reverse('install_status'))        

@login_required
@PermissionVerify()
def system_install_record(request):
    """
    List all operating system installation records
    """
    
    user = request.user 
    if request.method == 'POST':
        search_fields = request.POST.get('search')
    else:
        try:
            search_fields = request.GET.get('search','none')
        except ValueError:
            search_fields = 'none'
    if search_fields == 'none':
        record = InstallRecord.objects.all().order_by('-id')       
    else:
        record = InstallRecord.objects.filter(hostname__contains=search_fields).order_by('-id')   
    paginator = Paginator(record,12)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        record = paginator.page(page)
    except :
        record = paginator.page(paginator.num_pages)
 
    return render_to_response('install_record_list.html', {'record': record, 'page': page, 'paginator':paginator,'search':search_fields,'request':request},context_instance=RequestContext(request))