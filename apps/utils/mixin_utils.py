# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'lihao'
__date__ = '2017/3/4 14:31'


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)
