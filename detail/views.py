from django.shortcuts import render
from index.models import *
def detail(request):
    # 商品详情
    goods_id = request.GET.get("goods_id")
    if goods_id:
        # 根据id查询商品
        good = Goods.objects.get(pk=goods_id)
        new_goods_list = good.goods_sort.goods_set.all().order_by("-pub_date")[0:2]
        goods_comment = good.goodscomment_set.all().order_by("-comment_date")[0:2]

    sort_msg = GoodSort.objects.all()
    dic = {
        'sort_msg':sort_msg,
        'good_sort':good.goods_sort,
        'good':good,
        'new_goods_list':new_goods_list,
        'goods_comment':goods_comment
    }

    dic = dict(**dic)
    return render(request,'detail/detail.html',dic)