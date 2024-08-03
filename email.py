import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import schedule
import os
import datetime

sender = '2xxx4@qq.com'  # 发信人的邮箱账号
passWord = 'xxxxx'  # 发件人邮箱授权码
receiver = 'qq@qq.com'  # 收件人邮箱账号

# 指定在一起的日期和时间
start_date = datetime.datetime(2023, 6, 11, 23, 0)  # 在一起的起始日期和时间

# 记录在一起时间的文件路径
days_file = 'days_count.txt'


def get_time_together():
    # 计算当前时间和在一起的起始时间的时间差
    current_time = datetime.datetime.now()
    time_together = current_time - start_date

    # 计算在一起的小时数、天数和分钟数
    hours_together = time_together.total_seconds() / 3600
    days_together = time_together.days
    minutes_together = int(time_together.total_seconds() / 60)

    return hours_together, days_together, minutes_together


def mail():
    # 获取在一起的时间
    hours, days, minutes = get_time_together()

    # 构造邮件内容
    hour = datetime.datetime.now().hour
    if hour == 8:
        message = f"新的一天!开开心心,顺顺利利！"
    elif hour == 12:
        message = f"按时吃饭，事情吃完再做也没事！"
    elif hour == 24:
        message = f"虽然我们在一起已经 {days} 天 {int(hours)} 小时 {minutes} 分钟了，但是现在很晚啦，宝贝该睡觉觉辣！熬夜会变丑的！早点睡觉不要熬夜,我要是没睡你也监督我！！！"
    else:
        message = f"我们在一起已经 {days} 天 {int(hours)} 小时 {minutes} 分钟啦！"

    print(message)
    ret = True
    try:
        # 定义邮件类
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["sender", sender])                 # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["receiver", receiver])               # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "叮咚~"                     # 标题

        # 设置发件人信息
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, passWord)  # 发件人邮箱账号、授权码

        # 发送邮件
        server.sendmail(sender, [receiver, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("Success!")
    except Exception as e:
        print("Error!", e)
        ret = False
    return ret


# 设置每天8点、12点和24点执行函数mail
schedule.every().day.at("08:00").do(mail)
schedule.every().day.at("12:00").do(mail)
schedule.every().day.at("00:00").do(mail)
#schedule.every(0).seconds.do(mail)
while True:
    schedule.run_pending()


