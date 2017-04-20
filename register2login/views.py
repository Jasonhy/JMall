from django.shortcuts import render,redirect,HttpResponse
from index.models import *
import hashlib
from datetime import datetime
from usercenter import der

def register(request):
    if request.method == "GET":
        return render(request,"register2login/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        if username and len(password) >= 6 and email:
            try:
                if UserInfo.objects.get(username=username):
                    return render(request, "register2login/register.html")
            except Exception as e:
                user = UserInfo()
                user.username = username
                n = hashlib.md5(password.encode('utf-8'))
                user.password = n.hexdigest()
                user.email = email
                user.reg_date = datetime.now()
                user.save()
                print('注册成功')
                return redirect('/login/')
            else:
                print("用户名已存在")
                return render(request, "register2login/register.html")
        else:
            return render(request, "register2login/register.html")

@der.login_name
def login(request,dic):
    if request.method == "GET":
        return render(request,"register2login/login.html",dic)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        vcode = request.POST.get("vcode")
        # 先验证验证码防止暴力破解
        if vcode.upper() != request.session['verifycode']:
            return render(request, "register2login/login.html")
        if username and password:
            try:
                user = UserInfo.objects.get(username=username)
                # 如果用户名和密码都正确,登录成功
                n = hashlib.md5(password.encode('utf-8'))
                if user.password == n.hexdigest():
                    if request.POST.get('check') == 'on':
                        request.session['username'] = username
                    else:
                        request.session['username'] = username
                        # 超时测试
                        request.session.set_expiry(0)
                    return redirect('/index/')
                else:
                    return render(request, "register2login/login.html",{'error':{'password':'密码输入有误，请重新输入'}})
            except Exception as e:
                return render(request, "register2login/login.html")
        else:
            return render(request, "register2login/login.html",{'error':{'name':'请输入用户名','password':'请输入密码'}})

def changekw(request):
    pass

