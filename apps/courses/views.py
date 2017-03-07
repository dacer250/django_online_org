# coding=utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:2]
        # 课程机构分页
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_course = all_course.order_by("-students")
            elif sort == 'course_nums':
                all_course = all_course.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 3, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {'all_course': courses,
                                                    'sort': sort,
                                                    'hot_courses': hot_courses,
                                                    })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id,
                                           fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.course_org.id,
                                           fav_type=2):
                has_fav_org = True

        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html',
                      {'course': course,
                       'relate_courses': relate_courses,
                       'has_fav_org': has_fav_org,
                       'has_fav_course': has_fav_course,
                       })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            usr_course = UserCourse(user=request.user, course=course)
            usr_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_id = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_id)
        course_ids = [user_courser.course.id for user_courser in
                      all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by(
            '-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {"course": course,
                                                     "all_resources": all_resources,
                                                     'relate_courses': relate_courses,
                                                     })


class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            name_dict = {'status': 'fail', 'msg': "未登录！"}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            name_dict = {'status': 'success', 'msg': '添加成功'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            name_dict = {'status': 'fail', 'msg': '添加失败'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            usr_course = UserCourse(user=request.user, course=course)
            usr_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_id = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_id)
        course_ids = [user_courser.course.id for user_courser in
                      all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by(
            '-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {"course": course,
                                                     "all_resources": all_resources,
                                                     'relate_courses': relate_courses,
                                                     'video': video,
                                                     })
