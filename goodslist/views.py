from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator
from usercenter import der
from index.models import *

@der.login_name
def list(request,dic):
    sort_id = request.GET.get('sort',None)
    if sort_id == '' or sort_id == None:
        sort_id = 1
    sort_id = int(sort_id)
    good_sort = GoodSort.objects.get(id=sort_id)
    good_list = good_sort.goods_set.all()

    # 新品推荐排序 取出两个
    new_goods_list = good_list.order_by('-pub_date')[0:2]

    order = request.GET.get("order",None)
    if order == '' or order == None:
        order = 'id'
    if order == 'price':
        order_list = good_list.order_by('goods_price')
        active = {'price':'active'}
    elif order == 'id':
        order_list = good_list.order_by('id')
        active = {'id'"'active"}
    elif order == 'count':
        order_list = good_list.order_by('-sale_count')
        active = {'count':'active'}
    else:
        return HttpResponse('404')

    p_index = request.GET.get('page',None)
    order_list2,p_list,p_index = page_tab(order_list,p_index,5)
    if len(p_list) >= 3:
        if len(p_list) == p_index:
            p_list = p_list[p_index-3:p_index]
        elif p_index == 1:
            p_list = p_list[0:p_index+2]
        else:
            p_list = p_list[p_index-2:p_index+1]

    sort_msg = GoodSort.objects.all()
    data = {
        "good_list":{
            "new_goods_list":new_goods_list,
            "order_list":order_list2,
            "active":active,
            "p_list":p_list,
            "order_type":order,
            "p_index":p_index,
            "good_sort":good_sort
        },
        "sort_msg":sort_msg
    }

    dic = dict(dic,**data)
    return render(request,'goodslist/list.html',dic)


def page_tab(list1,p_index,num):
    '''
    分页函数
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