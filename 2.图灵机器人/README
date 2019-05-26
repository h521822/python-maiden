# 通过图灵机器人为微信群增加乐趣

---
## 简介

有些群人太少，为了增加一定的活跃度，想到了给微信群加个机器人。  
人多的大群，也可以利用机器人管理，如：自动邀请进群、违规自动踢人...

这里也写了自动回复指定好友的消息，主要是避免得被女朋友嫌弃罅隙回复的慢/手动滑稽

## 编写思路
为了方便快速开发，我们使用python中的wxpy模块完成微信的基本操作。  
首先，，我们设置一个`config.ini`配置文件，并从这个配置文件开始读取信息。

```ini
[configuration]

# 设置好友的微信名称，记住，不是微信ID也不是微信备注
# 注意：没有的话，把名字注释掉
my_friend_name = Alex

# 设置微信群名称
# 注意：没有的话，把名字注释掉
my_qun_name = 机器人测试群

# 机器人名称
robot_name = 机器人

# 图灵api_key
# 图灵机器人官网注册获取apikey。地址：http: // www.tuling123.com /
tuling_api_key = 5279ee06a58b4db8880fa6c44949b33c
```

这里的内容还不够丰富,你也可以接入其他的网站,自己进行封装

接着，开启微信机器人，为了程序的健壮性，自动判断一下操作系统，根据不同操作系统执行不同指令
```python
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
```

接收微信群信息，并调用图灵机器人进行自动回复
1. 回复指定的微信群
```python
# 微信群名
my_girl_group = bot.groups().search(my_qun_name)[0]
@bot.register(chats=my_girl_group, except_self=False)
def reply_my_group(msg):
    # 需要@机器人
    if (robot_name in msg.text):
        tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
        tuling.do_reply(msg)
```

2. 回复指定的微信好友
```python
my_girl_friend = bot.friends().search(my_friend_name)[0]
@bot.register(chats=my_girl_friend)
def reply_my_friend(msg):
    tuling = Tuling(api_key=tuling_api_key)  # ***填你的图灵api_key
    tuling.do_reply(msg)
```

当然仅仅写以上内容，会导致你的程序主程序运行结束自然退出。  
wxpy给出了embed()方法，在程序末尾（或其他你想要暂停调试的地方）加上embed()方法就可以让程序保持运行，同时进入Python命令行。
```python
# 进入 Python 命令行、让程序保持运行
# 推荐使用
embed()

# 或者仅仅堵塞线程
# bot.join()
```

## 完整源代码
项目源代码在 [GitHub仓库](https://github.com/h521822/python-maiden)  
项目持续更新，欢迎您[star本项目](https://github.com/h521822/python-maiden)


