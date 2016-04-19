开源运维自动化平台构思
1. 开源运维自动化工具体系：
系统安装部署-Cobbler
配置管理部署--Saltstack
系统应用监控--zabbix
日志收集分析--fluentd or Elasticsearch
 
2. 集成开源自动化系统流程设计
  裸机机房上架--->填写一些预配置信息(后期考虑直接实现"扫一扫")--->交给平台进行系统安装，进度控制等（cobbler的api实现）--->系统安装完成进行初始化和环境部署（saltstack的api完成）--->添加监控（zabbix的api进行监控主机添加）--->最后将详细的信息添加到CMDB中
 
3. 平台已经实现和计划实现功能
装机管理：系统安装，ipmi远程控制，安装进度监控；后期待实现 console的远程调用，权限控制，自动装机VLAN和应用VLAN的切换等；
部署管理：Key的认证管理，Minions状态监测，客户端系统及硬件信息的抓取，应用模块（zabbix,tomcat）的执行，Job状态的监控，及历史job的查询，远程命令的执行等；后期待实现执行权限的控制，危险操作的控制，客户机的分组管理，代码的发布等等；
设备管理：被管理服务器的软硬件信息，机房管理等 ；后期增加主机group管理，IP地址段管理等等
zabbix监控：通过api地址不同的dashboard;
系统管理：api配置文件的管理，同步信息的管理
用户管理：普通用户管理；后期增加第三方认证，权限组管理等
4. Demo Screenshots
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/menu.jpg)
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/install_form.jpg)
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/install_status.jpg)
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/salt_keys.jpg)
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/salt_job.jpg)
![Demo Screenshots](https://github.com/Elivis/opsa-master/blob/master/demo/salt_minions.jpg)






