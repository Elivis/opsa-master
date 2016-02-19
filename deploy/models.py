#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class joblist(models.Model):
    """
    Config api info
    """
    jid = models.CharField(max_length=200, verbose_name=u'jobid')
    fun = models.CharField(max_length=100, verbose_name=u'功能')
    tgt = models.CharField(max_length=255, verbose_name=u'目标主机')
    status = models.CharField(max_length=20, verbose_name=u'状态')
    #create_user = models.CharField(max_length=20, verbose_name=u'创建用户名')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')