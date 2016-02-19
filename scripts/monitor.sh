#!/bin/bash
PIDS=`ps -ef |grep salt_event_to_mysql.py |grep -v grep | awk '{print $2}'`
if [ "$PIDS" == "" ]; then
/usr/bin/python /var/www/html/ops/opsa-master/scripts/salt_event_to_mysql.py&
fi
