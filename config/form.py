#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

from django import forms
from config.models import *

class ConfigAPIForm(forms.ModelForm):
    class Meta:
        model = ConfigAPI
        exclude = ('create_date',)
        widgets = {
          'sroom': forms.Select(attrs={'class': 'form-control'}),
          'url': forms.TextInput(attrs={'class': 'form-control'}),
          'fqdn': forms.TextInput(attrs={'class': 'form-control'}),
          'user': forms.TextInput(attrs={'class': 'form-control'}),
          'password': forms.TextInput(attrs={'class': 'form-control'}),
          'type': forms.TextInput(attrs={'class': 'form-control'}),
          #'create_user': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ConfigOSForm(forms.ModelForm):
    class Meta:
        model = ConfigAPI
        exclude = ('create_date','isActivated',)
        widgets = {
          'os': forms.TextInput(attrs={'class': 'form-control'}),
                    
        }