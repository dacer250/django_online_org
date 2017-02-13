# coding=utf-8
import xadmin
from organization.models import Teacher, CourseOrg, CityDict

__author__ = 'lihao'
__date__ = '2017/2/12 23:52'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'fav_nums', 'image', 'address', 'city']
    search_fields = ['name', 'desc', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'fav_nums', 'image', 'address', 'city']


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums',
                    'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums',
                   'add_time']

xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
