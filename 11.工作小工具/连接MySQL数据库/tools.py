#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import time
import datetime
import uuid
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from requests import get
import json
from email.mime.text import MIMEText
import smtplib
from email.header import Header
import random
import pandas as pd
from sqlalchemy import create_engine


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

# referer列表
referer_list_hx = [
    'http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=161725&startdate=2017-05-10',
    'http://funds.hexun.com/',
    'http://jingzhi.funds.hexun.com/110011.shtml',
    'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode=110011'
]


class mysql_class:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'hj0522'
        self.db = 'hej'
        self.codeList = ['000961']
        self.mbcb = 1       # 目标成本

    def ljdb(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=3306, charset='utf8')
        # conn = pymysql.connect(ip, username, pwd, schema,port)
        self.conn.ping(True)  # 使用mysql ping来检查连接,实现超时自动重新连接
        # print(getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db)
        self.cur = self.conn.cursor()

    # 删除数据
    def deleteData(self):
        sql = "delete from jj_history where ly = 'tt'"
        self.cur.execute(sql)
        self.conn.commit()

    # 插入数据
    def insertData(self, table, my_dict):
        # print(my_dict)
        # print(my_dict['jj_code'])
        cols = ', '.join(my_dict.keys())
        values = '","'.join(my_dict.values())
        sql = "replace into %s (%s) values (%s)" % (table, cols, '"' + values + '"')
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()

    def get_html(self, baseUrl, headers):
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

    # 和讯。历史数据比较全，但是更新太慢
    def get_hx_data(self, code):
        yesterday = self.getYesterday()
        sqlYD = "select * from jj_history where jj_code = '" + code + "' and riqi = '" + str(yesterday) + "'"
        rYD = self.cur.execute(sqlYD)           # 返回条数
        # 如果不存在昨天的数据，才爬取和讯
        if rYD == 0:

            # 获取一个随机user_agent和Referer
            headers = {'User-Agent': random.choice(user_agent_list),
                       'Referer': random.choice(referer_list_hx)
                       }

            baseUrl = "http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=" + code + "&enddate=2025-05-15"
            soup = BeautifulSoup(self.get_html(baseUrl, headers), 'lxml')
            # 数据格式化
            trs = soup.select('.m_table > tbody > tr')
            # for tr in trs:
            for i in range(len(trs)):
                tr = trs[i]
                result = {}
                tds = tr.select('td')
                # print(tds)
                tdInfo = [td.get_text() for td in tds]

                result['id'] = str(uuid.uuid1())
                result['jj_code'] = code
                result['ly'] = 'hx'
                result['riqi'] = tdInfo[0]
                result['dwjz'] = tdInfo[1]
                result['ljjz'] = tdInfo[2]
                result['zdf'] = str(float(tdInfo[3].strip('%'))/100)
                result['create_date'] = self.getCurrentTime()
                # result['mmfe']='2'
                # result['mmjz']='2'
                # result['mmje']='2'
                # result['pjcb']='2'
                # result['comments']='2'

                sql = "select * from jj_history where jj_code = '" + code + "' and riqi = '" + tdInfo[0] + "'"
                r = self.cur.execute(sql)           # 返回条数
                if i == 0:
                    if r == 0:
                        self.insertData('jj_history', result)
                    else:
                        continue
                else:
                    if r == 0:
                        self.insertData('jj_history', result)
                    else:
                        break
        self.get_ttjj_data(code)

    # 天天基金。更新快，并且有估值。但是数据量少

    def get_ttjj_data(self, code):

        t = time.time()
        rt = int(round(t * 1000))

        # 获取一个随机user_agent和Referer
        headers = {'User-Agent': random.choice(user_agent_list),
                   'Referer': random.choice(referer_list)
                   }

        # 获取最新的估值
        # rt(毫秒级时间撮)，不用也能访问。但是我们尽量默认真实访问
        baseUrl = "http://fundgz.1234567.com.cn/js/" + code + ".js?rt=" + str(rt)

        # 查询首页所有信息
        # url = "http://fund.eastmoney.com/" + code + ".html?spm=search"

        txt = self.get_html(baseUrl, headers)
        # print(txt)
        jsonText = json.loads(txt[txt.find("{"):txt.find("}") + 1])
        # print(jsonText)
        name = jsonText['name']     # 基金名称
        jzrq = jsonText['jzrq']     # 上个交易日的日期
        dwjz = jsonText['dwjz']     # 上个交易日的单位净值
        gsz = jsonText['gsz']       # 最近一个交易日的单位净值估值
        gszzl = jsonText['gszzl']   # 最近一个交易日的日涨跌幅
        gztime = jsonText['gztime'][:10]  # 最近一个交易日的日期

        # sql = "update jj_history set jj_name = '" + name + "' where jj_code = '" + code + "'"
        # self.cur.execute(sql)

        sql1 = "select * from jj_history where jj_code = '" + code + "' and riqi = '" + gztime + "'"
        r1 = self.cur.execute(sql1)           # 返回条数
        # print(r1)
        if r1 == 0:
            result = {}
            result['id'] = str(uuid.uuid1())
            result['jj_code'] = code
            result['jj_name'] = name
            result['ly'] = 'tt'
            result['riqi'] = gztime
            result['dwjz'] = gsz
            result['zdf'] = gszzl
            result['create_date'] = self.getCurrentTime()
            self.insertData('jj_history', result)

            sql2 = "select * from jj_history where jj_code = '" + code + "' and riqi = '" + jzrq + "'"
            r2 = self.cur.execute(sql2)           # 返回条数
            if r2 == 0:
                result = {}
                result['id'] = str(uuid.uuid1())
                result['jj_code'] = code
                result['jj_name'] = name
                result['ly'] = 'tt'
                result['riqi'] = jzrq
                result['dwjz'] = dwjz
                result['create_date'] = self.getCurrentTime()
                self.insertData('jj_history', result)

    # 数据爬取
    def saveData(self):
        self.deleteData()        # 删除从天天基金爬来的数据
        for code in self.codeList:
            print("{}爬取开始".format(code))
            stop = random.uniform(3, 6)
            time.sleep(stop)
            self.get_hx_data(code)

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def getYesterday(self):
        # 获取昨天的日期
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        return yesterday

    # 数据处理
    def doData(self):
        # self.selectData('000961')
        msg_text = ''
        for code in self.codeList:
            print("{}处理开始".format(code))
            msg_text += self.selectData(code)
        self.send_sms(msg_text)

    # 数据处理
    def selectData(self, code):
        # engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
        engine = create_engine("mysql+pymysql://root:" + self.passwd + "@localhost:3306/" + self.db)
        # sql = "select riqi as date,ifnull(jj_name,'') as name,dwjz as unitNet from jj_history where jj_code = '" + code + "' ORDER BY riqi"
        sql = "select his.riqi as date,ifnull(info.jj_name,'') as name,his.dwjz as unitNet from jj_history his left join jj_dd_info info on info.jj_code = his.jj_code where his.jj_code = '" + code + "' ORDER BY his.riqi"
        df = pd.read_sql_query(sql, engine)
        # print(df)
        # print(df.info())

        # CCI指标
        # 获取5日均线
        df['ma5'] = df['unitNet'].rolling(5).mean()

        # 6、计算布林线指标
        # 中轨（20日均线）
        df['g1'] = df['unitNet'].rolling(20).mean()
        # 数据1     (净值-中轨)的平方
        # df['s1'] = (df['unitNet'] - df['g1']) * (df['unitNet'] - df['g1'])
        df['s1'] = (df['unitNet'] - df['g1']) ** 2
        # 数据2     数据1的20日均线
        df['s2'] = df['s1'].rolling(20).mean()
        # 数据3     数据2的平方根
        df['s3'] = df['s2'] ** 0.5
        # 上轨      中轨+2*数据3
        df['g2'] = df['g1'] + 2 * df['s3']
        # 下轨      中轨-2*数据3
        df['g3'] = df['g1'] - 2 * df['s3']
        # =(2*[@单位净值2]-[@上轨]-[@下轨])/[@单位净值2]
        # 量能柱
        df['lnz'] = (2*df['unitNet']-df['g2']-df['g3'])/df['unitNet']
        # [@中轨]+([@上轨]-[@中轨])*0.309
        # 高位止盈线
        df['gwvyx'] = df['g1']+(df['g2']-df['g1'])*0.309
        # =[@中轨]-([@中轨]-[@下轨])*0.309
        # 低位加仓线
        df['dwjcx'] = df['g1']-(df['g1']-df['g3'])*0.309

        # 去除缺失行
        df = df.dropna()
        for i in range(1, len(df)):
            # print(df[i:i+1])

            # 当天
            d = df[i:i+1]
            # d = df.iloc[i]
            # 昨天
            d1 = df[i-1:i]
            # d1 = df.iloc[i-1]

            # print(d)
            # print(d1)

            # IF(AND(E4>G4,[@单位净值2]<[@上轨]),"清仓"
            if float(d1['unitNet']) > float(d1['g2']) and float(d['unitNet']) < float(d['g2']):
                # print(d.index)
                # d['ypck'] = "清仓"
                df.loc[d.index, 'ypck'] = "清仓"
                # print(d['unitNet'])
            # IF(AND(E4>M4,E4<G4,[@单位净值2]<[@高位止盈线]),"止盈赎回"
            elif float(d1['unitNet']) > float(d1['gwvyx']) and float(d1['unitNet']) < float(d1['g2']) and float(d['unitNet']) < float(d['gwvyx']):
                df.loc[d.index, 'ypck'] = "止盈赎回"
            # IF([@单位净值2]>[@低位加仓线],"观望期",
            elif float(d['unitNet']) > float(d['dwjcx']):
                df.loc[d.index, 'ypck'] = "观望期"
            # IF([@单位净值2]>[@下轨],"可加仓","探底加仓")
            elif float(d['unitNet']) > float(d['g3']):
                df.loc[d.index, 'ypck'] = "可加仓"
            else:
                df.loc[d.index, 'ypck'] = "探底加仓"

            if i > 30:

                # 计算CCI值
                # =(B2-SUM(H2:H31)/30)/AVEDEV(H2:H31)/0.015
                # 平均值：mean()        平均绝对偏差：mad()         苦恼mad()不能和rolling()一同使用
                ddf = df[i-29:i+1]
                df.loc[d.index, 'cci'] = (d['unitNet'] - ddf['ma5'].mean()) / ddf['ma5'].mad() / 0.015

        # print(df)
        # print(df.iloc[-1]['name'])
        # print(df.iloc[-1]['ypck'])
        return df.iloc[-1]['name'] + '   ' + df.iloc[-1]['ypck'] + '   ' + str(round(df.iloc[-1]['cci'], 2)) + '\n'
        # return code + '   ' + df.iloc[-1]['ypck'] + '   ' + str(round(df.iloc[-1]['cci'],2)) + '\n'

    # 发送消息到邮箱
    def send_sms(self, msg_text):
        # 第三方 SMTP 服务
        mail_host = "smtp.126.com"  # 设置服务器
        mail_user = "he521822@126.com"  # 用户名
        # mail_pass = "hj123456"  # 口令（是授权码，不是登录密码）
        mail_pass = "ZTHDVBGWWTIGJJEW"  # 口令（是授权码，不是登录密码）

        sender = 'he521822@126.com'     # 发送人邮箱，必须与 mail_user 一致
        receivers = ['h521822@126.com', '1665521822@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        subject = '大吉大利晚上吃鸡'    # 标题
        msg_from = 'hej<h22@126.com>'   # 发件人(Tim为发送人名称，可以为空；<>为发送人邮箱，可以为空，可任意伪装)
        msg_to = 'h521822@126.com,1665521822@qq.com'   # 收件人，必须与 receivers 一致
        # msg_text = '现在是' + now + '，明天记得下午五点开会！'     # 发送内容

        message = MIMEText(msg_text, 'plain', 'utf-8')  # 邮箱内容
        message['From'] = msg_from
        message['To'] = msg_to

        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())    # 发送人，收件人，内容
            print("邮件发送成功")

        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

    # 做T，计算买入金额
    def doTmr(self, code):

        engine = create_engine("mysql+pymysql://root:" + self.passwd + "@localhost:3306/" + self.db)
        sql = ""
        sql += " select han.riqi,han.jj_code,info.jj_name,han.ccfe,han.cccb,his.dwjz from jj_handle han                                                                  "
        sql += " left join (select t.jj_code,t.riqi,t.dwjz from jj_history t where t.jj_code = '" + code + "' ORDER BY t.riqi desc LIMIT 1) his on han.jj_code = his.jj_code   "
        sql += " left join jj_dd_info info on info.jj_code = han.jj_code                                                                                                 "
        sql += " where han.jj_code = '" + code + "' ORDER BY han.riqi desc LIMIT 1                                                                                             "
        df = pd.read_sql_query(sql, engine)
        df = df.dropna()
        # print(df)
        mrData = df.iloc[0]
        # print(mrData)

        mrData = df.iloc[0]
        # print(type(mrData['cccb']))

        # 根据目标成本，计算需要买入多少金额
        # 追加份额 = (持仓成本 - 目标成本) * 持仓份额 / (目标成本 - 当前净值)
        mrfe = (mrData['cccb'] - self.mbcb) * mrData['ccfe'] / (self.mbcb - mrData['dwjz'])
        # print(mrfe)
        mrje = mrfe * mrData['dwjz']
        # print(mrje)
        print("将{}的成本降低到{}，需要买入{}元".format(mrData['jj_name'], self.mbcb, mrje))

    # 做T，计算卖出份额
    def doTmc(self, code):
        # 当前净值 大于 做T的平均持仓成本 的百分之一时，卖出做T时的所有份额
        engine = create_engine("mysql+pymysql://root:" + self.passwd + "@localhost:3306/" + self.db)
        sql = ""
        sql += " SELECT                                                                                                                                                                        "
        sql += " 		han_mr.riqi,han_mr.jj_code,info.jj_name,han_mr.mrje,his.dwjz,zx.dwjz as zxjz                                                                                    "
        sql += " FROM                                                                                                                                                                          "
        sql += " 		jj_handle han_mr                                                                                                                                               "
        sql += " 		LEFT JOIN jj_history his ON his.jj_code = han_mr.jj_code                                                                                                       "
        sql += " 		AND his.riqi = han_mr.riqi                                                                                                                                     "
        sql += " 		left join (select t.jj_code,t.riqi,t.dwjz from jj_history t where t.jj_code = '" + code + "' ORDER BY t.riqi desc LIMIT 1) zx on zx.jj_code = his.jj_code            "
        sql += " 		left join jj_dd_info info on info.jj_code = han_mr.jj_code                                                                                                     "
        sql += " WHERE                                                                                                                                                                         "
        sql += " 		han_mr.riqi > ( SELECT han_mc.riqi FROM jj_handle han_mc WHERE han_mc.jj_code = '" + code + "' AND han_mc.t_type = 'mc' ORDER BY han_mc.riqi DESC LIMIT 1 )          "

        df = pd.read_sql_query(sql, engine)
        df = df.dropna()

        sum_ccje = 0
        sum_ccfe = 0
        for i in range(len(df)):
            mr = df.iloc[i]
            sum_ccje += mr['mrje']
            sum_ccfe += mr['mrje'] / mr['dwjz']
        # print(sum_ccje)
        # print(sum_ccfe)
        # 做T的平局成本
        avg_tcb = sum_ccje / sum_ccfe

        mrData = df.iloc[0]
        ylRate = (mrData['zxjz'] - avg_tcb) / avg_tcb
        ylAmt = round((mrData['zxjz'] - avg_tcb) * sum_ccfe, 2)
        # print(ylAmt)
        if ylRate >= 0.01:
            # if avg_tcb * (1 + 0.01) < mrData['zxjz']:
            print("{}的当前盈利{},平均成本为：{}，卖出份额：{},可赚{}元".format(mrData['jj_name'], "%.2f%%" % (ylRate * 100), avg_tcb, sum_ccfe, ylAmt))
        # elif avg_tcb * (1 - 0.01) < mrData['zxjz']:
        elif ylRate <= -0.01:
            print("{}当前盈利率{}，当前盈利率{}，可考虑加仓".format(mrData['jj_name'], ylAmt, "%.2f%%" % (ylRate * 100)))
        else:
            print("{}当前盈利{}，当前盈利率{}，观望".format(mrData['jj_name'], ylAmt, "%.2f%%" % (ylRate * 100)))


if __name__ == "__main__":

    starttime = datetime.datetime.now()
    print(starttime)

    mysql_class = mysql_class()
    mysql_class.ljdb()          # 连接MySQL
    mysql_class.codeList = ['001548', '000961', '000962',         # 50/300/500
                            '000071',       # 恒生

                            '001508', '000727', '000751',     # 动力灵活、健康灵活、嘉实新兴产业

                            '161721',       # 招商地产      （不打算持有了）

                            '001631',       # 食品饮料
                            '161725',       # 白酒
                            '320007',       # 诺安
                            '001618',       # 电子
                            '004070',       # 证券
                            '001595',       # 银行

                            '166002',       # 中欧蓝筹
                            '163402',       # 兴全趋势
                            '519697',       # 交银优势

                            '005224']       # 基建工程

    # mysql_class.codeList = ['000961']       # 基建工程

    # mysql_class.saveData()        # 数据获取并保存到MySQL数据库
    # mysql_class.doData()        # 数据处理

    # 目标买入
    # mysql_class.mbcb = 0.94
    # mysql_class.doTmr('004070')
    # T卖出
    mysql_class.doTmc('004070')

    endtime = datetime.datetime.now()
    print(endtime)

    print('\n数据处理成功!所用时间为：' + str((endtime - starttime).seconds))
