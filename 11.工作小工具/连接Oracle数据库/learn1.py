#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import cx_Oracle  #导入模块
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'        # 解决中文乱码问题

###############################################################################
# oracle数据库连接基础
# 
# 基本使用流程:
# 1. 引用模块cx_Oracle
# 2. 连接数据库
# 3. 获取cursor
# 4. 使用cursor进行各种操作
# 5. 关闭cursor
# 6. 关闭连接
# 
# 连接Oracle数据库，需要配置Oracle的环境变量，instantclient版本与Python版本一致，我这里都使用64位
# instantclient64位下载地址点击
# 详情参考:https:// https://blog.csdn.net/guimaxingmc/article/details/80360840
# 
###############################################################################



# 连接数据库
# 连接user/passwd@host:端口/instance
conn = cx_Oracle.connect('prm_wb_test6/prm_wb_test6@192.168.101.75:1521/sm2')
# conn = cx_Oracle.connect(connectString, encoding = "UTF-8", nencoding = "UTF-8")             # 解决中文乱码问题 
# 创建游标对象
c = conn.cursor()
# 执行命令
# x = c.execute('select sysdate from dual')
x = c.execute("select t1.column_name,data_type,comments from (    select table_name,column_name,data_type,data_default,nullable from user_tab_cols where Table_Name='WB_TBL_QUOTE_DOCK_LOG'  )t1 RIGHT JOIN  (     select column_name,comments from user_col_comments where Table_Name='WB_TBL_QUOTE_DOCK_LOG' )t2 on t1.column_name=t2.column_name") 
# data = x.fetchone()       # 返回单个元组，如果查询不到结果，则返回None(也就是只返回一条数据)
# print(data)

data = x.fetchall()         # 返回二维元组，如果查询不到结果，则返回()
# print(data)
# 关闭游标对象
c.close()
# 关闭连接
conn.close()


for f in data:
    print(f)
    # print(f[0])
    for i in range(len(f)):
        print(f[i])