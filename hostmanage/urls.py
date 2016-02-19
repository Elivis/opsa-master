#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('hostmanage.views',
    url(r'^hostinfo/(?P<id>\d+)/$', 'hostinfo.host_control_info', name='hostinfo'),   
)
