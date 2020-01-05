# 题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。

import string

s = input('请输入一个字符串：')
letters = 0
space = 0
digit = 0
other = 0

for i in range(0,len(s)):
    if s[i].isalpha():
        letters += 1
    elif s[i].isspace():
        space += 1
    elif s[i].isdigit():
        digit += 1
    else:
        other += 1
        
print('letters=%d,space=%d,digit=%d,other=%d '%(letters,space,digit,other))