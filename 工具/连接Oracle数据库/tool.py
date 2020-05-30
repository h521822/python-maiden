#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import cx_Oracle  #导入模块
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'        # 解决中文乱码问题

###############################################################################
# 
# oracle数据库连接及工具的使用
# 
# 1. 生成相应的基础代码
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

arrs = []
for f in data:
    arr = []
    for i in range(len(f)):
        if i == 0 :
            title = f[0].title().replace('_','')
            col = title[0].lower() + title[1:]
            # print(col)
            arr.append(col)
        else :
            arr.append(f[i])
    arr.append(title)
    arrs.append(arr)

# print(arrs)






ret = '***************多语言（英文）******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    ret += column_name + ': \'' + column_name + '\',\n'  
ret += '***************多语言（英文）******end*******************'
print(ret)

ret = '***************多语言（中文）******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    ret += column_name + ': \'' + comments + '\',\n'  
ret += '***************多语言（中文）******end*******************'
print(ret)


ret = '***************多语言（列表）******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    # ret = ret + '<el-table-column label="'+ key +'" prop="' + value + '" min-width="80" align="left"></el-table-column>\n' 
    ret += '<!-- ' + comments + ' -->\n'
    ret = ret + '<el-table-column :label="$t(\'base.quoteDockLog.' + column_name + '\')" prop="' + column_name + '" min-width="80" align="left"></el-table-column>\n' 
ret += '***************多语言（列表）******end*******************'
print(ret)

ret = '***************后台假数据（列表）******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    title = f[3]
    # ret += '<!-- ' + comments + ' -->\n'
    ret = ret + 'dto.set' + title + '("' + column_name + '");     // ' + comments + '\n'
ret += '***************后台假数据（列表）******end*******************'
print(ret)


ret = '***************前端编辑画面******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    title = f[3]
    ret += '<!-- ' + comments + ' -->\n'
    ret +=  '<el-col :span="12"> <div> <el-form-item :label="$t(\'base.quoteDockLog.' + column_name + '\')" prop="' + column_name + '"> <el-input v-model="saveObj.' + column_name + '"></el-input> </el-form-item> </div> </el-col>\n'
 
ret += '***************前端编辑画面******end*******************'
print(ret)


ret = '***************前端编辑画面验证******start*******************\n'
for f in arrs:
    column_name = f[0]
    data_type = f[1]
    comments = f[2]
    title = f[3]
    ret += '// ' + comments + '\n'
    ret += column_name + ': [{ required: true, message: this.$t(\'base.quoteDockLog.' + column_name + '\') + this.$t(\'pay.canNotBeBlank\'), trigger: [\'blur\', \'change\'] }],\n'
ret += '***************前端编辑画面验证******end*******************'
print(ret)

