#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

html = '/** * 测试数据 * @typ*//*2020-06-25 11:53:29*/var ishb=false;/*基金或股票信息*/var fS_name = "广发双擎升级混合A";var fS_code = "005911";/*原费率*/var fund_sourceRate="1.50";/*现费率*/var fund_Rate="0.15";/*最小申购金额*/var fund_minsg="100";/*基金持仓股票代码*/var stockCodes=["3006012","0000632","6007031","6005361","6005881","0009772","3000142","3005292","0009382","3006612"];/*基金持仓债券代码*/var zqCodes = "";/*基金持仓股票代码(新市场号)*/var stockCodesNew =["0.300601","0.000063","1.600703","1.600536","1.600588","0.000977","0.300014","0.300529","0.000938","0.300661"];/*基金持仓债券代码（新市场号）*/var zqCodesNew = "";/*收益率*//*近一年收益率*/var syl_1n="123.1847";/*近6月收益率*/var syl_6y="37.3726";/*近三月收益率*/var syl_3y="26.5182";/*近一月收益率*/var syl_1y="13.5242";/*股票仓位测算图*/var Data_fundSharesPositions = [[1590336000000,95.00],[1590422400000,95.00],[1590508800000,95.00],[1590595200000,95.00],[1590681600000,95.00],[1590940800000,95.00],[1591027200000,95.00],[1591113600000,95.00],[1591200000000,95.00],[1591286400000,95.00],[1591545600000,95.00],[1591632000000,97.100],[1591718400000,95.00],[1591804800000,95.00],[1591891200000,95.00],[1592150400000,95.00],[1592236800000,84.1300],[1592323200000,81.7400],[1592409600000,83.3700],[1592496000000,98.9900],[1592755200000,98.9900],[1592841600000,98.9900]]'

fS_name_com = re.compile("var fS_name = \"(.*?)\";")
fS_name = re.findall(fS_name_com,html)[0]

print(fS_name)


