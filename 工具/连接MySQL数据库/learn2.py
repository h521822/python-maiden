

import requests
from requests import get
import time
import os
from requests.exceptions import RequestException
import re
import random
import uuid
import pymysql 
#####################################
# 
# 获取所有基金代码
# 
#####################################



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

host = 'localhost'
user = 'root'
passwd = 'hj0522'
db = 'hej'
table = 'jj_dd_info'


if __name__ == "__main__":

    # 获取一个随机user_agent和Referer
    headers = {'User-Agent': random.choice(user_agent_list),
                'Referer': random.choice(referer_list)
    }

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 访问网页接口
    req = requests.get('http://fund.eastmoney.com/js/fundcode_search.js', timeout=5, headers=headers)

    # 获取所有基金代码
    fund_code = req.content.decode()
    fund_code = fund_code.replace("﻿var r = [","").replace("];","")
    # print(type(fund_code))
    # 正则批量提取
    codeList = re.findall(r"[\[](.*?)[\]]", fund_code)


    conn =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8') 
    conn.ping(True)      #使用mysql ping来检查连接,实现超时自动重新连接 
    cur = conn.cursor() 

    for d in codeList:
        dList = d.replace('"','').split(',')

        result = {} 
        result['id']=str(uuid.uuid1())
        result['jj_code']=dList[0]
        result['jj_name']=dList[2]
        result['jj_type']=dList[3]

        cols = ', '.join(result.keys()) 
        values = '","'.join(result.values())
        # print(values)
        sql = "replace into %s (%s) values (%s)" % (table, cols, '"' + values + '"') 
        # print(sql)
        cur.execute(sql) 
        conn.commit()




