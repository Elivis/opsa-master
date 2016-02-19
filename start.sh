#!/bin/bash
#encoding = utf-8

case $1 in
start)
     nohup python  manage.py runserver 0.0.0.0:9000  &
     echo "server is start on 0.0.0.0:9000"
     ;;
stop)
     ps -ef |awk '/0.0.0.0:9000/&& !/awk/ {print $2}'|xargs kill -9
     ;;
*)
     echo "Usage $0 {start|stop}"
     ;;
esac
