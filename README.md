#企望制造ERP系统 RCE漏洞 POC  

由于企望制造 ERP comboxstore.action接口权限设置不当，默认的配置可执行任意SQL语句，利用xp_cmdshell函数可远程执行命令，未经认证的攻击者可通过该漏洞获取服务器权限。  

```
Usage:
  python3 Hope_Erp.py -h
```
