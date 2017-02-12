# coding=utf-8
import xadmin
from users.models import EmailVerifyRecord, UserProfile, Banner

__author__ = 'lihao'
__date__ = '2017/2/12 21:29'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    list_display= ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index',]
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(Banner, BannerAdmin)

class UserProfileAdmin(object):
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile','image']
    search_fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile','image']
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile','image']

xadmin.site.register(UserProfile, UserProfileAdmin)
