# coding=utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

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
        # 课程机构分页
        org_num = all_org.count()
        # 学生人数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-students")
            elif sort == 'course_nums':
                all_org = all_org.order_by("-course_nums")
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
            return HttpResponse(json.dumps(name_dict), content_type='application/json')
        else:
            name_dict = {'status':'fail','msg':'添加出错'}
            return HttpResponse(json.dumps(name_dict), content_type='application/json')
