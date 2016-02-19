#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from asset.form import *
from asset.models import *
from asset.asset_info import *
from asset.host_info import *
from opsa.mysql import db_operate
from opsa import settings
from opsa.models import *
from UserManage.views.permission import PermissionVerify
from opsa.common.CommonPaginator import SelfPaginator


@login_required
@PermissionVerify()
def host_list_manage(request,id=None):
    """
    Manage Host List
    """
    #if request.method == 'GET':
        #id = request.GET.get('id')
    #get id(GET)
    user = request.user
    if id:
        host_list = get_object_or_404(HostList, pk=id)
        action = 'edit'
        page_name = '编辑主机'
        db = db_operate() 
        sql = 'select ip from asset_hostlist where id = %s' % (id)
        ret = db.mysql_command(settings.opsa_MYSQL,sql)
        
    else:
        host_list = HostList()
        action = 'add'   
        page_name = '新增主机'

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        if delete:
           Message.objects.create(type='host', action='manage', action_ip=id, content='主机下架')
           host_list = get_object_or_404(HostList, pk=id)
           host_list.delete()
           return HttpResponseRedirect(reverse('host_list'))

    if request.method == 'POST': 
        form = HostsListForm(request.POST,instance=host_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('host_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list'))
                else:
                    pass
    else:
        form = HostsListForm(instance=host_list)

    return render_to_response('host_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
            'request':request,
           },context_instance=RequestContext(request))

@login_required
def host_list(request):
    """
    List all Hosts
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
        all_host = HostList.objects.all()         
    else:
        all_host = HostList.objects.filter(hostname__contains=search_fields)   
    paginator = Paginator(all_host,10)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_host = paginator.page(page)
    except :
        all_host = paginator.page(paginator.num_pages)
 
    return render_to_response('host_list.html', {'all_host_list': all_host, 'page': page, 'paginator':paginator,'search':search_fields,'request':request},context_instance=RequestContext(request))

@login_required
@PermissionVerify()
def autoget_host_list(request):
    """
    Get information service assets
    """
    error='fail'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        userip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        userip = request.META['REMOTE_ADDR']
    user = request.user
    if request.method == 'GET':
        action = request.get_full_path().split('=')[1]
        if action == 'flush':
            hostlist_sql = 'select hostname from asset_hostlist'
        elif action == 'partflush':
            hostlist_sql = 'select hostname from asset_hostlist where ip = ""'
        if action and hostlist_sql:
            db = db_operate() 
            host_ret = db.mysql_command(settings.opsa_MYSQL,hostlist_sql)
            
            obj = [i for i in host_ret]       #主机列表数据
            ret = multitle_collect_host(obj)
            for i in ret:
                try:
                    sql_ret = HostList.objects.filter( hostname = i).update(status = ret[i]['status'],version = ret[i]['version'],ip = ret[i]['ip'],cpu_model = ret[i]['cpu_model'],mem = ret[i]['mem'],os_ver = ret[i]['os_ver'],manufacturer = ret[i]['manufacturer'],productname = ret[i]['productname'])
                    error = 'success'
                except Exception as e:
                    error = 'fail' 
                Message.objects.create(type='hostsync', action='grains', action_ip=userip, username=user, content='%s sync %s' % (i,error))
          
        return HttpResponseRedirect(reverse('host_list'))
    
def get_host_grains(request):
    user = request.user
    if request.method == 'GET':
        hostname = request.GET.get('id')
        all_grains = host_grains(hostname)
        #all_grains = ret.items()
            
        return render_to_response('host_grains_list.html', {'hostname':hostname,'all_grains': all_grains,'request':request})

@login_required
@PermissionVerify()    
def get_server_asset(request):
    """
    Get information service assets
    """
    
    if request.method == 'GET':
        action = request.get_full_path().split('=')[1]
        if action == 'flush':
            hostlist_sql = 'select hostname from asset_hostlist'
            server_sql = 'select hostname from asset_serverasset'
            db = db_operate() 
            host_ret = db.mysql_command(settings.opsa_MYSQL,hostlist_sql)
            server_ret = db.mysql_command(settings.opsa_MYSQL,server_sql)
            obj = [i for i in host_ret if i not in server_ret]       #主机列表数据与服务器资产数据IP做差集，数据更新时只更新差集，避免一次性更新全部
            ret = multitle_collect(obj)
            for i in ret:
                ServerAsset.objects.create(manufacturer=i[0], productname=i[1], service_tag=i[2], cpu_model=i[3], cpu_nums=i[4], cpu_groups=i[5],mem=i[6], disk=i[7], raid=i[8], hostname=i[9], ip=i[10], macaddress=i[11], os=i[12], virtual=i[13], idc_name=i[14])
        Message.objects.create(type='server', action='manage', action_ip='扫描', content='录入%s服务器软件、硬件信息' % (obj))
          
        return HttpResponseRedirect(reverse('server_asset_list'))

@login_required
def server_asset_list(request):
    """
    List all Server Asset Info
    """

    user = request.user
    all_server = ServerAsset.objects.all()
    paginator = Paginator(all_server,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_server = paginator.page(page)
    except :
        all_server = paginator.page(paginator.num_pages)

    return render_to_response('server_asset_list.html', {'all_server_list': all_server, 'page': page, 'paginator':paginator,'request':request})

@login_required
@PermissionVerify()
def network_device_discovery(request,id=None):
    """
    Manage Network Device
    """
    
    if id:
        device_list = get_object_or_404(NetworkAsset, pk=id)
        action = 'edit'
        page_name = '编辑设备'
    else:
        device_list = NetworkAsset()
        action = 'add'   
        page_name = '新增设备'

    if request.method == 'POST': 
        form = NetworkAssetForm(request.POST,instance=device_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('network_device_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    return HttpResponseRedirect(reverse('network_device_list'))
                else:
                    pass
    else:
        form = NetworkAssetForm(instance=device_list)

    return render_to_response('device_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
            'request':request,
           },context_instance=RequestContext(request)) 

@login_required
def network_device_list(request):
    """
    List all Network Device
    """
  
    user = request.user
    all_device = NetworkAsset.objects.all()
    paginator = Paginator(all_device,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_device = paginator.page(page)
    except :
        all_device = paginator.page(paginator.num_pages)

    return render_to_response('device_list.html', {'all_device_list': all_device, 'page': page, 'paginator':paginator,'request':request})    

@login_required
@PermissionVerify()
def idc_asset_manage(request,id=None):
    """
    Manage IDC
    """
    user = request.user
    if id:
        idc_list = get_object_or_404(IdcAsset, pk=id)
        action = 'edit'
        page_name = '编辑IDC机房'
    else:
        idc_list = IdcAsset()
        action = 'add'
        page_name = '新增IDC机房'

    if request.method == 'POST':
        form = IdcAssetForm(request.POST,instance=idc_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('idc_asset_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    return HttpResponseRedirect(reverse('idc_asset_list'))
                else:
                    pass
    else:
        form = IdcAssetForm(instance=idc_list)

    return render_to_response('idc_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
            'request':request,
           },context_instance=RequestContext(request))

@login_required
def idc_asset_list(request):
    """
    List all IDC
    """

    user = request.user
    all_idc = IdcAsset.objects.all()
    paginator = Paginator(all_idc,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_idc = paginator.page(page)
    except :
        all_idc = paginator.page(paginator.num_pages)

    return render_to_response('idc_list.html', {'all_idc_list': all_idc, 'page': page, 'paginator':paginator,'request':request})




@login_required
@PermissionVerify()
def AddHostgroups(request):
    if request.method == "POST":
        form = HostgroupsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listhostgroups'))
    else:
        form = HostgroupsForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('hosts/hostgroups.add.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListHostgroups(request):
    mList =Hostgroups.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('hosts/hostgroups.list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditHostgroups(request,ID):
    iRole = Hostgroups.objects.get(id=ID)

    if request.method == "POST":
        form = HostgroupsForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listhostgroups'))
    else:
        form = HostgroupsForm(instance=iRole)

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('hosts/hostgroups.edit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def DeleteHostgroups(request,ID):
    Hostgroups.objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listhostgroups'))
