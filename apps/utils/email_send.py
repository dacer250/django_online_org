# coding=utf-8
__author__ = 'lihao'
__date__ = '2017/2/20 21:06'
from random import Random

from django.core.mail import send_mail

from mxonline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def random_str(random_length=8):
    str_code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str_code += chars[random.randint(0, length)]
    return str_code


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(random_length=16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '慕学在线注册激活链接'
        email_body = '请点解链接：http://127.0.0.1:8000/active/{}/'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
