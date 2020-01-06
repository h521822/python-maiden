# 题目：一个5位数，判断它是不是回文数。即12321是回文数，个位与万位相同，十位与千位相同。


def hui(s):
  flag = '是'
  for i in range(len(s)//2):
      if s[i] != s[len(s) - i -1]:
        flag = '不是'
  return flag

s = int(input('请输入一个5位数：'))
print('{}{}回文数'.format(s,hui(str(s))))