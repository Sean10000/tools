from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from util import get_yaml_config
import os

__author__ = 'Ma,Shi-Cheng'


class SendMail(object):

    def __init__(self, mail_config_section):
        # yaml config file
        # mail:
        #  host_server: smtp.exmail.qq.com
        #  port: 587
        #  sender:
        #  password:
        #  sender_mail:
        #  receiver:
        #  mail_content:
        #  mail_title:
        self.mail_conf = get_yaml_config(mail_config_section)

    def send_mail(self, attach_file=None):
        validate_attach = True if attach_file else False
        host_server = self.mail_conf.get("host_server")
        sender_nick = self.mail_conf.get("sender_nick")
        password = self.mail_conf.get("password")
        sender_mail = self.mail_conf.get("sender_mail")
        receiver = self.mail_conf.get("receiver").split(',')
        mail_content = self.mail_conf.get("mail_content")
        mail_title = self.mail_conf.get("mail_title")
        # port = conf.get(cfg_section, "port")

        msg = MIMEMultipart() if validate_attach else MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = formataddr([sender_nick, sender_mail])
        msg["To"] = ';'.join(receiver)

        if validate_attach:
            msg.attach(MIMEText(mail_content, 'html', 'utf-8'))
            att = MIMEText(open(attach_file, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename={}'.format(os.path.basename(attach_file))
            msg.attach(att)

        smtp = SMTP_SSL(host_server)
        # smtp.set_debuglevel(1) #de-comment this line to debug
        smtp.ehlo(host_server)
        smtp.login(sender_mail, password)
        smtp.sendmail(sender_mail, receiver, msg.as_string())
        smtp.quit()


# if __name__ == '__main__':
#     s = SendMail("mail")
#     s.send_mail(attach_file="rate_20191008173105.xls")
