# coding=utf-8
__author__ = 'lihao'
__date__ = '2017/3/1 23:33'

from django.conf.urls import url

from courses.views import CourseListView, CourseDetailView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
]
