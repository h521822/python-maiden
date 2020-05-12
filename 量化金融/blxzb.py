# -*- coding:utf-8 -*-

from requests import post
from requests import get
import random
import json
import time
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import math
import matplotlib.pyplot as plt
# matplotlib.use('agg')
plt.style.use('bmh') 

import numpy as np
import baostock as bs

#############################
# 
# 量化金融，用数据科学投资（布林线指标）
# 
#############################





class blxzb_class:
    # 初始化一些数据
    def __init__(self):
        # 基金或者股票代码
        self.code = 'sh.000001'
        # 开始时间
        self.start_date = ''
        # 结束时间（没有就空着）
        self.end_date = ''
        # 是否获取最新数据(默认为false)
        self.isNew = False
        self.isPlt = False
        

    # 1、获取数据
    def getDate(self):
        if self.isNew:
            # 登陆系统
            lg = bs.login()
            # 显示登陆返回信息
            # print('login respond error_code:'+lg.error_code)
            # print('login respond  error_msg:'+lg.error_msg)
            
            # 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
            # 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
            # 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
            # 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
            # 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
            # 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
            # 成长指数，例如：sz.399376 小盘成长 等；
            # 价值指数，例如：sh.000029 180价值 等；
            # 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；

            # 详细指标参数，参见“历史行情指标参数”章节
            rs = bs.query_history_k_data_plus(self.code,
                # 成交数量:volume
                "date,close,pctChg,volume",
                # "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                start_date=self.start_date, end_date=self.end_date, frequency="d")
            # print('query_history_k_data_plus respond error_code:'+rs.error_code)
            # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

            # 打印结果集
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            self.df = pd.DataFrame(data_list, columns=rs.fields)
            # 结果集输出到csv文件
            self.df.to_csv(self.code + ".csv", index=False)
            # print(self.df)

            # 登出系统
            bs.logout()
        else:
            # 读取数据
            self.df = pd.read_csv(self.code + '.csv',index_col='date')


    # 2、获取5日均线、30日均线
    def ma5ma30(self):
        # .rolling(5)   一次滚动5个单位
        # .mean()       均值
        self.df['ma5'] = self.df['close'].rolling(5).mean()
        self.df['ma30'] = self.df['close'].rolling(30).mean()

        # print(self.df)
        # 去除缺失行
        self.df = self.df.dropna()
        # print(self.df)


    # 6、计算布林线指标
    def js_blxzb(self):
        # 6、计算布林线指标
        # 中轨（20日均线）
        self.df['g1'] = self.df['close'].rolling(20).mean()
        # 数据1     (净值-中轨)的平方
        self.df['s1'] = (self.df['close'].astype(float) - self.df['g1'].astype(float)) ** 2
        # 数据2     数据1的20日均线
        self.df['s2'] = self.df['s1'].rolling(20).mean()
        # 数据3     数据2的平方根
        self.df['s3'] = self.df['s2'] ** 0.5 
        # 上轨      中轨+2*数据3
        self.df['g2'] = self.df['g1'] + 2 * self.df['s3']
        # 下轨      中轨-2*数据3
        self.df['g3'] = self.df['g1'] - 2 * self.df['s3']
        # =(2*[@单位净值2]-[@上轨]-[@下轨])/[@单位净值2]
        # 量能柱
        self.df['lnz'] = (2 * self.df['close'].astype(float) - self.df['g2'].astype(float) - self.df['g3'].astype(float))/self.df['close'].astype(float)
        # [@中轨]+([@上轨]-[@中轨])*0.309
        # 高位止盈线
        self.df['gwvyx'] = self.df['g1']+(self.df['g2']-self.df['g1'])*0.309
        # =[@中轨]-([@中轨]-[@下轨])*0.309
        # 低位加仓线
        self.df['dwjcx'] = self.df['g1']-(self.df['g1']-self.df['g3'])*0.309

        # 去除缺失行
        self.df = self.df.dropna()
        for i in range(1,len(self.df)):
            # print(self.df[i:i+1])
            
            # 当天
            d = self.df[i:i+1]
            # 昨天
            d1 = self.df[i-1:i]
            # print(d)
            # print(d1)

            # IF(AND(E4>G4,[@单位净值2]<[@上轨]),"清仓"
            if float(d1['close']) > float(d1['g2']) and float(d['close']) < float(d['g2']):
                # print(d.index)
                # d['ypck'] = "清仓"
                self.df.loc[d.index,'ypck'] = "清仓"
                # print(d['close'])
            # IF(AND(E4>M4,E4<G4,[@单位净值2]<[@高位止盈线]),"止盈赎回"
            elif float(d1['close']) > float(d1['gwvyx']) and float(d1['close']) < float(d1['g2']) and float(d['close']) < float(d['gwvyx']):
                self.df.loc[d.index,'ypck'] = "止盈赎回"
            # IF([@单位净值2]>[@低位加仓线],"观望期",
            elif float(d['close']) > float(d['dwjcx']):
                self.df.loc[d.index,'ypck'] = "观望期"
            # IF([@单位净值2]>[@下轨],"可加仓","探底加仓")
            elif float(d['close']) > float(d['g3']):
                self.df.loc[d.index,'ypck'] = "可加仓"
            else:
                self.df.loc[d.index,'ypck'] = "探底加仓"

            
        self.df.drop(['s1','s2','s3'],axis=1,inplace=True)
        # print(self.df)
        # 保存数据
        # self.df.to_csv('4444444444444.csv')

        # self.df = self.df[-50:]
        self.df[['close','g1','g2','g3','lnz','gwvyx','dwjcx']].plot()
        # matplotlib显示
        # plt.style.use('bmh')
        if self.isPlt:
            plt.show()

        self.df = self.df[-30:]
        print(self.df)
        # self.df.to_csv('4444444444444.csv')

    




if __name__ == '__main__':
   

    blxzb_class = blxzb_class()
    # # sh.000065	上证龙头
    # blxzb_class.code = 'sh.000065'
    # # sz.399101	中小板综	中小板综合指数
    # blxzb_class.code = 'sz.399101'
    # sz.399102	创业板综	创业板综指
    # blxzb_class.code = 'sz.399102'
    # # sz.399231	农林指数	农林牧渔指数
    # blxzb_class.code = 'sz.399231'
    # # sz.399235	建筑指数	建筑业指数
    # blxzb_class.code = 'sz.399235'
    # # sz.399239	IT指数	信息技术指数
    # blxzb_class.code = 'sz.399239'
    # # sz.399240	金融指数	金融业指数
    # blxzb_class.code = 'sz.399240'
    # # sz.399395	国证有色	国证有色指数
    # blxzb_class.code = 'sz.399240'
    # # sz.399437	国证证券	国证证券行业指数
    # blxzb_class.code = 'sz.399437'
    # # sz.399417	新能源车	国证新能源车指数
    # blxzb_class.code = 'sz.399417'
    # sz.399389	国证通信	国证通信指数
    # blxzb_class.code = 'sz.399389'
    # sh.000998	中证TMT	中证TMT产业主题指数(电子)
    blxzb_class.code = 'sh.000998'



    blxzb_class.isNew = True
    # blxzb_class.isPlt = True
     

    # # 白酒
    # code = '161725'
    # # 50
    # code = '001548'
    # # 证券
    # code = '004070'
    # # 银行
    # code = '001594'
    # # 恒生
    # code = '000071'


    # 1、获取数据
    blxzb_class.getDate()
    # 2、获取5日均线、30日均线
    blxzb_class.ma5ma30()
    # 3、获取5日均线、30日均线
    blxzb_class.js_blxzb()

    print('\n列表爬取成功!')

 # sh.000006	地产指数
    # sz.399101	中小板综	中小板综合指数
    # sz.399102	创业板综	创业板综指
    # sz.399231	农林指数	农林牧渔指数
    # sz.399235	建筑指数	建筑业指数
    # sz.399239	IT指数	信息技术指数
    # sz.399240	金融指数	金融业指数
    # 
    # sh.000016	上证50	上证50指数
    # sh.000300	沪深300	沪深300指数
    # sh.000905	中证500	中证小盘500指数
    # 
    # sz.399006	创业板指	创业板指数P
    # sz.399012	创业300	创业板300
  
#   一级行业指数
    # 
    # sh.000032	上证能源	上证能源行业指数
    # sh.000033	上证材料	上证原材料行业指数
    # sh.000034	上证工业	上证工业行业指数
    # sh.000035	上证可选	上证可选消费行业指数
    # sh.000036	上证消费	上证主要消费行业指数
    # sh.000037	上证医药	上证医药卫生行业指数
    # sh.000038	上证金融	上证金融地产行业指数
    # sh.000039	上证信息	上证信息技术行业指数
    # sh.000040	上证电信	上证电信业务行业指数
    # sh.000041	上证公用	上证公用事业行业指数
    # 
    # sh.000986	全指能源	中证全指能源指数	
    # sh.000987	全指材料	中证全指原材料指数	
    # sh.000989	全指可选	中证全指可选消费指数	
    # sh.000990	全指消费	中证全指主要消费指数	
    # sh.000991	全指医药	中证全指医药卫生指数	
    # sh.000992	全指金融	中证全指金融地产指数	
    # sh.000993	全指信息	中证全指信息技术指数
    # 
    # sz.399908	300 能源	沪深300能源指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于能源行业的全部股票构成指数成份股。
    # sz.399909	300 材料	沪深300原材料指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于原材料行业的全部股票构成指数成份股。
    # sz.399910	300 工业	沪深300工业指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于工业行业的全部股票构成指数成份股。
    # sz.399911	300 可选	沪深300可选消费指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于可选消费行业的全部股票构成指数成份股。
    # sz.399912	300 消费	沪深300主要消费指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于主要消费行业的全部股票构成指数成份股。
    # sz.399913	300 医药	沪深300医药卫生指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于医药卫生行业的全部股票构成指数成份股。
    # sz.399914	300 金融	沪深300金融地产指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于金融地产行业的全部股票构成指数成份股。
    # sz.399915	300 信息	沪深300信息技术指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于信息技术行业的全部股票构成指数成份股。
    # sz.399916	300 电信	沪深300电信业务指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于电信行业的全部股票构成指数成份股。
    # sz.399917	300 公用	沪深300公用事业指数
    # 
    # 
# 主题指数
    # 
    # sh.000015	红利指数	上证红利指数	2005/1/4	上海证券交易所	挑选在上交所上市的现金股息率高、分红比较稳定、具有一定规模及流动性的50只股票作为样本，以反映上海证券市场高红利股票的整体状况和走势。
    # sh.000018	180金融	上证180金融股指数	2007/12/10	上海证券交易所	以上证180指数样本股中银行、保险、证券和信托等行业的股票构成样本股，反映上海证券市场的金融股走势。
    # sh.000019	治理指数	上证公司治理指数	2008/1/2	上海证券交易所	以上证公司治理板块的股票作为样本股，目的是鼓励和促进上市公司进一步改善公司治理，提升上市公司的整体质量。
    # sh.000021	180治理	上证180公司治理指数	2008/9/10	上海证券交易所	从上证180指数与上证公司治理指数样本股中挑选100只规模大、流动性好的股票作为样本股，以反映上证180指数中治理状况良好公司股票的走势。
    # sh.000025	180基建	上证180基建指数	2008/12/15	上海证券交易所	从上证180指数中挑选拥有、管理基础设施和从事基础设施建设的公司股票组成样本股，以反映上海证券市场基建类股票的整体走势。
    # sh.000026	180资源	上证180资源指数
    # sh.000065	上证龙头	上证龙头企业指数
    # 
    # 
    # 
    # 