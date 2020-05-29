#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2019/6/25 21:54
# @Author   : zeroone
# @File     : wxpy_wx.py
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
        # 微信群名称
        my_groups = bot.groups().search('机器人测试群')[0]
        print("群主：" + my_groups.owner.name)

        # 发送消息
        my_groups.send(your_message)
        print("消息:" + your_message + "\n发送成功，发送时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))

        # 发送文本
        my_groups.send('Hello, WeChat!')
        # 发送图片
        my_groups.send_image('D:/code.jpg')



    except:

         # 出问题时，发送信息到文件传输助手
        bot.file_helper.send("微信机器人出问题了，赶紧去看看咋回事~")

# 上传文件
def upload_file(path):
    media_id = bot.upload_file(path)
    print(media_id)

    # my_groups = bot.groups().search('机器人测试群')[0]
    # my_groups.send_image("",media_id)


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
    elif('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2, cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")

    print(bot.self.name)
    # 发送信息到文件传输助手，测试是否启动成功
    bot.file_helper.send("微信机器人启动成功！！！" + time.strftime("%Y-%m-%d %H:%M:%S"))

    send_message("测试")

    # upload_file("D:/code.jpg")

    # chromedriver_path = "D:/code.jpg"
    # media_id = bot.upload_file(chromedriver_path)
    # print(media_id)

    # media_id = bot.upload_file(".‪/code.jpg")



    # # 2、读取配置文件
    # cf = configparser.ConfigParser()
    # cf.read("./config.ini", encoding='UTF-8')
    #
    # # 群名称
    # my_qun_name = cf.get("configuration", "my_qun_name")
    # # 发送群公告时间
    # qun_notice_time = cf.get("configuration", "qun_notice_time")
    # # 群公告信息
    # qun_notice_info = cf.get("configuration", "qun_notice_info")

    # # 3、微信机器人相关操作
    # t = Thread(target=start_care, name='start_care')
    # t.start()

# 4、接收微信群消息监听器

# 微信群名
my_groups = bot.groups().search('机器人测试群')[0]
@bot.register(chats=my_groups, except_self=False)
def print_others(msg):
    # my_friend = bot.friends().search('Alex')[0]

    my_mp = bot.mps().search('小冰')[0]

    # 输出聊天内容
    # print(msg)
    print(msg.text)

    if msg.is_at:
        msg.forward(my_mp)

# embed()


# 公众号
my_mp = bot.mps().search('小冰')[0]
@bot.register(chats=my_mp, except_self=False)
def print_others(msg):
    my_friend = bot.friends().search('Alex')[0]

    # 输出聊天内容
    # print(msg)
    print(msg.text)
    msg.forward(my_friend)

embed()


