from django.shortcuts import render,redirect
from usercenter import der
from index.models import *
from django.core.urlresolvers import reverse

@der.login_yz
@der.login_name
def user_center_info(request,dic):
    if request.method == "GET":
        print("用户信息",dic)

        recentsee = dic['user'].recentsee_set().all()
        goods_list = []
        for i in recentsee:
            goods_list.append(Goods.objects.get(id=int(i.goods_name)))
        recv = goods_list[-5:]
        recv.reverse()
        dic = dict(dic,**{"recentsee":recv})
        return render(request,'usercenter/user_center_info.html',dic)
    else:
        addr = request.POST.get('addr')
        phone = request.POST.get('phone')
        if addr and str(phone).isdigit() and len(phone) == 11:
            dic['user'].phone = phone
            dic['user'].addr = addr
            dic['user'].save()
        return redirect(reverse('usercenter:user_center_info'))

