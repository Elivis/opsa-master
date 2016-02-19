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
from django.core.exceptions import ObjectDoesNotExist
from asset.models import HostList
from config.form import ConfigAPIForm
from config.models import *
from opsa.models import *
from opsa.mysql import db_operate
from opsa import settings
from installed.cobbler_api import CobblerAPI
from UserManage.views.permission import PermissionVerify

@login_required
@PermissionVerify()
def config_info(request,id=None):
    """
    Management API
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR'] 
    if id:
        config_api = get_object_or_404(ConfigAPI, pk=id)
        action = 'edit'
        page_name = '编辑API'
    else:
        config_api = ConfigAPI()
        action = 'add'
        page_name = '添加API'
    if request.method == 'POST': 
        operate = request.POST.get('operate')
        form = ConfigAPIForm(request.POST,instance=config_api)
        if form.is_valid():
            if operate:
                if operate == 'update':
                    form.save()
                    db = db_operate() 
                    sql = 'select create_user from installed_ConfigAPI where id = %s' % (id)
                    ret = db.mysql_command(settings.opsa_MYSQL,sql)
                    Message.objects.create(type='config', action='update', action_ip=userip, username=user,content='update %s config api '%(id))
                    return HttpResponseRedirect(reverse('config_api_list'))
                elif operate == 'add':
                    form.save()
                    db = db_operate() 
                    #sql = 'select ip from installed_ConfigAPI where id = %s' % (id)
                    #ret = db.mysql_command(settings.opsa_MYSQL,sql)
                    ret = '添加新API'
                    #Message.objects.create(type='config', action='api_add', action_ip=ret, content='API信息已经更新')
                    Message.objects.create(type='config', action='add', action_ip=userip, username=user,content='add new %s'%(ret))
                    return HttpResponseRedirect(reverse('config_api_list'))					
                else:
					pass
    else:
        form = ConfigAPIForm(instance=config_api)

    return render_to_response('config_api_manage.html',
           {"form": form,
            "page_name": page_name,
			"action": action,
            'request':request,
           },context_instance=RequestContext(request))   

@login_required
@PermissionVerify()
def config_api_list(request):
    """
    List all waiting for the host operating system is installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR'] 

    all_config_api_list = ConfigAPI.objects.all()
    paginator = Paginator(all_config_api_list,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_config_api_list = paginator.page(page)
    except :
        all_config_api_list = paginator.page(paginator.num_pages)

    return render_to_response('config_api_list.html', {'all_config_api_list': all_config_api_list, 'page': page, 'paginator':paginator,'request':request})

@login_required
def config_os_list(request):
    """
    List all waiting for the host operating system is installed
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR'] 

    all_config_os_list = ConfigOS.objects.all()
    paginator = Paginator(all_config_os_list,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_config_os_list = paginator.page(page)
    except :
        all_config_os_list = paginator.page(paginator.num_pages)

    return render_to_response('config_os_list.html', {'all_config_os_list': all_config_os_list, 'page': page, 'paginator':paginator,'request':request})

@login_required
@PermissionVerify()
def get_os_list(request):
    """
    Get information cobbler profiles
    """
    user = request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR'] 
    if request.method == 'GET':
        action = request.get_full_path().split('=')[1]
        if action == 'sync':
            #ConfigOS.objects.all().delete()
            ConfigOS.objects.all().update(isActivated=0) #将所有的cobbler profiles全部设置成禁用模式（0）
            cobbler_apis = ConfigAPI.objects.filter(type = 'cobbler')[:1]
            for cobbler_api in cobbler_apis:
                cobbler_api_url = cobbler_api.url
                cobbler_api_user = cobbler_api.user
                cobbler_api_password = cobbler_api.password
            cobbler = CobblerAPI(url=cobbler_api_url,user=cobbler_api_user,password=cobbler_api_password)
            ret = cobbler.get_proflies()
            for i in ret:
                sql_ret = 1
                sql_ret = ConfigOS.objects.filter(os=i).update(isActivated=1) #将存在的且在cobbler中也存在的设置成enable(1)
                if not sql_ret:
                    ConfigOS.objects.create(os=i,isActivated=1)                
                    Message.objects.create(type='config', action='addOS', action_ip=userip, username=user,content='import %s cobbler profile'%(i))
        return HttpResponseRedirect(reverse('config_os_list'))