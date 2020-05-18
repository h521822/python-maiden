
#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-


##############################
# 
# 快速生成导出的entity和contract部分
# 
##############################


import os

# 3、数据存储
def save_data(dataInfo):
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w',encoding="utf-8")
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass


# 2、数据处理
def doData(dict):
  ret = ''
  dyh = '\n'
  for (d,x) in dict.items():
    # print("key:" + d + ",value:" + str(x).capitalize())
    # execl.setCustomsDate(DateUtils.str2Date(StringUtil.nvl(rowMap.get("customsDate")), DateUtils.date_sdf));
    # execl.setQuantityAtFactory(StringUtil.big2Zero(rowMap.get("quantityAtFactory")).setScale(6, BigDecimal.ROUND_HALF_UP));
    # String
    ret = ret + '// ' + d + dyh +  'execl.set' + str(x)[:1].upper() + str(x)[1:] + '(StringUtil.nvl(rowMap.get("' + str(x) + '"))); ' + dyh
    # BigDecimal
    # ret = ret + '// ' + d + dyh +  'execl.set' + str(x)[:1].upper() + str(x)[1:] + '(StringUtil.big2Zero(rowMap.get("' + str(x) + '")).setScale(2, BigDecimal.ROUND_HALF_UP)); ' + dyh

  ret = ret + dyh + dyh + dyh + dyh + dyh + dyh
  for (d,x) in dict.items():
    ret = ret + '/** ' + d + ' */' + dyh + '@Excel(name = "' + d + '")' + dyh + 'private String ' + str(x) + ';' + dyh


  # print(ret)
  save_data(ret)


# 1、数据读取
def openFile():
  dict = {}
  with open('open.txt','r',encoding='utf-8') as f:
    dataArr = f.readlines()
    for i in dataArr:
      if (i.find('t:dgCol') >= 0):
        s1 = 'title="'
        s2 = 'field="'
        w1 = i.find(s1) + len(s1)
        w2 = i.find(s2) + len(s2)

        title = i[w1: i.find('"', w1)]
        field = i[w2: i.find('"', w2)]

        dict[title] = field
    doData(dict)
    # print(dict)



if __name__ == "__main__":
  os.chdir(os.path.abspath(os.path.dirname(__file__)))
  openFile()
  print('处理完成')

