# coding=utf-8
from users.views import UserInfoView, UploadImageView, UpdatePwdViw, \
    SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView

__author__ = 'lihao'
__date__ = '2017/3/7 15:43'

from django.conf.urls import url

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='up_load_image'),
    url(r'^update/pwd/$', UpdatePwdViw.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='update_email'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

]