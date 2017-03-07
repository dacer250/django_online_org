# coding=utf-8
__author__ = 'lihao'
__date__ = '2017/3/1 23:33'

from django.conf.urls import url

from courses.views import CourseListView, CourseDetailView, CourseInfoView, \
    CommentView, AddCommentView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^play/(?P<course_id>\d+)/$', CommentView.as_view(),name='course_play'),

]
