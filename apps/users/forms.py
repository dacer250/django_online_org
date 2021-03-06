# coding=utf-8
from users.models import UserProfile

__author__ = 'lihao'
__date__ = '2017/2/20 12:40'

from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ModifyPasswordForm(forms.Form):
    password1= forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['image']




class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['nick_name','gender','birthday','address','mobile']
