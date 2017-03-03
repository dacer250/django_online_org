# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course, CourseResource
from operation.models import UserFavorite


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
        return render(request, 'course-detail.html', {'course': course,
                                                      'relate_courses': relate_courses,
                                                      'has_fav_org': has_fav_org,
                                                      'has_fav_course': has_fav_course,
                                                      })


class

class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {"course": course,
                                                     "all_resources": all_resources,
                                                     })
