#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from opsa.common.CommonPaginator import SelfPaginator
from UserManage.views.permission import PermissionVerify

from django.contrib import auth
from django.contrib.auth import get_user_model
from UserManage.models import *
from UserManage.forms import LoginUserForm,ProfileUserForm,ChangePasswordForm,AddUserForm,EditUserForm

def LoginUser(request):
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

@login_required
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def ChangePassword(request):
    if request.method=='POST':
        form = ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logouturl'))
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/password.change.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListUser(request):    
    if request.method == 'POST':
        search_fields = request.POST.get('search')
    else:
        try:
            search_fields = request.GET.get('search','none')
        except ValueError:
            search_fields = 'none'
    if search_fields == 'none':
        all_users = User.objects.all()         
    else:
        all_users = User.objects.filter(username__contains=search_fields)   
    paginator = Paginator(all_users,10)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_users = paginator.page(page)
    except :
        all_users = paginator.page(paginator.num_pages)

    kwvars = {
        'lPage':all_users,
        'request':request,
    }

    return render_to_response('UserManage/user.list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def AddUser(request):

    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            form.save()
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = AddUserForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/user.add.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditUser(request,ID):
    user = get_user_model().objects.get(id = ID)

    if request.method=='POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = EditUserForm(instance=user
        )

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/user.edit.html',kwvars,RequestContext(request))
@login_required
def UserProfile(request):
    user = get_user_model().objects.get(username=request.user)

    if request.method=='POST':
        form = ProfileUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profileurl'))
    else:
        form = ProfileUserForm(instance=user
        )

    kwvars = {
        'ID':user.id,
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/user.profile.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def DeleteUser(request,ID):
    if ID == '1':
        return HttpResponse(u'超级管理员不允许删除!!!')
    else:
        get_user_model().objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listuserurl'))

@login_required
@PermissionVerify()
def ResetPassword(request,ID):
    user = get_user_model().objects.get(id = ID)

    newpassword = get_user_model().objects.make_random_password(length=10,allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
    print '====>ResetPassword:%s-->%s' %(user.username,newpassword)
    user.set_password(newpassword)
    user.save()

    kwvars = {
        'object':user,
        'newpassword':newpassword,
        'request':request,
    }

    return render_to_response('UserManage/password.reset.html',kwvars,RequestContext(request))
