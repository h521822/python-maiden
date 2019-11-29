#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

# 第三方 SMTP 服务
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "he521822@126.com"  # 用户名
mail_pass = "hj123456"  # 口令（是授权码，不是登录密码）

sender = 'he521822@126.com'     # 发送人邮箱，必须与 mail_user 一致
receivers = ['h521822@126.com','1665521822@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
subject = '我是江小白不喝酒'    # 标题
msg_from = 'Tim<h22@126.com>'   # 发件人(Tim为发送人名称，可以为空；<>为发送人邮箱，可以为空，可任意伪装)
msg_to = 'h521822@126.com,1665521822@qq.com'   # 收件人，必须与 receivers 一致
msg_text = '现在是' + now + '，明天记得下午五点开会！'     # 发送内容

message = MIMEText(msg_text, 'plain', 'utf-8')  # 邮箱内容
message['From'] = msg_from
message['To'] = msg_to

message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())    # 发送人，收件人，内容
    print("邮件发送成功")

except smtplib.SMTPException:
    print("Error: 无法发送邮件")
