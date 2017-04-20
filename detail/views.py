from django.shortcuts import render
from index.models import *
from usercenter import der

@der.login_name
def detail(request,dic):
    # 商品详情
    goods_id = request.GET.get("goods_id")
    if goods_id:
        # 根据id查询商品
        good = Goods.objects.get(pk=goods_id)
        new_goods_list = good.goods_sort.goods_set.all().order_by("-pub_date")[0:2]
        goods_comment = good.goodscomment_set.all().order_by("-comment_date")[0:2]

    if dic['user']:
        flag = False
        rece = dic['user'].recentsee_set().order_by("-id")[0:5]
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