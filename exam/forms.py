from django import forms
from django.core.exceptions import ValidationError

from exam.models import User


class UserInfoForm(forms.Form):
    username = forms.CharField(label='用户名',
                               error_messages={
                                   'required': '用户名不能为空'
                               })
    password = forms.CharField(label='密码',
                               max_length=15,
                               min_length=1,
                               error_messages={
                                   'max-length': '密码最长15位',
                                   'required': '密码不能为空',
                                   'min-length': '密码最短1位'
                               })

    def clean_username(self):
        """局部钩子"""
        val = self.cleaned_data.get('username')
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字!")

    def clean(self):
        return self.cleaned_data


class RegisterForm(UserInfoForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已被注册')
        else:
            return username
