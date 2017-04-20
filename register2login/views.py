from django.shortcuts import render,redirect
from index.models import *
import hashlib
from datetime import datetime

def register(request):
    if request.method == "GET":
        return render(request,"register2login/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        if username and len(password) > 8 and email:
            try:
                if UserInfo.objects.get(username=username):
                    pass
            except Exception as e:
                user = UserInfo()
                user.username = username
                n = hashlib.md5()
                n.update(password)
                user.password = n.hexdigest()
                user.email = email
                user.reg_date = datetime.now()
                user.save()
                print('注册成功')
                return redirect('/login/')
            else:
                print("同户名已存在")
                return render(request, "register2login/register.html")
            finally:
                pass

def login(request):

    return render(request,"register2login/login.html")