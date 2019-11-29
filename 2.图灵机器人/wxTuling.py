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


# 读取配置文件
cf = configparser.ConfigParser()
cf.read("./config.ini", encoding='UTF-8')


# 好友名称
my_friend_name = cf.get("configuration", "my_friend_name")
# 群名称
my_qun_name = cf.get("configuration", "my_qun_name")
# 图灵api_key
tuling_api_key = cf.get("configuration", "tuling_api_key")



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


# 微信群名（发送指定的群）
my_girl_group = bot.groups().search(my_qun_name)[0]
@bot.register(chats=my_girl_group, except_self=False)
def reply_my_group(msg):
    # 需要@机器人
    if msg.is_at:
        tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
        tuling.do_reply(msg)

# 微信好友（发送指定的好友）
my_girl_friend = bot.friends().search(my_friend_name)[0]
@bot.register(chats=my_girl_friend)
def reply_my_friend(msg):
    tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
    tuling.do_reply(msg)

# @bot.register()
# def auto_reply(msg):
#
#     # 如果是微信群的话，需要@机器人，好友不需要
#     if isinstance(msg.chat, Group) and not msg.is_at:
#         return
#     else:
#         tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
#         tuling.do_reply(msg)

embed()

