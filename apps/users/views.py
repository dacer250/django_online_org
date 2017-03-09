# coding=utf-8
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from operation.models import UserCourse, UserFavorite
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPasswordForm, \
    UploadImageForm, UserInfoUpdateForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return e


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '用户已存在！', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, 'register')
            return render(request, "login.html",{{'msg':'请先登录您的邮箱，激活账号'}})
        else:
            return render(request, "register.html", {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_forms = LoginForm(request.POST)
        if login_forms.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_forms})


            # Create your views here.


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return (request, 'login.html', dict(msg='您已激活，请登录！'))
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', dict(forget_form=forget_form))

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html',
                          dict(forget_form=forget_form))


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', dict(email=email))
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyView(View):
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html',
                              dict(email=email, msg='密码不一致，请重新输入！'), )
            which_user = UserProfile.objects.get(email=email)
            which_user.password = make_password(pwd2)
            which_user.save()

            return render(request, 'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html",
                          dict(email=email, modify_form=modify_form))


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoUpdateForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            name_dict = dict(status='success')
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES,
                                     instance=request.user)
        if image_form.is_valid():
            request.user.save()
            name_dict = dict(status='success')
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            name_dict = {'status': 'fail'}
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )


class UpdatePwdViw(View):
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd1 != pwd2:
                name_dict = dict(status='fail',
                                 msg='密码不一致，请重新输入！', )
                return HttpResponse(
                    json.dumps(name_dict),
                    content_type='application/json'
                )
            which_user = UserProfile.objects.get(user=request.user)
            which_user.password = make_password(pwd2)
            which_user.save()
            name_dict = dict(status='success', msg='修改成功')
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )
        else:
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type='application/json'
                                )


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            name_dict = dict(email='邮箱已存在')
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )

        send_register_email(email=email, send_type='update_email')
        name_dict = dict(status='success')
        return HttpResponse(json.dumps(name_dict),
                            content_type='application/json'
                            )


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email,
                                                           code=code,
                                                           send_type='update_email'
                                                           )
        if existed_records:
            user = request.user
            user.email = email
            user.save()
        else:
            name_dict = dict(email='验证码出错')
            return HttpResponse(json.dumps(name_dict),
                                content_type='application/json'
                                )


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html',
                      dict(user_courses=user_courses))


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html',
                      dict(org_list=org_list))

class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html',
                      dict(teacher_list=teacher_list))
