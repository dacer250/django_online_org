# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from  organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',blank=True,null=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(("cj", '初级'), ('zj', '中级'), ('gz', '高级')), max_length=2)
    teachers = models.ForeignKey(Teacher, verbose_name=u'教师',null=True, blank=True,)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name=u'封面')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    tag = models.CharField(default='', verbose_name='标签', max_length=10)
    category = models.CharField(max_length=20, verbose_name='课程类别', default='')
    need_know = models.CharField(max_length=300,verbose_name=u'须知',default='')
    teacher_tell = models.CharField(max_length=300,verbose_name=u'须知公告',default='')


    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_chapter_nums(self):
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __unicode__(self):
        return '{}'.format(self.name)

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    learn_times = models.IntegerField(default=0, verbose_name=u'时长', )
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'下载文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
