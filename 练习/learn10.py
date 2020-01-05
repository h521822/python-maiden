# 题目：利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。

score = int(input('int:'))
# grade = score >= 90?'a':'b'
if score >= 90 :
    grade = 'A'
elif score >= 60:
    grade = 'B'
else:
    grade = 'C'


print('%d 属于 %s' % (score,grade))
print('{} 属于 {}'.format(score,grade))
print('{0} 属于 {1}'.format(score,grade))
