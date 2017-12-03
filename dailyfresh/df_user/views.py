# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
from models import *


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    upwd2 = post['cpwd']
    uemail = post['email']
    # 判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    user = User_Info()
    user.uname = uname
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = User_Info.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'用户登陆', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息，可以使用get方法，也可以使用词典获取方式
    post = request.POST
    uname =post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    users = User_Info.objects.filter(uname=uname)
    # []如果用get的话如果查不到会出现异常，filter则是[]，不会出现异常
    print(uname)
    # 判断：如果未查到则用户名错误，如果查到了则判断密码是否正确，正确的话转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登陆', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登陆', 'error_name':1, 'error_pwd':0, 'uname':uname, 'upwd':upwd}
        return render(request, 'df_user/login.html', context)


def info(request):
    user_email = User_Info.objects.get(id = request.session['user_id']).uemail
    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name']
    }
    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    return render(request, 'df_user/user_center_order.html')


def site(request):
    user = User_Info.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {
        'title': '用户中心',
        'user': user
    }
    return render(request, 'df_user/user_center_site.html', context)