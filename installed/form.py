#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django import forms
from installed.models import SystemInstall

class SystemInstallForm(forms.ModelForm):
    class Meta:
        model = SystemInstall
        #filter = isActivated
        exclude = ('install_date',)
        pv_type = forms.ChoiceField(widget=forms.RadioSelect)
        #ipmi_user = forms.CharField(label='ipmi_user',initial='root',widget=forms.TextInput(attrs={'class': 'form-control'}))
        widgets = {
          'sroom': forms.Select(attrs={'class': 'form-control'}),
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'macaddress': forms.TextInput(attrs={'class': 'form-control'}),
          'system_version': forms.Select(attrs={'class': 'form-control'}),
          'ipmi_ip': forms.TextInput(attrs={'class': 'form-control'}),
          'ipmi_user': forms.TextInput(attrs={'class': 'form-control'}),
          'ipmi_passwd': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.Select(attrs={'class': 'form-control','readOnly':'true'}),
          #'statusdesc': forms.TextInput(attrs={'class': 'form-control','readOnly':'true'}),
          'raid_type': forms.Select(attrs={'class': 'form-control','data-toggle':'#phipmi'}),
                    
        }