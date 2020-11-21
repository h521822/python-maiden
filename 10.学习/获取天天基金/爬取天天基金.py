#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os
import datetime
import pymysql 
import random 
import time 
from requests import get


# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# referer列表
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/',
    'http://fund.eastmoney.com/110025.html'
]


class mysql_class:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'hj0522'
        self.db = 'hej'


    def ljdb(self):
        self.conn =pymysql.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=3306,charset='utf8') 
        # conn = pymysql.connect(ip, username, pwd, schema,port) 
        self.conn.ping(True)      #使用mysql ping来检查连接,实现超时自动重新连接 
        # print(getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db) 
        self.cur = self.conn.cursor() 

    
    # 插入数据 
    def insertData(self,table, my_dict):
        cols = ', '.join(my_dict.keys()) 
        values = '\',\''.join(my_dict.values())
        sql = "replace into %s (%s) values (%s)" % (table, cols, '\'' + values + '\'') 
        # print(sql)
        self.cur.execute(sql) 
        self.conn.commit()


    def get_html(self,baseUrl):
        # 获取一个随机user_agent和Referer
        headers = {'User-Agent': random.choice(user_agent_list), 'Referer': random.choice(referer_list) }
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        try:
            resp = get(baseUrl, headers=headers)
            # print(resp.status_code)
            if resp.status_code == 200:
                # print(resp.content)
                return resp.text
            print("没有爬取到相应的内容")
            return None
        except RequestException:
            print("没有爬取到相应的内容")
            return None


    def doData(self,jj): 
        jj = jj.replace("\"","")
        info = jj.split(",")
        # fS_code = '000002'
        fS_code = info[0]
        fS_name = info[2]
        jj_type = info[3]
        print(fS_code)

        if '后端' not in fS_name and '162509' <= fS_code:
            stop = random.uniform(2, 5)
            time.sleep(stop)
            v = time.strftime("%Y%m%d%H%M%S",time.localtime())
            baseUrl = "http://fund.eastmoney.com/pingzhongdata/" + fS_code + ".js?v=" + v
            data = self.get_html(baseUrl)

            if data:
                data = data.replace("\'","\"")

                # 基金基本信息
                base_info_com1 = re.findall(re.compile("基金或股票信息\*/(.*?);/\*股票仓位测算图"),data)
                base_info_com2 = re.findall(re.compile("mom-较上期环比\*/(.*?);/\*同类型基金涨幅榜"),data)
                if base_info_com1 and base_info_com2:
                    base_info = base_info_com1[0] + base_info_com2[0]

                    result = {} 
                    result['jj_code']=fS_code
                    result['jj_name']=fS_name
                    result['jj_type']=jj_type
                    result['jj_base_info']=base_info
                    self.insertData('jj_info', result)

  
    def doDatas(self,code): 
        datas = self.get_html("http://fund.eastmoney.com/js/fundcode_search.js")

        datas = datas.replace("var r = [","")
        jj_com = re.compile("\[(.*?)\]")

        jjArr = re.findall(jj_com,datas)
        for jj in jjArr:
            self.doData(jj)


if __name__ == "__main__":

    starttime = datetime.datetime.now()
    print(starttime)

    mysql_class = mysql_class()
    mysql_class.ljdb()          # 连接MySQL
  
    mysql_class.doDatas('004070') 
    
    endtime = datetime.datetime.now()
    print(endtime)

    print('\n数据处理成功!所用时间为：' +  str((endtime - starttime).seconds))
