from django.shortcuts import render,redirect
from django.http import *
from django.core.urlresolvers import reverse
from usercenter import der
from index.models import *
from datetime import datetime
import time
@der.login_yz
@der.login_name
def cart(request,dic):
    cart_list = dic['user'].cart_set.all().filter(is_delete=False)
    cart_good_list = []
    for cart in  cart_list:
        cart_good_list.append({
            "cart":cart,
            'good':Goods.objects.get(id=int(cart.goods_name))
        })
    dic = dict(dic,**{
        "lis":cart_good_list
    })

    return render(request,'cart/cart.html',dic)

@der.login_yz
def deleteHander(request):
    cart_id = request.POST.get('cart_id',None)
    if cart_id:
        cart = Cart.objects.get(id=int(cart_id))
        cart.is_delete = True
        cart.save()
        return JsonResponse({"response":'1'})

@der.login_yz
@der.login_name
def place_order(request,dic):
    '''
    结算
    :param request:
    :return:
    '''
    cart_id = []
    if request.method == 'GET':
        count = request.GET.get('count',None)
        good_id = int(request.GET.get('id',None))
        good_id = [good_id]
    else:
        count = request.POST.getlist('count',None)
        cart_id = request.POST.getlist('id',None)
        good_id=[]
        j = 0
        for i in cart_id:
            cart = Cart.objects.get(id=int(i))
            good_id.append(cart.goods_name)
            if int(count[j]) != cart.buy_count:
                cart.buy_count = int(count[j])
                cart.save()
            j += 1

    order_list = []
    freight = 10
    sumprice = 0
    for i in range(len(good_id)):
        goods = Goods.objects.get(id=int(good_id[i]))
        orderdic = {
            "goods":goods,
            "count":i+1,
            "sumtotal":goods.goods_price*int(count[i]),
            "goods_count":count[i]
        }
        if len(cart_id) > 0:
            orderdic["cart_id"] = cart_id[i]
        order_list.append(orderdic)
        sumprice += goods.goods_price*int(count[i])
    addr_list = dic['user'].user_addr_info.all()
    dic = dict(dic,**{
        'addr_list':addr_list,
        'order_list':order_list,
        'all_price':sumprice + freight,
        'goods_amount':len(good_id),
        'all_total':sumprice,
        'cart_id':cart_id,
        'freight':freight,
    })
    return render(request,'cart/place_order.html',dic)

@der.login_yz
@der.login_name
def place_hander(request,dic):
    '''
    提交订单后,处理页面跳转到用户订单页
    :param request:
    :param dic:
    :return:
    '''
    addr = request.POST.get('addr')
    goods_count = request.POST.get('goods_count')
    goods_id = request.POST.get('goods_id')  # 如果是立即购买的获取物品id
    cart_id = request.POST.get('cart_id')   # 如果是购物车结算的获取购物车id

    orders = Orders()
    orders.order_time = datetime.now()
    orders.order_number = str(int(time.time()))
    orders.user_order_id = dic['user'].id
    orders.addr = int(addr)
    orders.save()
    if cart_id and cart_id[0]:
        for i in cart_id:
            cart = Cart.objects.get(id=int(i))
            goods = Goods.objects.get(id=int(cart.goods_name))
            order_detail = orders.order_detail.create(goods_name=goods.goods_name,
                                                      goods_price=goods.goods_price,
                                                      buy_count=int(goods_count),
                                                      goods_id=goods_id)
            order_detail.save()
            cart.is_delete=True
            cart.save()
    else:
        goods = Goods.objects.get(id=int(goods_id))
        orders.order_detail.create(goods_name=goods.goods_name,
                                   goods_price=goods.goods_price,
                                   buy_count=goods_count,
                                   goods_id=goods_id)
    return redirect(reverse('usercenter:user_center_order'))

