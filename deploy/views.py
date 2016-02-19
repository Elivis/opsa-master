#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from deploy.saltapi import SaltAPI
from deploy.models import *
from opsa import settings
from opsa.mysql import db_operate
from asset.models import HostList
from opsa.models import *
from asset.models import *
import time
from installed.models import *
from UserManage.views.permission import PermissionVerify

@login_required
def salt_key_list(request):
    """
    list all key 
    """

    user = request.user
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    minions,minions_pre,minions_rej = sapi.list_all_key()
    minions_count = len(minions) 
    minions_pre_count = len(minions_pre) 
    minions_rej_count = len(minions_rej) 
    return render_to_response('salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre,'all_minions_rej': minions_rej,'minions_count':minions_count,'minions_pre_count':minions_pre_count,'minions_rej_count':minions_rej_count,'request':request}) 

@login_required
@PermissionVerify()
def salt_accept_key(request):
    """
    accept salt minions key
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR'] 
    user = request.user
    node_name = request.GET.get('node_name')
    what = request.GET.get('what')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    if what == "accept":
        ret = sapi.accept_key(node_name)
        HostList.objects.create(hostname=node_name)
    if what == "reject":
        ret = sapi.reject_key(node_name)    
    Message.objects.create(type='salt-key', action=what, action_ip=ip, username=user,content='saltstack accept %s key'%(node_name))
    return HttpResponseRedirect(reverse('key_list')) 

@login_required
@PermissionVerify()
def salt_delete_key(request):
    """
    delete salt minions key
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR'] 
    user = request.user
    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    ret = sapi.delete_key(node_name)
    id_list = HostList.objects.filter(hostname=node_name)
    if id_list:
        for i in id_list:
            host_list = get_object_or_404(HostList, pk=i.id)
            host_list.delete()
            Message.objects.create(type='hostlist', action='delete', action_ip=ip, username=user,content='delete %s' %(node_name))
    Message.objects.create(type='salt-key', action='delete', action_ip=ip, username=user, content='delete %s salt-key' %(node_name))
    return HttpResponseRedirect(reverse('key_list'))

@login_required
@PermissionVerify()
def module_deploy(request):
    ret = []
    ret_err = '' 
    jid = []
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR'] 
    user = request.user
    hostlists = HostList.objects.all()
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        tgt = request.POST.getlist('tgt')
        if len(tgt) == 0:
           ret_err = "目标主机不能为空"
        else:
            ret_err =""
            if action == 'deploy':                          
                arg = request.POST.getlist('module')           
                #Message.objects.create(type='salt', action='deploy', action_ip=tgt, content='saltstack %s module depoy' % (arg))
                sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
                for host in tgt:
                    if 'sysinit' in arg:
                        obj = sapi.async_deploy(host,arg[-1])    #先执行初始化模块,其他任意
                        jid.append(obj)
                        joblist.objects.create(fun='sysinit',tgt=host,status='2',jid=obj)
                        Message.objects.create(type='salt-module', action='deploy', action_ip=ip, username=user, content='%s sysinit_jid %s' % (host,obj))
                        arg.remove('sysinit')
                        if arg:
                            for i in arg:
                                obj = sapi.async_deploy(host,i)     
                                jid.append(obj)
                                joblist.objects.create (fun=i,tgt=host,status='2',jid=obj)
                                Message.objects.create(type='salt-module', action='deploy', action_ip=ip, username=user, content='%s %s_jid %s' % (host,i,obj))
                        
                    else:
                        if arg:
                            for i in arg:
                                obj = sapi.async_deploy(host,i)
                                jid.append(obj)
                                joblist.objects.create (fun=i,tgt=host,status='2',jid=obj)
                                Message.objects.create(type='salt-module', action='deploy', action_ip=ip, username=user, content='%s %s_jid %s' % (host,i,obj))
                    #return HttpResponseRedirect(reverse('job_list'))
                
            elif action == 'sysinit':
                #tgt = request.POST.getlist('tgt')
                arg = 'sysinit'
                #tgtcheck = HostList.objects.filter(hostname=tgt)
                sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                for h in tgt:
                    #Message.objects.create(type='salt-module', action='os_init', action_ip=ip, username=user, content='%s %s_jid %s' % (host,i,obj))
                    sapi.accept_key(h)
                    #sapi.remote_noarg_execution(h,'test.ping')
                    install_ret = SystemInstall.objects.filter(hostname=h)
                    for each_ret in install_ret:
                        sroom_id = each_ret.sroom_id
                    if sroom_id:
                        arg = "sysinit_"+str(sroom_id)                    
                    obj = sapi.async_deploy(h,arg) 
                    SystemInstall.objects.filter(hostname=h).delete()               #安装后，装机列表此IP信息删除，转让到安装记录里供审计
                    Message.objects.create(type='installed', action='os_init', action_ip=ip, username=user, content='%s acceptkey_%s_del_sysinstall' % (h,arg))
                    #Message.objects.create(type='salt', action=arg, action_ip=h, content='已经初始化')
                    #time.sleep(5)
                    #obj = sapi.async_deploy(h,arg)    #先执行初始化模块,其他任意
                     #jid.append(obj)
                    joblist.objects.create (fun=arg,tgt=h,status='2',jid=obj)
                return HttpResponseRedirect(reverse('job_list'))

    return render_to_response('salt_module_deploy.html',{'ret': ret,'hostlists': hostlists,'ret_err':ret_err,'jid':jid,'request':request},context_instance=RequestContext(request)) 

@login_required
@PermissionVerify()
def remote_execution(request):
    """
    remote command execution
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR']      
    tgtcheck = ''
    ret_cmd_msg = []
    hosts = []
    node = ''
    danger = ('rm','reboot','init ','shutdown')
    user = request.user
    ret_err = ''
    ret = 'none'
    tgt = 'none'
    hostlists = HostList.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        tgt = request.POST.getlist('tgt')
        arg = request.POST.get('arg')
        if action != '' and len(tgt) != 0  and arg !='':
            if action == 'exec':#远程命令执行            
                arg1 = arg.split()[0]
                print arg1
                hosts = tgt
                for node in hosts:               
                    argcheck = arg1 not in danger
                    if argcheck:
                        sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                        ret = sapi.remote_execution(node,'cmd.run',arg)
                        cmd_msg="\n"+str(node)+":\n"+"="*24+"\n"+str(ret)
                        #print node,ret[node]
                        ret_cmd_msg.append(cmd_msg)
                        ret_err = '' 
                        Message.objects.create(type='salt-run', action='cmd_run', action_ip=ip, username=user, content='%s cmd.run %s' % (node,arg))
                        
                    elif not argcheck:
                        ret_err = '命令很危险, 你这样子老大会不开森'
            if action == 'grains':#远程命令执行
                arg1 = arg.split()[0]
                print arg1
                hosts = tgt
                for node in hosts:
                    ret_str_msg = ""               
                    argcheck = arg1 not in danger
                    if argcheck:
                        sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                        ret = sapi.remote_execution(node,'grains.item',arg)
                        if type(ret[arg]) == dict:
                            for k, v in ret[arg].items():
                                ret_str_msg  = str(k)+":   "+ str(v)+"\n"+ret_str_msg                               
                            cmd_msg="\n"+str(node)+":\n"+"="*24+"\n"+ret_str_msg
                        else:
                            cmd_msg="\n"+str(node)+":\n"+"="*24+"\n"+str(ret[arg])
                        #print node,ret[node]
                        ret_cmd_msg.append(cmd_msg)
                        ret_err = ''
                        Message.objects.create(type='salt', action='grains', action_ip=ip, username=user, content='%s grains.item %s' % (node,arg))
                                 
                    elif not argcheck:
                        ret_err = '命令很危险, 你这样子老大会不开森'
        elif len(tgt) == 0:
            ret_err = "目标主机不能为空"
        elif arg == '':
            ret_err = "命令不能为空"
            
        #Message.objects.create(type='salt', action='execution', action_ip=ip, username=user, content='saltstack execution command: %s ' % (arg))
         
    return render_to_response('salt_remote_execution.html',
           {'ret':ret,'ret_err': ret_err,'ret_cmd_msg':ret_cmd_msg,'hostlists':hostlists,'request':request},context_instance=RequestContext(request)) 

@login_required
@PermissionVerify()
def salt_job_list(request):
    """
    list all job 
    """

    user = request.user
    if request.method == 'POST':
        search_type = request.POST.get('search_type')
        search_fields = request.POST.get('search')
    else:
        try:
            search_type = request.GET.get('search_type','none')
            search_fields = request.GET.get('search','none')
        except ValueError:
            search_type = 'none'
            search_fields = 'none'
    if search_fields == 'none' or search_type == 'none':
        all_jobs = joblist.objects.all().order_by('-jid')        
    else:        
        if  search_type == 'jid':
            all_jobs = joblist.objects.filter(jid__contains=search_fields).order_by('-jid')
        elif search_type == 'tgt':
            all_jobs = joblist.objects.filter(tgt__contains=search_fields).order_by('-jid')
        elif search_type == 'status':            
            all_jobs = joblist.objects.filter(status=search_fields).order_by('-jid')
        elif search_type == 'fun':            
            all_jobs = joblist.objects.filter(fun__contains=search_fields).order_by('-jid') 
        
    paginator = Paginator(all_jobs,10)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_jobs = paginator.page(page)
    except :
        all_jobs = paginator.page(paginator.num_pages)
    return render_to_response('salt_jobs_list.html', {'all_jobs': all_jobs, 'page': page, 'paginator':paginator,'search':search_fields,'search_type':search_type,'request':request},context_instance=RequestContext(request)) 


def salt_job_results(request):
    """
    list job results
    """
    user = request.user
    if request.method == 'GET':
        jid = request.GET.get('jid')
        tgt = request.GET.get('tgt')
        db = db_operate() 
        if tgt:
            sql = 'select returns from salt_returns where jid=%s and id=%s'
            result=db.select_table(settings.RETURNS_MYSQL,sql,(jid,tgt))    #通过jid获取执行结果
        else:
            sql = 'select returns from salt_returns where jid=%s'
            result=db.select_table(settings.RETURNS_MYSQL,sql,jid)    #通过jid获取执行结果 #  
              
    return render_to_response('salt_jobs_results.html', {'jid':jid,'tgt': tgt,'result':result,'request':request})
 
@login_required
@PermissionVerify()
def deploy_init_status(request):  
    """
    List all waiting for the host operating system is installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR'] 
    #获取待初始化的信息,从数据库中查询是否存在，未存在的插入到列表
    all_system_list = SystemInstall.objects.filter(status='99')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    minions = sapi.list_all_key()
    for tgt in all_system_list:
        if tgt.hostname not in minions[0]:
            sapi.accept_key(tgt.hostname)
            Message.objects.create(type='salt', action='initkey', action_ip=userip, username=user, content='%s accept key' % (tgt.hostname))
            if tgt.hostname in sapi.list_all_key()[0]:
                ret = HostList.objects.filter(hostname=tgt.hostname)
                if ret:
                    print "already in database"
                    #SystemInstall.objects.filter(hostname=h).delete()
                    Message.objects.create(type='sql', action='init', action_ip=tgt.hostname, username=user, content='已经存在')
                else:
                    HostList.objects.create(hostname=tgt.hostname)
                    #SystemInstall.objects.filter(hostname=h).delete()               #安装后，装机列表此IP信息删除，转让到安装记录里供审计
                    #Message.objects.create(type='sql', action='add', action_ip=tgt.hostname, username=user, content='添加主机')
                    Message.objects.create(type='asstes', action='create', action_ip=userip, username=user, content='add %s in hostlist' % (tgt.hostname))
    paginator = Paginator(all_system_list,15)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_system_list = paginator.page(page)
    except :
        all_system_list = paginator.page(paginator.num_pages)

    return render_to_response('deploy_init_status.html', {'all_system_list': all_system_list, 'page': page, 'paginator':paginator,'request':request},context_instance=RequestContext(request))
