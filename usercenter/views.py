from django.shortcuts import render,redirect
from usercenter import der
from index.models import *
from django.core.urlresolvers import reverse
from django.http import *
from django.core.paginator import Paginator

@der.login_yz
@der.login_name
def user_center_info(request,dic):
    if request.method == "GET":
        recentsee = dic['user'].user_recent_see.all()
        goods_list = []
        for i in recentsee:
            # goods_list.append(Goods.objects.get(id=int(i.goods_name)))
            goods_list.append(Goods.objects.get(id=i.id))
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

@der.login_yz
@der.login_name
def user_center_site(request,dic):
    if request.method == 'GET':
        user = dic['user']
        addr_info = user.user_addr_info.all().filter(is_delete=False)
        list2 = []
        for i in addr_info:
            a = i.phone[0:]
            list2.append({
                "id":i.id,
                "province":i.province,
                "city":i.city,
                "dis":i.dis,
                "address":i.address,
                "phone":i.phone,
                "default_addr":i.default_addr
            })
        dic = dict(dic,**{"addr_info":list2})
        delete = request.GET.get("delete")
        change = request.GET.get("change")

        if delete:
            addr = AddrInfo.objects.get(id=delete)
            addr.is_delete = True
            addr.save()
            return redirect(reverse("usercenter:user_center_site"))
        if change:
            addr = AddrInfo.objects.get(id=change)
            try:
                default = AddrInfo.objects.filter(user=user.id).get(default_addr=True)
            except Exception as e:
                pass
            else:
                default.default_addr = False
                default.save()
                return redirect(reverse("usercenter:user_center_site"))

        return render(request,'usercenter/user_center_site.html',dic)
    else:
        addressee = request.POST.get('addressee')
        province = request.POST.get('province')
        city = request.POST.get('city')
        dis = request.POST.get('dis')
        detaaddr = request.POST('detaaddr')
        postcode = request.POST('postcode')
        phonenumber = request.POST('phonenumber')

        if addressee and province and city and detaaddr and str(phonenumber).isdigit() and len(phonenumber) == 11:
            addr_info = AddrInfo()
            addr_info.province = AreaInfo.objects.get(parent_id__exact=province)
            addr_info.city = AreaInfo.objects.get(parent_id__exact=city)
            if dis:
                addr_info.dis = AreaInfo.objects.get(parent_id__exact=dis)
            addr_info.address = addressee
            addr_info.default_addr =detaaddr
            addr_info.post_code = postcode
            addr_info.phone = phonenumber
            addr_info.user = dic['user']
            addr_info.save()
            print("成功存入")
            return redirect(reverse("usercenter:user_center_site"))
        else:
            return redirect(reverse("usercenter:user_center_site"))

def areal(request):
    list1 = AreaInfo.objects.filter(parent__isnull=True)
    list2 = []
    for a in list1:
        list2.append({
            "id":a.id,
            "title":a.title
        })
    return JsonResponse({'data':list2})

@der.login_yz
@der.login_name
def user_center_order(request,dic):
    order_list = Orders.objects.filter(is_delete=False).filter(user_order_id=dic['user'].id).order_by('-id').order_by('is_finish')
    p_index = request.GET.get("page",None)
    order_list2,p_list,p_index = pag_tab(order_list,p_index,2)
    if len(p_list) >= 3:
        '''页码显示页数'''
        if len(p_list) == p_index:
            p_list = p_list[p_index-3:p_index]
        elif p_index == 1:
            p_list = p_list[0:p_index+2]
        else:
            p_list = p_list[p_index:p_index+1]

    orders = []
    for order in order_list2:
        detail_list = []
        addr = AddrInfo.objects.get(id=order.addr)
        for i in order.order_detail.all():
            detail_list.append({
                "od":i,
                "good":i.goods,
            })
        orders.append({
            "order":order,
            "order_detail":detail_list,
            "addr":addr
        })
    dic = dict(dic,**{
        "order_list":orders,
        'p_list':p_list,
        "p_index":p_index
    })
    return render(request,'usercenter/user_center_order.html',dic)

def pag_tab(list1,p_index,num):
    '''
    分页
    :param list1:
    :param p_index:
    :param num:
    :return:
    '''
    p = Paginator(list1,num)
    if p_index == '' or p_index == None:
        p_index = '1'
    p_index = int(p_index)
    list2 = p.page(p_index)
    p_list = p.page_range
    return list2,p_list,p_index

@der.login_yz
@der.login_name
def pay(request,dic):
    order_id = request.GET.get('order',None)
    order = Orders.objects.get(id=int(order_id))
    order.is_finish = True
    order.save()
    return redirect(reverse("usercenter:user_center_order"))