import smtplib
from email.mime.text import MIMEText
class EmailUtil:
    def __init__(self):
        pass
    def send(self,content,tos):
        mail_host = 'smtp.163.com'
        mail_user = '13048282493'
        mail_pass = 'qiutan123'
        sender = '13048282493@163.com'
        receivers = tos

        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = '分数提醒'
        message['From'] = sender
        if len(receivers) > 1:
            message['To'] = ','.join(receivers)  # 群发邮件
        else:
            message['To'] = receivers[0]

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print('success to %s' % message['To'])
        except smtplib.SMTPException as e:
            print('error', e)
if __name__ == '__main__':
    EmailUtil().send()