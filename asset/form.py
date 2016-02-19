#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django import forms
from asset.models import *

class HostsListForm(forms.ModelForm):
    class Meta:
        model = HostList
        exclude = ('add_date',)
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'version': forms.TextInput(attrs={'class': 'form-control'}),
          'application': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
          'cpu_model': forms.TextInput(attrs={'class': 'form-control'}),
          'mem': forms.TextInput(attrs={'class': 'form-control'}),
          'os_ver': forms.TextInput(attrs={'class': 'form-control'}),
          'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
          'productname': forms.TextInput(attrs={'class': 'form-control'}),          
        }

class NetworkAssetForm(forms.ModelForm):
    class Meta:
        model = NetworkAsset
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
          'productname': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'service_tag': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }

class IdcAssetForm(forms.ModelForm):
    class Meta:
        model = IdcAsset
        widgets = {
          'idc_name': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_type': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_location': forms.TextInput(attrs={'class': 'form-control'}),
          'contract_date': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_contacts': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }
class HostgroupsForm(forms.ModelForm):
    class Meta:
        model = Hostgroups
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'hostlist' : forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
            #'permission' : forms.CheckboxSelectMultiple(choices=[(x.id,x.name) for x in PermissionList.objects.all()]),
        }

    def __init__(self,*args,**kwargs):
        super(HostgroupsForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['hostlist'].label=u'主机'
        self.fields['hostlist'].required=False