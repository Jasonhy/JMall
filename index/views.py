from django.shortcuts import render,HttpResponse

from index.models import *

def index(request):
    # 拿到产品分类信息
    sort_msg = GoodSort.objects.all()
    msg = []

    for sort in sort_msg:
        msg.append({
            'sort':sort,
            'good_msg_list':sort.goods_set.all().order_by('goods_name')[0:4],
            'good_other_list':sort.goods_set.all().order_by('goods_name')[4:7]
        })

    dic = dict(**{
        'message':msg,
    })

    return render(request,"index/index.html",dic)