from django.shortcuts import render,redirect,HttpResponse
from index.models import *
from usercenter import der
from datetime import datetime
from django.http import *

@der.login_name
def detail(request,dic):
    # 商品详情
    goods_id = request.GET.get("goods_id")
    if goods_id:
        # 根据id查询商品
        good = Goods.objects.get(pk=goods_id)
        new_goods_list = good.goods_sort.goods_set.all().order_by("-pub_date")[0:2]
        goods_comment = good.goods_comments.all().order_by("-comment_date")[0:2]

    if dic['user']:
        flag = False
        rece = dic['user'].user_recent_see.order_by("-id")[0:5]
        for i in rece:
            if i.goods_name == goods_id:
                flag = True
            if not flag:
                rec = RecentSee()
                rec.goods_name = goods_id
                rec.user_id = dic['user'].id
                rec.save()

    sort_msg = GoodSort.objects.all()
    dic2 = {
        'sort_msg':sort_msg,
        'good_sort':good.goods_sort,
        'good':good,
        'new_goods_list':new_goods_list,
        'goods_comment':goods_comment
    }

    dic = dict(dic,**dic2)
    return render(request,'detail/detail.html',dic)

@der.login_yz
def comment(request,gid):
    '''
    商品评论
    :param request:
    :param gid:
    :return:
    '''
    comments = request.POST.get("comment",None)
    if comments and gid:
        good_comment = GoodsComment()
        good_comment.username = request.session['username']
        good_comment.comment_date = datetime.now()
        good_comment.comment = comments
        good_comment.goods_id = int(gid)
        good_comment.save()
        return redirect('/detail/?goods_id='+gid)

@der.login_yz
def addcart(request):
    goods_id = request.POST.get("goods_name",None)
    buy_count = request.POST.get("buy_count",None)
    if goods_id and buy_count:
        username = request.session['username']
        user = UserInfo.objects.get(username=username)
        cart = Cart()
        cart.goods_name = goods_id
        cart.buy_count = int(buy_count)
        cart.user_cart_id = user.pk
        cart.save()
        number = user.cart_set.filter(is_delete=False).count()
        return JsonResponse({"number":number})


