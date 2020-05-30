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



class db_class:
    # 初始化（连接数据库，并获取数据）
    def __init__(self):
        self.tableName = 'WB_TBL_QUOTE_DOCK_LOG'
        self.multilingual = 'base.quoteDockLog'


    def db_data(self):
        # 连接数据库
        # 连接user/passwd@host:端口/instance
        conn = cx_Oracle.connect('prm_wb_test6/prm_wb_test6@192.168.101.75:1521/sm2')
        # conn = cx_Oracle.connect(connectString, encoding = "UTF-8", nencoding = "UTF-8")             # 解决中文乱码问题 
        # 创建游标对象
        c = conn.cursor()
        # 执行命令
        # x = c.execute('select sysdate from dual')
        x = c.execute("SELECT t1.column_name, t1.data_type, t2.comments FROM	user_tab_cols t1 left join user_col_comments t2 ON t1.table_name = t2.table_name 	AND t1.column_name = t2.column_name WHERE	t1.Table_Name = '" + self.tableName + "' 	AND t1.column_name NOT IN ( 'DELETE_FLAG', 'CREATE_USER', 'CREATE_DATE', 'UPDATE_USER', 'UPDATE_DATE', 'VERSION_NUM', 'ID' )") 
        # data = x.fetchone()       # 返回单个元组，如果查询不到结果，则返回None(也就是只返回一条数据)
        # print(data)

        self.data = x.fetchall()         # 返回二维元组，如果查询不到结果，则返回()
        # print(data)
        # 关闭游标对象
        c.close()
        # 关闭连接
        conn.close()


    # 下划线转驼峰
    def str2Hump(self):
        self.arrs = []
        for f in self.data:
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
            self.arrs.append(arr)


    def do1(self):
        ret = '***************多语言（英文）******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            ret += column_name + ': \'' + column_name + '\',\n'  
        ret += '***************多语言（英文）******end*******************'
        print(ret)


    def do2(self):
        ret = '***************多语言（中文）******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            ret += column_name + ': \'' + comments + '\',\n'  
        ret += '***************多语言（中文）******end*******************'
        print(ret)

    def do3(self):
        ret = '***************多语言（列表）******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            # ret = ret + '<el-table-column label="'+ key +'" prop="' + value + '" min-width="80" align="left"></el-table-column>\n' 
            ret += '<!-- ' + comments + ' -->\n'
            ret = ret + '<el-table-column :label="$t(\'' + self.multilingual + '.' + column_name + '\')" prop="' + column_name + '" min-width="80" align="left"></el-table-column>\n' 
        ret += '***************多语言（列表）******end*******************'
        print(ret)
    
    def do4(self):
        ret = '***************后台假数据（列表）******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            title = f[3]
            # ret += '<!-- ' + comments + ' -->\n'
            ret = ret + 'dto.set' + title + '("' + column_name + '");     // ' + comments + '\n'
        ret += '***************后台假数据（列表）******end*******************'
        print(ret)

    def do5(self):
        ret = '***************前端编辑画面******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            title = f[3]
            ret += '<!-- ' + comments + ' -->\n'
            ret +=  '<el-col :span="12"> <div> <el-form-item :label="$t(\'' + self.multilingual + '.' + column_name + '\')" prop="' + column_name + '"> <el-input v-model="saveObj.' + column_name + '"></el-input> </el-form-item> </div> </el-col>\n'
        
        ret += '***************前端编辑画面******end*******************'
        print(ret)

    def do6(self):
        ret = '***************前端编辑画面验证******start*******************\n'
        for f in self.arrs:
            column_name = f[0]
            data_type = f[1]
            comments = f[2]
            title = f[3]
            ret += '// ' + comments + '\n'
            ret += column_name + ': [{ required: true, message: this.$t(\'' + self.multilingual + '.' + column_name + '\') + this.$t(\'pay.canNotBeBlank\'), trigger: [\'blur\', \'change\'] }],\n'
        ret += '***************前端编辑画面验证******end*******************'
        print(ret)



if __name__ == "__main__":
    db = db_class()
    db.tableName = 'WB_TBL_QUOTE_CU_CONTRACT'
    db.db_data()
    db.str2Hump()
    # db.do1()
    db.do2()
    # db.do3()
    # db.do4()
    # db.do5()
    # db.do6()