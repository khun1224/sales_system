from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    """ 用户注册 """

    username = forms.CharField(label='用户名', min_length=3, max_length=10,
                               error_messages={
                                   'min_length': '用户名不能小于3位',
                                   'max_length': '用户名不能超过10位',
                                   'required': '用户名不能为空',
                               })
    password = forms.CharField(label='密码', min_length=6,  max_length=32, widget=forms.PasswordInput,
                               error_messages={
                                   'min_length': '密码不能小于6位',
                                   'max_length': '用户名不能超过32位',
                                   'required': '密码不能为空',
                               })
    password_repeat = forms.CharField(label='重复密码', min_length=6,  max_length=64, widget=forms.PasswordInput,
                                      error_messages={
                                          'min_length': '密码不能小于6位',
                                          'max_length': '用户名不能超过32位',
                                          'required': '密码不能为空',
                                      })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        """ 验证用户名是否已经被注册 """
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('用户名已存在')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password_repeat = cleaned_data.get('password_repeat', None)
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError('两次密码输入不一致')
        return cleaned_data

    def register(self):
        """ 注册方法 """
        data = self.cleaned_data
        # 1. 创建用户
        User.objects.create_user(username=data['username'],
                                 password=data['password'],)
        # 2. 自动登录
        user = authenticate(username=data['username'],
                            password=data['password'])
        login(self.request, user)
        return user



