#!/usr/bin/python3#Atuhor:zeroone# -*- coding: utf-8 -*-# @Time     : 2019/5/26 21:35# @Author   : zeroone# @File     : wx_tuling.py# @Software : PyCharm# 获取系统信息from platform import systemimport time# 微信机器人from wxpy import Bot# 图灵机器人from wxpy import Tuling# 微信机器人调试工具from wxpy import embedimport configparserfrom threading import Threadif __name__ == '__main__':    # 1、启动机器人    if ('Windows' in system()):        # Windows        bot = Bot()     # 启动微信机器人        # bot = Bot(cache_path=True)  # 保存缓存，保持登录状态，方便测试        bot.file_helper.send("微信机器人启动成功！!" + time.strftime("%Y-%m-%d %H:%M:%S"))    elif ('Darwin' in system()):        # MacOSX        bot = Bot()    elif ('Linux' in system()):        # Linux        bot = Bot(console_qr=2, cache_path=True)    else:        # 自行确定        print("无法识别你的操作系统类型，请自己设置")# 微信群名# my_girl_group = bot.groups().search("美团红包群")[0]my_girl_group = bot.groups().search("遗忘之城")[0]@bot.register(chats=my_girl_group, except_self=False)def reply_my_group(msg):    if ("@机器人" in msg.text):        tuling = Tuling(api_key='5279ee06a58b4db8880fa6c44949b33c')  # ***填你的图灵api_key        tuling.do_reply(msg)# my_girl_friend = bot.friends().search("A3")[0]# @bot.register(chats=my_girl_friend)# def reply_my_friend(msg):#     tuling = Tuling(api_key='5279ee06a58b4db8880fa6c44949b33c')  # ***填你的图灵api_key#     tuling.do_reply(msg)embed()