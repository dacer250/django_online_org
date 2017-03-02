# coding=utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from operation.models import UserFavorite
from organization.form import UserAskForm
from organization.models import CityDict, CourseOrg


class OrgView(View):
    def get(self, request):
        # 课程机构
        all_org = CourseOrg.objects.all()
        # 热门
        hot_org = all_org.order_by('-click_nums')[:3]
        # 城市
        all_city = CityDict.objects.all()
        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_org = all_org.filter(category=category)

        org_num = all_org.count()
        # 学生人数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-students")
            elif sort == 'course_nums':
                all_org = all_org.order_by("-course_nums")
        # 课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 3, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {'all_org': orgs,
                                                 'all_city': all_city,
                                                 'org_num': org_num,
                                                 'city_id': city_id,
                                                 'category': category,
                                                 'hot_org': hot_org,
                                                 'sort': sort,
                                                 })


class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            name_dict = {'status': 'success'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            name_dict = {'status': 'fail', 'msg': '添加出错'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )


class OrgHomeView(View):
    """
    org home page
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id,
                                           fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html',
                      {'all_course': all_courses,
                       'all_teacher': all_teacher,
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_fav': has_fav,
                       })


class OrgCourseView(View):
    """
    org course page
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=course_org.id,
                    fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html',
                      {'all_course': all_courses,
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_fav': has_fav,
                       })


class OrgDescView(View):
    """
    org home page
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id,
                                           fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    org home page
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id,
                                           fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated():
            # 判断用户状态
            name_dict = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )

        exist_records = UserFavorite.objects.filter(user=request.user,
                                                    fav_id=int(fav_id),
                                                    fav_type=int(fav_type)
                                                    )
        if exist_records:
            # if用户存在，则表示用户取消收藏
            exist_records.delete()
            name_dict = {'status': 'success', 'msg': '收藏'}
            return HttpResponse(
                                json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                name_dict = {'status': 'success', 'msg': '已收藏'}
                return HttpResponse(json.dumps(name_dict),
                                    content_type='application/json'
                                    )
            else:
                name_dict = {'status': 'fail', 'msg': '收藏出错'}
                return HttpResponse(json.dumps(name_dict),
                                    content_type='application/json'
                                    )
