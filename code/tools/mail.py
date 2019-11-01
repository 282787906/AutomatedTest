#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from tools import log


def send(title, msg):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "282787906@qq.com"  # 用户名
    mail_pass = "qtgyzyduulvkcaah"  # 口令

    sender = '282787906@qq.com'
    receivers = ['121002248@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(msg)
    message['From'] = Header("liqg", 'utf-8')
    # message['To'] = Header("测试", 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return  0
    except smtplib.SMTPException  as e:
        log.e('邮件发送异常', e)
        return 1


if __name__ == "__main__":
    send('test',"123123234234\nyyyyy")