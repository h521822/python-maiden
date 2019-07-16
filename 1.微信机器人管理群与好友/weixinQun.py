#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2019/5/26 14:54
# @Author   : zeroone
# @File     : weixin_qun.py
# @Software : PyCharm

# 获取系统信息
from platform import system
import time
# 微信机器人
from wxpy import Bot
# 微信机器人调试工具
from wxpy import embed
import configparser
from threading import Thread


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
            send_message(qun_notice_info)

        now_time_minute = now_time[-2:]

        # 每小时发送信息到文件传输助手，方便监控运行状态
        if(now_time_minute == "16"):
            bot.file_helper.send("微信机器人运行正常~")

        # 每60秒检测一次
        time.sleep(60)

if __name__ == "__main__":

    # 1、启动微信机器人
    # 自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if('Windows' in system()):
        # Windows
        # bot = Bot()     # 启动微信机器人
        bot = Bot(cache_path=True)      # 保存缓存，保持登录状态，方便测试
        # embed()  # 进入 Python 命令行
        # 发送信息到文件传输助手，测试是否启动成功
        bot.file_helper.send("微信机器人启动成功！!" + time.strftime("%Y-%m-%d %H:%M:%S"))
    elif('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2, cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")

    # 2、读取配置文件
    cf = configparser.ConfigParser()
    cf.read("./config.ini", encoding='UTF-8')

    # 群名称
    my_qun_name = cf.get("configuration", "my_qun_name")
    # 发送群公告时间
    qun_notice_time = cf.get("configuration", "qun_notice_time")
    # 群公告信息
    qun_notice_info = cf.get("configuration", "qun_notice_info")

    # 3、微信机器人相关操作
    t = Thread(target=start_care, name='start_care')
    t.start()


# 4、接收微信群消息监听器

# 微信群名
my_girl_group = bot.groups().search(my_qun_name)[0]
@bot.register(chats=my_girl_group, except_self=False)
def print_others(msg):
    # 输出聊天内容
    print(msg)
    print(msg.text)
    
