#!/usr/bin/python3
#Atuhor:zeroone
# -*- coding: utf-8 -*-
# @Time     : 2019/6/26 23:54
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

if __name__ == "__main__":

    # 1、启动微信机器人
    # 自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if('Windows' in system()):
        # Windows
        # bot = Bot()     # 启动微信机器人
        bot = Bot(cache_path=True)      # 保存缓存，保持登录状态，方便测试
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

    # 2、读取配置文件
    cf = configparser.ConfigParser()
    cf.read("./config.ini", encoding='UTF-8')

    # 公众号
    my_mp_name = cf.get("configuration", "my_mp_name")
    # 群名称
    my_group_name = cf.get("configuration", "my_group_name")
    # 菜单
    menu = cf.get("configuration", "menu")

    # 公众号
    my_mp = bot.mps().search(my_mp_name)[0]
    # 微信群名
    my_group = bot.groups().search(my_group_name)[0]

# 2、接收微信群、公众号消息监听器
@bot.register(chats=my_group, except_self=False)
def print_others(msg):
    # 输出聊天内容
    print(msg.text)
    if msg.is_at:
        if "菜单" in msg.text:
            return menu
        else:
            msg.forward(my_mp)

@bot.register(chats=my_mp, except_self=False)
def print_others(msg):
    print(msg.text)
    print(msg.type)
    print(msg.sender.name)
    if msg.sender.name == "小冰":
        msg.forward(my_group)

embed()     # 进入 Python 命令行


