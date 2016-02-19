# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# import views
from asset.views import *
from opsa.views import *
from installed.views import *
from deploy.views import *
from config.views import *
from api.views import *
from message.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opsa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^opsa/admin/', include(admin.site.urls)),
    #url(r'^login', login, name='login'),
    #url(r'^accounts/login/$', login, name='login'),
    url(r'^logout', logout, name='logout'),
    url(r'^$', index, name='index'),
    url(r'^asset/host_list/$', host_list, name='host_list'),
    url(r'^asset/add_host/$', host_list_manage, name='add_host'),
    url(r'^asset/delete_host/$', host_list_manage, name='delete_host'),
    url(r'^asset/host_manage/(?P<id>\d+)/$', host_list_manage, name='host_manage'),
    url(r'^asset/server_asset/$', server_asset_list, name='server_asset_list'),
    url(r'^asset/server_get/$', get_server_asset, name='get_server_asset'),
    url(r'^asset/grains_get/$', get_host_grains, name='get_host_grains'),
    url(r'^asset/hosts_autget/$', autoget_host_list, name='autoget_host_list'),
    url(r'^asset/device_list/$', network_device_list, name='network_device_list'),
    url(r'^asset/device_add/$', network_device_discovery, name='add_device'),
    url(r'^asset/idc_list/$', idc_asset_list, name='idc_asset_list'),
    url(r'^asset/add_idc/$', idc_asset_manage, name='add_idc'),
    url(r'^asset/listhostgroups/$', ListHostgroups, name='listhostgroups'),
    url(r'^asset/edithostgroups/(?P<ID>\d+)/$', EditHostgroups, name='edithostgroups'),
    url(r'^asset/deletehostgroups/(?P<ID>\d+)/$', DeleteHostgroups,name='deletehostgroups'),
    url(r'^asset/addhostgroups/$', AddHostgroups, name='addhostgroups'),
    url(r'^install/install_list/$', system_install_list, name='install_list'),
    url(r'^install/install_status/$', system_install_status, name='install_status'),
    url(r'^install/install_manage/(?P<id>\d+)/$', system_install_managed, name='install_manage'),
    url(r'^install/add_install/$', system_install_managed, name='add_install'),
    url(r'^install/install_logs/$', install_logs, name='install_logs'),
    url(r'^install/system_install/$',system_install, name='system_install'),
    url(r'^install/ipmi_c/$',ipmi_c, name='ipim_c'),
    url(r'^install/install_record/$',system_install_record, name='install_record'),
    url(r'^install/install_finish/$',system_install_finish, name='install_finish'),
    url(r'^install/install_init/$', deploy_init_status, name='install_init'),
    url(r'^deploy/job_list/$', salt_job_list, name='job_list'),
    url(r'^deploy/minions_status/$', host_list, name='minions_status'),
    url(r'^deploy/job_result/$', salt_job_results, name='job_result'),
    url(r'^deploy/key_list/$', salt_key_list, name='key_list'),
    url(r'^deploy/key_delete/$', salt_delete_key, name='delete_key'),
    url(r'^deploy/key_accept/$', salt_accept_key, name='accept_key'),
    url(r'^deploy/module_deploy/$', module_deploy, name='module_deploy'),
    url(r'^deploy/remote_execution/$', remote_execution, name='remote_execution'),
    url(r'^config/config_api_add/$', config_info, name='config_api_add'),
    url(r'^config/config_api_list/$', config_api_list, name='config_api_list'),
    url(r'^config/config_os_list/$', config_os_list, name='config_os_list'),
    url(r'^config/get_os_list/$', get_os_list, name='get_os_list'),
    url(r'^config/config_api_add/(?P<id>\d+)/$', config_info, name='config_api_add'),
    url(r'^api/install_status_collect/',install_status_collect, name='install_status_collect'),
    url(r'^message/mesg_list/',mesg_list, name='mesg_list'),
    url(r'^accounts/',include('UserManage.urls' )),
    url(r'^hosts/',include('hostmanage.urls' )),
)
