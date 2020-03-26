# 将福利饭的文章处理成markdown

import os

# 2、数据存储
def save_data(dataInfo):
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w',encoding="utf-8")
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass


# 1、数据读取
def openFile():
  with open('open.txt','r',encoding='utf-8') as f:
    dataArr = f.readlines()
    sData = ''  
    for i in dataArr:
      sData += i

    save_data(
      sData[sData.find('<div id="main-content" class="outerbox clr">'):sData.find('<section class="meta clearfix" id="single-meta">')]
      + 
      sData[sData.find('<article class="entry single-post-article clearfix">'):sData.find('<div id="single-author" class="clearfix">')]
      + 
      '\n[飞猫云](' + sData[sData.find('http://www.fmpan.com'):sData.find('" class="wpex-twitter" title="飞猫云"')] + ')'
      )



if __name__ == "__main__":
  os.chdir(os.path.abspath(os.path.dirname(__file__)))
  openFile()
  print('处理完成')