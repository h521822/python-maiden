#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pymysql 
import time 
import uuid

def getCurrentTime(): 
    # 获取当前时间 
    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())) 

# 查询
def db_select(host, user, passwd, db,port=3306,charset='utf8'): 
    conn =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8') 
    #conn = pymysql.connect(ip, username, pwd, schema,port) 
    conn.ping(True)      #使用mysql ping来检查连接,实现超时自动重新连接 
    # print(getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db) 
    cur = conn.cursor() 
    sql = "select * from jj_history"
    result = cur.execute(sql)           # 返回条数
    dataslist = cur.fetchall()
    # print(result)
    print(dataslist)
    cur.close()
    conn.close()

    sum = 0
    for data in dataslist:
        for d in data:
            print(d)
        # print(data[i])
        # sum += data[3]
    # print(sum)

def db_insert(host, user, passwd, db,port=3306,charset='utf8'): 
    conn =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8') 
    #conn = pymysql.connect(ip, username, pwd, schema,port) 
    conn.ping(True)      #使用mysql ping来检查连接,实现超时自动重新连接 
    # print(getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db) 
    cur = conn.cursor() 
    id = uuid.uuid1()
    sql = "INSERT INTO `jj_history`(`id`, `riqi`, `dwjz`, `ljjz`, `zdf`, `mmfe`, `mmjz`, `mmje`, `pjcb`, `comments`) VALUES ('" + str(id) + "', '3', 41.000000000, 4.000000000, 2.000000000, 2.000000000, 2.000000000, 4.000000000, 3.000000000, '2')"
    result = cur.execute(sql)           # 返回条数
    # insert_id = conn.insert_id() 
    conn.commit() 
    # print(insert_id)


if __name__ == "__main__":
    # db_select('localhost', 'root', 'hj0522', 'hej') 
    db_insert('localhost', 'root', 'hj0522', 'hej') 