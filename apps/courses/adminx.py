# coding=utf-8
import xadmin

__author__ = 'lihao'
__date__ = '2017/2/12 22:24'

from .models import Course, Lesson, Video


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', ]
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name',]
    list_filter =['course','name','add_time']


xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Course, CourseAdmin)


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name',]
    list_filter = ['lesson','name','add_time']


xadmin.site.register(Video, VideoAdmin)