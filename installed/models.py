#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django.db import models
from asset.models import IdcAsset
from config.models import ConfigOS
from config.models import raidscripts
class SystemInstall(models.Model):
    """
    System Install Manage
    """
    STATUS_TAG = (
        ('0','待安装'),
        ('0.5','RAID创建'),
        ('1','PXE启动'),
        ('2','软件包安装'),
        ('3','软件完成安装'),
        ('4','系统环境配置'),
        ('5','完成安装'),
        ('50','启动设置失败'),
        ('51','删除cobbler失败'),
        ('101','删除DTK失败'),
        ('102','重新添加system失败'),
        ('103','raid划分系统安装失败'),
    )
    PV_TAG = (
        ('0','虚拟机'),
        ('1','物理机'),
    )
    #sroom = models.CharField(max_length=1, choices=SHIRT_SIZES)
    sroom = models.ForeignKey(IdcAsset)
    #sroom = models.CharField(max_length=20, verbose_name=u'待装机机房')
    ip = models.IPAddressField(max_length=20, verbose_name=u'待装机IP')
    hostname = models.CharField(max_length=50, verbose_name=u'主机名')
    macaddress = models.CharField(max_length=50, verbose_name=u'MAC地址')
    system_version = models.ForeignKey(ConfigOS)
    status = models.CharField(max_length=20,verbose_name=u'状态',default='0',choices=STATUS_TAG)
    #statusdesc = models.CharField(max_length=40,verbose_name=u'状态描述')
    ipmi_ip = models.IPAddressField(max_length=20, verbose_name=u'IPMIIP',blank='True')
    ipmi_user = models.CharField(max_length=20, verbose_name=u'IPMIUser')
    ipmi_passwd = models.CharField(max_length=20, verbose_name=u'IPMIPasswd')
    install_date = models.DateTimeField(auto_now_add=True, verbose_name=u'安装时间')
    raid_type = models.ForeignKey(raidscripts,default=0)
    pv_type = models.CharField(max_length=20,verbose_name=u'raid_type',default='0',choices=PV_TAG)

    def __unicode__(self):
        return u'%s -- %s' %(self.ip, self.install_date)

    class Meta:
        verbose_name = u'装机列表'
        verbose_name_plural = u'装机列表管理'

class InstallRecord(models.Model):
    """
    Server Install Recored
    """
    sroom = models.ForeignKey(IdcAsset)
    hostname = models.CharField(max_length=60, verbose_name=u'主机名')
    install_date = models.CharField(max_length=20, verbose_name=u'安装时间')
    ip = models.CharField(max_length=20, verbose_name=u'安装IP')
    system_version = models.CharField(max_length=50, verbose_name = '安装操作系统版本')
    username = models.CharField(max_length=20, verbose_name=u'操作人员')

    def __unicode__(self):
        return u'%s - %s' %(self.ip, self.system_version)

    class Meta:
        verbose_name = u'装机记录'
        verbose_name = u'装机记录管理'
