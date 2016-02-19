#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-


from sys import path
#from Tkconstants import FALSE
if 'deploy' not in path:
    path.append(r'deploy')
from deploy.saltapi import SaltAPI
#import saltapi
from opsa import settings
import threading

host_info = {}

def autoget_host_info(tgt):
    '''
    Salt API得到资产信息，进行格式化输出
    '''
    global host_info
    info = {}
    grains_ret = False
    #ver_info = []
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    try:
        ret = sapi.remote_noarg_execution(tgt,'test.ping')
    except Exception as e:
        ret = False
    if ret:
        try:
            grains_ret = sapi.remote_noarg_execution(tgt,'grains.items')
        except Exception as e:
            grains_ret = False
    if grains_ret:
        info['ip'] =  grains_ret['ip'].split('/')[0]
        info['version'] = grains_ret['saltversioninfo']
        info['cpu_model'] = grains_ret['cpu_model']
        info['mem'] = grains_ret['mem_total']
        info['os_ver'] = grains_ret['os']+'_'+grains_ret['osrelease']+'_'+grains_ret['osarch']
        info['manufacturer'] = grains_ret['manufacturer']
        info['productname'] = grains_ret['productname']
    else:
        info['ip'] =  ''
        info['version'] = ''
        info['cpu_model'] = ''
        info['mem'] = ''
        info['os_ver'] = ''
        info['manufacturer'] = ''
        info['productname'] = ''   
        
     
    info['hostname'] = tgt
    info['status'] = ret
    host_info[info['hostname']] = info
    
def host_grains(tgt):
    '''
    Salt API得到grains信息，进行格式化输出
    '''
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    ret = sapi.remote_noarg_execution(tgt,'grains.items')
    return ret

def multitle_collect_host(tgt):
    global host_info
    #全局变量置空,避免多次请求的时候返回结果叠加
    host_info = {}
    threads = []
    loop = 0
    numtgt = len(tgt)
    print numtgt
    for i in range(0, numtgt, 2):
        nkeys = range(loop*2, (loop+1)*2, 1)
        #实例化线程
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                t = threading.Thread(target=autoget_host_info, args=(tgt[i],))
                threads.append(t)
        #启动线程
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                threads[i].start()
        #等待并发线程结束
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                threads[i].join()
        loop = loop + 1
    return host_info

'''
if __name__ == '__main__':
    print multitle_collect(['test-02', 'test-01'])
'''
