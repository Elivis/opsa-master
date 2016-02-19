#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Elivis.Zhang <elivis.zhang@aliyun.com>
# QQ Group：99798703
# Created on Aug 8, 2015
# -*- coding: utf-8 -*-

import json
import time

# Import salt modules
import salt.config
import salt.utils.event

# Import third party libs
import MySQLdb

__opts__ = salt.config.client_config('/etc/salt/master')

# Create MySQL connect
conn = MySQLdb.connect(host=__opts__['mysql.host'], user=__opts__['mysql.user'], passwd=__opts__['mysql.pass'], db=__opts__['mysql.db'], port=__opts__['mysql.port'])
cursor = conn.cursor()
conn2 = MySQLdb.connect(host=__opts__['mysql.host'], user='opsa', passwd='opsa', db='opsa', port=__opts__['mysql.port'])
cursor2 = conn2.cursor()
# Listen Salt Master Event System
event = salt.utils.event.MasterEvent(__opts__['sock_dir'])
for eachevent in event.iter_events(full=True):
    ret = eachevent['data']
    if "salt/job/" in eachevent['tag']:
        # Return Event
        if ret.has_key('id') and ret.has_key('return'):
            # Igonre saltutil.find_job event
            if ret['fun'] == "saltutil.find_job":
                continue

            sql = '''INSERT INTO `salt_returns`
                (`fun`, `jid`, `returns`, `id`, `success`, `full_ret` )
                VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (ret['fun'], ret['jid'],
                                 json.dumps(ret['return']), ret['id'],
                                 ret['success'], json.dumps(ret)))
            cursor.execute("COMMIT")
            cursor2.execute('select count(*) from deploy_joblist where jid = %s and tgt = %s', (ret['jid'],ret['id']))
            count_rows = cursor2.fetchall()
            create_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            for i in count_rows:
                value=int(i[0])
                #print value
                if value == 0 :
                    sql3 = '''INSERT INTO deploy_joblist (`fun`,`tgt`,`status`,`jid`,`create_date`) VALUES (%s, %s, %s, %s,%s)'''
                    #print sql3
                    cursor2.execute(sql3, (ret['fun'],ret['id'],ret['success'],ret['jid'],create_date))
                    cursor2.execute("COMMIT")
                else:
                    sql2 = '''update deploy_joblist set status=%s where jid =%s'''
                    cursor2.execute(sql2, (ret['success'],ret['jid']))
                    cursor2.execute("COMMIT")
                
                
            
    # Other Event
    else:
        pass
