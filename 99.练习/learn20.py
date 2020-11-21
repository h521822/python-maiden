# 利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。


def output(s,l):
    outs = ''
    if l == 0:
        outs = ''
    else:
        outs = s[l-1] + output(s,l-1)
    # print(outs)
    return outs

s = input('请输入需要倒序的字符串：\n')
print(output(s,len(s)))

