# 将MyBatis中的问号，替换为实际参数
# 类似idea的插件MyBatis Log Pligin

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
def doData(sData,cData):
  ret = ''
  dyl = ' \''
  dyr = '\' '

  arr = sData.split('?')
  i = cData.find('Parameters') + len('Parameters:')
  parameters = cData[i:]
  sArr = parameters.split(',')
  for i in range(len(arr)):
    s = arr[i].strip()
    if i == 0:
      ret = s[s.find('Preparing') + len('Preparing:'): ]
    else:
      p = sArr[i-1]
      c = p[:p.find('(')].strip()     # 参数
      t = p[p.find('(')+1:p.find(')')].strip()   # 类型
      ret = ret + dyl + c + dyr + s

  save_data(ret)


def str2Hump(data):
  arr = data.lower().split('_')
  res = ''
  j = 0
  for i in arr:
      if j == 0:
          res = i
      else:
          res = res + i[0].upper() + i[1:]
      j += 1
  return res
  # save_data(res)


# 1、数据读取
def openFile():
  with open('open.txt','r',encoding='utf-8') as f:

    dataArr = f.readlines()
    sData = '' 
    # for i in dataArr:
    #   v = i[i.find('WB_TBL_FUT_RECEIPT_JOIN"."') + len('WB_TBL_FUT_RECEIPT_JOIN"."'): i.find('" IS')]
    #   k = i[i.find('IS \'') + len('IS \''): i.find('\';')]
    #   # print(v)
    #   # print(k)
    #   sData = '/** \n* ' + k + '\n */ \n @TableField("' + v + '") \n private String ' + str2Hump(v) + ';\n' + sData + 'public static final String ' + v + ' = "' + v + '";\n'


    for i in dataArr:
      v = i[i.find('WB_TBL_FUT_RECEIPT_JOIN"."') + len('WB_TBL_FUT_RECEIPT_JOIN"."'): i.find('" IS')]
      k = i[i.find('IS \'') + len('IS \''): i.find('\';')]
      sData += '/** \n* ' + k + '\n */ \n @ApiModelProperty(value = "' + k + '") \n private String ' + str2Hump(v) + ';\n' 

    print(sData)




    #   if (i.find('Parameters') >= 0):
    #     cData = i
    #     break
    #   else:
    #     # sData += i.strip()     # 因为eclipse打印出来的log每一行会有个空格。。。
    #     sData += i[:-1]     # 因为eclipse打印出来的log每一行会有个空格。。。
    # doData(sData,cData)



if __name__ == "__main__":
  os.chdir(os.path.abspath(os.path.dirname(__file__)))
  openFile()
  print('处理完成')