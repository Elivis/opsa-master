#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from opsa.models import Users
from asset.models import *

class UserForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

def index(request):
    '''验证用户是否通过认证 '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    '''获取登录用户名'''
    username=request.session.get('username')
    print username
    #return render_to_response('index.html')
    host_up_count = HostList.objects.filter(status='True').count()
    host_nosync_count = HostList.objects.filter(status='').count()
    host_down_count = HostList.objects.filter(status='False').count()
    return render_to_response('index.html',{'host_down_count':host_down_count,'host_up_count':host_up_count,'host_nosync_count':host_nosync_count,'request':request})
'''
def login(request):
    message = " "
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username is not None and password is not None:
            user=auth.authenticate(username=username,password=password)
            print username,password
            if user is not None and user.is_active:
                auth.login(request,user)
                #设置用户的session
                request.session['username']=username
                return HttpResponseRedirect('/')
            else:
                message = "用户名或密码错误"              
        else:
            #return HttpResponseRedirect('/login/')
            message = "用户名或密码不能为空"
    #判断是否已经登录
    #if req.user.is_authenticated() and req.session['username'] is not None:
    #    return HttpResponseRedirect('/')
        
    return  render_to_response('login.html',{'message':message},context_instance=RequestContext(request))
'''
def logout(request):
    session = request.session.get('username',False)
    if session:
        print "delete session",request.session.get('username')
        auth.logout(request)
        #del request.session['username']        
        #return render_to_response('logout.html',{'username':session})
        return HttpResponseRedirect('/accounts/login/')
    else:
        return HttpResponseRedirect('/accounts/login/')