from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserForm


# Create your views here.
def custom_login(request):
    if request.method == 'POST':
        # 获取数据
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        # 验证用户是否合法
        user = authenticate(username=username, password=password)
        if user:
            # 登录
            if user.is_active:
                login(request, user)
                # 返回页面
                return redirect(reverse('bbs:index'))
            else:
                return render(request, 'accounts/login.html', {'error_message': '用户没有被激活，联系DE8UG'})
        else:
            return render(request, 'accounts/login.html', {'error_message': '用户名或密码错误！'})

    return render(request, 'accounts/login.html')


def register(request):
    form = UserForm(request.POST or None)
    print(form['region'].value())
    if form.is_valid():
        # 如果数据合法，保存到user
        user = form.save(commit=False)     
        user.set_password(form.cleaned_data['password'])
        user.save()

        # 同步保存到profile
        profile = UserProfile()
        profile.user = user
        profile.region = form['region'].value()
        profile.save()

        login(request, user)
        return redirect('bbs:index')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def custom_logout(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def update_userprofile(request):
    try: 
        if request.method == 'POST':
            # 获取数据
            data = request.POST
            f = request.FILES
            print(data, f)
            # 找到用户
            user = User.objects.get(username=data['username'])
            # 更新数据
            profile = UserProfile.objects.get(user=user)
            if profile:
                user.email = data['email']
                profile.sex = data['gridRadios']
                profile.phone_number = data['phoneNumber']
                profile.region = data['region']
                # if f:
                profile.picture = f['picture']       
                # 保存
                profile.save()
                user.save()
    except Exception as e:
        print(e)
    return redirect('bbs:my-page')


