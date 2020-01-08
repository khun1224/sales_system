
from django.shortcuts import render, redirect

from account.forms import UserRegisterForm


def user_register(request):
    """ 注册 """
    if request.method == 'POST':
        form = UserRegisterForm(request=request, data=request.POST)
        if form.is_valid():
            form.register()
            return redirect('account:success')

    else:
        form = UserRegisterForm(request=request)
    return render(request, 'user_register.html', {
        'form': form,
    })


def success(request):
    """ 注册成功跳转 """
    return render(request, 'success.html')



