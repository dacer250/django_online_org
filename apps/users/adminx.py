# coding=utf-8
import xadmin
from users.models import EmailVerifyRecord, UserProfile, Banner
from xadmin import views
__author__ = 'lihao'
__date__ = '2017/2/12 21:29'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = '后台管理系统'
    site_footer = '你的公司'
    menu_style = 'accordion'

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index', ]
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class UserProfileAdmin(object):
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    search_fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']


xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)