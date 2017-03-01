# coding=utf-8
from django.conf.urls import url

from organization.views import OrgView,AddUserAskView, OrgHomeView

__author__ = 'lihao'
__date__ = '2017/2/25 15:09'

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home' )
]
