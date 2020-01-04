#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2019/5/26 21:35
# @Author   : zeroone
# @File     : wx_tuling.py
# @Software : PyCharm


# 获取系统信息
from platform import system
import time
# 微信机器人
from wxpy import Bot
# 图灵机器人
from wxpy import Tuling
# 微信机器人调试工具
from wxpy import embed
import configparser
from wxpy import Group
import os
from threading import Thread

from requests import get
import json
from requests.exceptions import RequestException

def get_html():
    try:
        resp = get(yiyan_url)  # 发送get请求
        # print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            jsonText = json.loads(resp.text)
            return jsonText['hitokoto']
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None

# 发送信息
# your_message：信息内容
def send_message(your_message):
    try:
        # 对方的微信名称
        my_friend = bot.groups().search(my_qun_name)[0]

        # 发送消息给对方
        my_friend.send(your_message)
        print("消息:" + your_message + "\n发送成功，发送时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))
    except:
         # 出问题时，发送信息到文件传输助手
        bot.file_helper.send("微信机器人出问题了，赶紧去看看咋回事~")


# 在规定的时间发送群公告
def start_care():
    # 死循环，24小时执行
    while (True):
        print("微信群管理正常，时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))

        now_time = time.ctime()[-13:-8]
        if (now_time == qun_notice_time):
            send_message(get_html())

        now_time_minute = now_time[-2:]

        # 每小时发送信息到文件传输助手，方便监控运行状态
        if(now_time_minute == "16"):
            bot.file_helper.send("微信机器人运行正常~" + time.strftime("%Y-%m-%d %H:%M:%S"))

        # 每60秒检测一次
        time.sleep(60)

if __name__ == '__main__':

    # 1、启动机器人
    if ('Windows' in system()):
        # Windows
        bot = Bot()     # 启动微信机器人
        # bot = Bot(cache_path=True)  # 保存缓存，保持登录状态，方便测试
        bot.file_helper.send("微信机器人启动成功！!" + time.strftime("%Y-%m-%d %H:%M:%S"))
    elif ('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif ('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2, cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")


    # 2、读取配置文件
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    cf = configparser.ConfigParser()
    # PyCharm 能用相对路径，VScode却只能使用绝对路径。暂时不清楚什么原因，当应该不会是编辑器的问题。
    # 解决方法：跳转到配置文件所在的路径。我这将.ini文件和.py文件凡在放在同一路径下，所以跳转到当前路径，也就类似于相对路径了。
    # cf.read("./config.ini", encoding='UTF-8')
    filename = cf.read("configs.ini", encoding='UTF-8')
    # print(filename)

    # 群名称
    my_qun_name = cf.get("configuration", "my_qun_name")
    # 发送群公告时间
    qun_notice_time = cf.get("configuration", "qun_notice_time")
    # 图灵api_key
    tuling_api_key = cf.get("configuration", "tuling_api_key")
    # 一言API地址
    yiyan_url = cf.get("configuration", "yiyan_url")

    

    # 3、微信机器人相关操作
    t = Thread(target=start_care, name='start_care')
    t.start()

# 4、监听指定的微信群，做出相应的回复
# 微信群名（发送指定的群）
my_girl_group = bot.groups().search(my_qun_name)[0]
@bot.register(chats=my_girl_group, except_self=False)
def reply_my_group(msg):

    # 需要@机器人
    if msg.is_at:
        if ("一言" in msg.text):
            send_message(get_html())
        else:
            tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
            tuling.do_reply(msg)


embed()
