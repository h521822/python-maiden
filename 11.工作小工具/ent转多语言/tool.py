
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

  # 英文
  # for i in arr:
  #   s1 = 'private '
  #   w1 = i.find(s1) + len(s1)
  #   field = i[i.find(' ', w1) + 1: ]
  #   ret = ret + field + ': \'' + field + '\',\n'  
  # # print(ret)

  # 中文
  # ret += '\n\n'
  # for i in arr:
  #   s1 = 'private '
  #   w1 = i.find(s1) + len(s1)
  #   field = i[i.find(' ', w1) + 1: ]
  #   ret = ret + field + ': \'' + i[i.find('/*** ') + len('/*** '): i.find('*/') ] + '\',\n'  
  # print(ret)


  # # 列表
  # # ret += '\n\n'
  # # <el-table-column label="品种" prop="productName" min-width="80" align="left"></el-table-column>
  # # :label="$t('base.futureproduct.fproductName')"
  # for (d,x) in dict.items():
  #   key = d
  #   value = str(x)
  #   ret = ret + '<el-table-column label="'+ key +'" prop="' + value + '" min-width="80" align="left"></el-table-column>\n' 
  #   # ret = ret + '<el-table-column :label="$t(\'base.quoteDockLog.' + value + '\')" prop="' + value + '" min-width="80" align="left"></el-table-column>\n' 
  # print(ret)





  # 后台假数据
  # dto.setFuncDescription("funcDescription");
  for (d,x) in dict.items():
    key = d
    value = str(x)
    ret = ret + 'dto.set' + value[:1].upper() + value[1:] + '("' + value + '");\n'
  print(ret)


  # <el-col :span="12">
  #   <div>
  #     <el-form-item label="合同号" prop="contractNo">
  #       <el-input v-model="saveObj.contractNo" disabled></el-input>
  #     </el-form-item>
  #   </div>
  # </el-col>

  # # 输入框
  # for (d,x) in dict.items():
  #   key = d
  #   value = str(x)
  #   ret += '<!-- ' + key + ' -->\n'
  #   ret +=  '<el-col :span="12"> <div> <el-form-item :label="$t(\'base.quoteDockLog.' + value + '\')" prop="' + value + '"> <el-input v-model="saveObj.' + value + '"></el-input> </el-form-item> </div> </el-col>'
  # # print(ret)


  # ret += '\n\n'
  # # organId: [{ required: true, message: this.$t('contract.contractInfo.product') + this.$t('pay.canNotBeBlank'), trigger: ['blur', 'change'] }],
  # # 必输
  # for (d,x) in dict.items():
  #   key = d
  #   value = str(x)
  #   ret += '// ' + key + '\n'
  #   ret += value + ': [{ required: true, message: this.$t(\'base.quoteDockLog.' + value + '\') + this.$t(\'pay.canNotBeBlank\'), trigger: [\'blur\', \'change\'] }],\n'
  # print(ret)




# 1、数据读取
def openFile():
  with open('open.txt','r',encoding='utf-8') as f:

    dataArr = f.readlines()
    # print(dataArr)
    sData = ''     
    for i in dataArr:
      sData += i.strip()

    arr = sData.split(';')
    dict = {}
    for i in arr:
      if (i.find('/*** ') >= 0):
        s1 = 'private '
        w1 = i.find(s1) + len(s1)
        field = i[i.find(' ', w1) + 1: ]
        title = i[i.find('/***') + len('/***:'): i.find('*/')]
        # print(field)
        # print(title)
        dict[title] = field
      
    # print(dict)

    doData(dict)
    # save_data(sData)
    # print(sData)


# /*** 



if __name__ == "__main__":
  os.chdir(os.path.abspath(os.path.dirname(__file__)))
  openFile()
  print('处理完成')