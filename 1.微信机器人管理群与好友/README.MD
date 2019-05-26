# 每天不同时间段给好友或者群发送消息

---
## 简介

每天给微信群或好友定时发送消息。  
大家个自行丰富代码，比如：每隔一个小时发一次群公告、设置多个时间段24小时关怀女友

## 编写思路
为了方便快速开发，我们使用python中的wxpy模块完成微信的基本操作。  
首先，，我们设置一个`config.ini`配置文件，并从这个配置文件开始读取信息。

```ini
[configuration]

# 设置好友的微信名称，记住，不是微信ID也不是微信备注
;my_friend_name = Alex

# 设置微信群名称
my_qun_name = 美团红包群

# 定时发送群公告
# 若某一项时间不想设置，请输入99:00，不能留空（注意：时分必须都是两位数）
;qun_notice_time = 08:00
qun_notice_time = 16:23

# 群公告信息
qun_notice_info = 早
```

这里的内容还不够丰富,你也可以接入其他的网站,自己进行封装，比如情感类网站分析亲密度、占卜类网站增加趣味性。。。

接着，开启微信机器人，为了程序的健壮性，自动判断一下操作系统，根据不同操作系统执行不同指令
```python
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
```

死循环，24小时执行
```python
# 在规定的时间发送群公告
def start_care():
    # 待发送的内容，先置为空
    # message = ""

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
```

开始执行相关操作
```python
t = Thread(target=start_care, name='start_care')
t.start()
```


## 完整源代码
项目源代码在 [GitHub仓库](https://github.com/h521822/python-maiden)  
项目持续更新，欢迎您[star本项目](https://github.com/h521822/python-maiden)


