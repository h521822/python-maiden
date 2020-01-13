# 下划线转驼峰

import os

# 3、数据存储
def save_data(dataInfo):
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w')
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass

# 2、数据处理
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
  save_data(res)

# 1、数据读取
def openFile():
  with open('open.txt','r',encoding='utf8') as f:
    data = f.read()
    str2Hump(data)

if __name__ == "__main__":
  os.chdir(os.path.abspath(os.path.dirname(__file__)))
  openFile()
  print('处理完成')





