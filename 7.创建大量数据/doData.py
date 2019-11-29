#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2019/11/21 16:57
# @Author   : zeroone
# @File     : __init__.py.py
# @Software : PyCharm

import time
import datetime

saveDataNum = 0

baseData1 = r' INSERT INTO `spot_contract_mould`(`id`, `trade_date`, `is_provisional`, `is_internal`, `is_rebuy`, `is_init`, `our_id`, `customer_id`, `customer_title_id`, `ps`, `document_no`, `head_no`, `serial_no`, `prefix`, `suffix`, `commodity_id`, `product_id`, `quantity`, `currency`, `delivery_term`, `payment_term`, `delivery_start_date`, `delivery_end_date`, `due_date`, `due_days`, `pricer`, `term`, `trader_id`, `trader_number`, `spot_type`, `full_no`, `quantity_contractual`, `quantity_delivered`, `quantity_stoarged`, `quantity_priced`, `quantity_hedged`, `quantity_invoiced`, `quantity_of_lots`, `status`, `is_priced`, `is_delivered`, `is_storaged`, `is_invoiced`, `is_has_reversed`, `reversed_id`, `is_parent_contract`, `is_first_upd`, `update_name`, `create_by`, `update_by`, `create_date`, `update_date`, `create_name`, `comments`, `need_files`, `more_less_basis`, `more_less_value`, `loading`, `intermediate`, `discharging`, `is_internal_type`, `qp`, `delivery_cycle`, `unit`, `pricing_type`, `major_market_id`, `major_type`, `major_basis`, `major_start_date`, `major_end_date`, `premium_market_id`, `premium_type`, `premium_basis`, `premium_start_date`, `premium_end_date`, `plan_sale_place`, `major_fixed`, `is_etd_month`, `premium_fixed`, `provisional_water_content`, `provisional_cu_content`, `payable`, `type`, `supply_no`, `ransom`, `bill`, `process`, `rebuy_contract_id`, `is_risk`, `qp_date`) VALUES ( '
baseData2 = '40283f816eb516ec016eb52d7076000c'
baseData3 = ''', '2019-11-14', NULL, NULL, NULL, NULL, 'ff808081682caa2a016830240bf90026', '2c91669d6e166322016e34ce397c081e', '2c91669d6e166322016e34ce397d081f', 'B', 'test_20190702_fp01', NULL, NULL, '', '', '', '4028e5af6d388c71016d38978d830027', NULL, 'USD', 'CIF', 'T/T', NULL, NULL, NULL, NULL, 'US', NULL, '8a8ab0b246dc81120146dc8181950052', '8a8ab0b246dc81120146dc8181950052', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'admin', NULL, '2019-11-29 11:21:24', NULL, '管理员', '', NULL, 'PERCENTAGE', 5.000000000, 'Belgrade', NULL, 'BOR', 'transit', '0', '0', NULL, 'P+F', 'LME', 'P', '', NULL, NULL, 'NA', 'F', NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, '0', '0', '0', NULL, NULL, NULL); '''
baseData4 = ' \n'
dataInfo = ''

# 处理数据
def do_data():
    global saveDataNum
    global dataInfo
    while (saveDataNum < saveDataNumTotal):
        saveDataNum = saveDataNum + 1
        dataInfo = dataInfo + baseData1 + '\'' + baseData2 + str(saveDataNum) + '\'' + baseData3 + baseData4
        print('第'+str(saveDataNum)+'条数据保存成功')

# 将处理好的数据保存到txt文件中
def save_data(dataInfo):
    # if saveDataNum == 1:
    #     # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    #     file_handle = open('data.txt', mode='w')
    # else:
    #     file_handle = open('data.txt', mode='a')
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w')
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass

if __name__ == '__main__':

    # startTime = time.strftime("%Y-%m-%d %H:%M:%S")
    starttime = datetime.datetime.now()
    print(starttime)
    saveDataNumTotal = 30
    do_data()
    save_data(dataInfo)
    # endTime = time.strftime("%Y-%m-%d %H:%M:%S")
    endtime = datetime.datetime.now()
    print(endtime)

    print('\n数据处理成功!所用时间为：' +  str((endtime - starttime).seconds))