#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2020/1/2 17:33
# @Author   : zeroone
# @File     : yiyanHE.py
# @Software : PyCharm

# 参考文档:https://hitokoto.cn/api

from requests import get
import json
from requests.exceptions import RequestException

baseUrl = 'https://v1.hitokoto.cn/?c=b'

def get_html():
    try:
        resp = get(baseUrl)  # 发送get请求
        print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None


if __name__ == '__main__':
 
    txt = get_html()
    jsonText = json.loads(txt)
    infos = jsonText['hitokoto']
    print(infos)

    print('爬取完成!')