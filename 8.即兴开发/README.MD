

<!-- TOC -->

- [1. 通过图灵机器人为微信群增加乐趣](#1-通过图灵机器人为微信群增加乐趣)
  - [1.1. 简介](#11-简介)
  - [1.2. 编写思路](#12-编写思路)
    - [1.2.1. 定时问候](#121-定时问候)
    - [1.2.2. 接收微信群信息，并调用图灵机器人进行自动回复](#122-接收微信群信息并调用图灵机器人进行自动回复)
  - [1.3. 完整源代码](#13-完整源代码)

<!-- /TOC -->



# 1. 通过图灵机器人为微信群增加乐趣

---
## 1.1. 简介

有些群人太少，为了增加一定的活跃度，想到了给微信群加个机器人。  
人多的大群，也可以利用机器人管理，如：自动邀请进群、违规自动踢人...

这里写的是每条早上定时的问候语，以及图灵机器人的互动。以达到活跃的效果。/手动滑稽

## 1.2. 编写思路
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

# 定时发送群消息的时间
# 若某一项时间不想设置，请输入99:00，不能留空（注意：时分必须都是两位数）
;qun_notice_time = 08:00
qun_notice_time = 18:25

# 图灵api_key
# 图灵机器人官网注册获取apikey。地址：http: // www.tuling123.com /
tuling_api_key = 5279ee06a58b4db8880fa6c44949b33c


# 一言的接口
# c	可选	Cat，即类型。提交不同的参数代表不同的类别，具体：

# a	Anime - 动画
# b	Comic – 漫画
# c	Game – 游戏
# d	Novel – 小说
# e	Myself – 原创
# f	Internet – 来自网络
# g	Other – 其他
yiyan_url = https://v1.hitokoto.cn/?c=b



```

我这里直接入了一言和图灵机器人，内容还不够丰富,你也可以接入其他的网站,自己进行封装

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

### 1.2.1. 定时问候
每天早上定时调用一言的接口问候群里的朋友，开启每天的第一的话题
```python
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
```

### 1.2.2. 接收微信群信息，并调用图灵机器人进行自动回复
回复指定的微信群
```python
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

## 1.3. 完整源代码
项目源代码在 [GitHub仓库](https://github.com/h521822/python-maiden)  
项目持续更新，欢迎您[star本项目](https://github.com/h521822/python-maiden)


