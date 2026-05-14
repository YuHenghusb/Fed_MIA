import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tkinter import messagebox
def get(email):#邮箱验证码发送
    ini = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    v_code = ''
    for j in range(0, 6):
        v_code += ini[random.randint(0, 61)]
    sender = '3508579721@qq.com'
    recivers = email

    message = MIMEText('这是来自电子书阅读平台E-Book发来的验证码，如果你没有请求该类信息，请忽略这封邮件。\n验证码为：%s' %(v_code), 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = Header(recivers, 'utf-8')
    message['Subject'] = Header('电子书阅读平台验证码')


    try:
        mail = smtplib.SMTP('smtp.qq.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, 'jerdtptaggnadaeb')
        mail.sendmail(sender, recivers, message.as_string())
        messagebox.showinfo('成功', '邮件发送成功')
    except smtplib.SMTPException as e:
        messagebox.showinfo('错误', '邮件发送成功')

    return v_code