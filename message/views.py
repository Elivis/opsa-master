#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from opsa.models import *
from UserManage.views.permission import PermissionVerify
from django.contrib.auth.decorators import login_required
'''
#包含json模块 
try: 
    import json 
except ImportError,e: 
    import simplejson as json 
'''
@login_required
@PermissionVerify()
def mesg_list(request):
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
        all_mesgs = Message.objects.all().order_by('-id')        
    else:        
        if  search_type == 'username':
            all_mesgs = Message.objects.filter(username=search_fields).order_by('-id')
        elif search_type == 'content':
            all_mesgs = Message.objects.filter(content__contains=search_fields).order_by('-id')
        elif search_type == 'type':            
            all_mesgs = Message.objects.filter(type__contains=search_fields).order_by('-id')
        elif search_type == 'action':            
            all_mesgs = Message.objects.filter(fun__contains=search_fields).order_by('-id') 
        
    paginator = Paginator(all_mesgs,20)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_mesgs = paginator.page(page)
    except :
        all_mesgs = paginator.page(paginator.num_pages)
    return render_to_response('message_list.html', {'all_mesgs': all_mesgs, 'page': page, 'paginator':paginator,'search':search_fields,'search_type':search_type,'request':request},context_instance=RequestContext(request)) 