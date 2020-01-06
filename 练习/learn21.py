# 题目：给一个不多于5位的正整数，要求：一、求它是几位数，二、逆序打印出各位数字。


def dao(s,l):
  sd = ''
  if l == 0:
    sd = ''
  else:
    sd = s[l-1] + dao(s,l-1)
  return sd

s = input('请输入一个字符串：')
print('它是{}位数，逆序打印出各位数字:{}'.format(len(s),dao(s,len(s))))