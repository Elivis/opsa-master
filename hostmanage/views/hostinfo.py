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
from asset.form import *
from asset.models import *
from asset.asset_info import *
from asset.host_info import *
from opsa import settings
from opsa.models import *
from UserManage.views.permission import PermissionVerify
from opsa.common.CommonPaginator import SelfPaginator
import os

@login_required
@PermissionVerify()
def host_control_info(request,id=None):
    """
    Manage Host List
    """
    #if request.method == 'GET':
        #id = request.GET.get('id')
    #get id(GET)
    user = request.user
    if id:
       try:
           hostinfo=HostList.objects.filter(id=id)
           if not hostinfo:
               ret_err = '您查找的%s不正确' % (unicode(id,"utf-8"))
               return render_to_response('error_ret.html', {'ret_err': ret_err,'request':request})
               
       except Exception as e:
        ret_err = '您查找的服务器不正确'
        return render_to_response('error_ret.html', {'ret_err': ret_err,'request':request})   
    else:
        ret_err = '选择错误，请您回退重新选择'
        return render_to_response('error_ret.html', {'ret_err': ret_err,'request':request})
    return render_to_response('hosts/host_control.html',
           {
            'hostinfo':hostinfo,
            'hostid':id,
            'hostname':hostinfo[0].hostname,
            'request':request,
           })