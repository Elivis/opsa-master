#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.db import models
from asset.models import IdcAsset
class ConfigAPI(models.Model):
    """
    Config api info
    """
    sroom = models.ForeignKey(IdcAsset)
    #sroom = models.CharField(max_length=20, verbose_name=u'待装机机房')
    url = models.CharField(max_length=200, verbose_name=u'API的URL')
    fqdn = models.CharField(max_length=100, verbose_name=u'API的FQDN')
    user = models.CharField(max_length=20, verbose_name=u'API用户')
    password = models.CharField(max_length=20, verbose_name=u'API的密码')
    type = models.CharField(max_length=20, verbose_name=u'操作系统')
    #create_user = models.CharField(max_length=20, verbose_name=u'创建用户名')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
class ConfigOS(models.Model):
    """
    Config cobbler info
    """
    os = models.CharField(max_length=200, verbose_name=u'操作系统')
    isActivated = models.BooleanField(verbose_name = u'是否激活')
    #create_user = models.CharField(max_length=20, verbose_name=u'创建用户名')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    def __unicode__(self):
        return u'%s' %(self.os)
 
    class Meta:
        verbose_name = u'配置信息管理'
        verbose_name_plural = u'API列表管理'
class raidscripts(models.Model):
    """
    Config cobbler info
    """
    name = models.CharField(max_length=20, verbose_name=u'名称')
    script = models.BooleanField(verbose_name = u'是否激活')
    other = models.BooleanField(verbose_name = u'是否激活')
    #create_user = models.CharField(max_length=20, verbose_name=u'创建用户名')
    #create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    def __unicode__(self):
        return u'%s' %(self.name)
 
    class Meta:
        verbose_name = u'配置信息管理'
        verbose_name_plural = u'API列表管理'