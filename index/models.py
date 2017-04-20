from django.db import models
from tinymce.models import HTMLField
import django.utils.timezone as timezone


# 用户表
class UserInfo(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    addr = models.CharField(max_length=50,null=True,blank=True)
    reg_date = models.DateTimeField()
    is_delete = models.BooleanField(default=False)

    # 额外信息 预留
    extra = models.CharField(max_length=20,null=True,blank=True)

    class Meta:
        db_table = 'userinfo'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

# 省市区表
class AreaInfo(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey('self',null=True,blank=True)

    class Meta:
        db_table = 'areainfo'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.title

# 地址信息表
class AddrInfo(models.Model):
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    dis = models.CharField(max_length=15)
    # 收信人
    address = models.CharField(max_length=20)
    detail_addr = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10,null=True,blank=True)
    phone = models.CharField(max_length=15)
    is_delete = models.BooleanField(default=False)
    # 默认地址
    default_addr = models.BooleanField(default=False)
    # 预留
    extra = models.CharField(max_length=20,null=True,blank=True)

    # 一个人可以填写多个地址 人与地址之间是一对多的关系
    user = models.ForeignKey('UserInfo')

    class Meta:
        db_table = 'addrinfo'
        verbose_name_plural = '地址信息'

    def __str__(self):
        return self.phone

# 商品种类表
class GoodSort(models.Model):
    sort_name = models.CharField(max_length=10)
    sort_pic = models.ImageField(upload_to='static/uploads/')
    # 预留
    sort_class = models.CharField(max_length=20)

    class Meta:
        db_table = 'goodsort'
        verbose_name_plural = '商品种类'

    def __str__(self):
        return self.sort_name

# 商品表
class Goods(models.Model):
    goods_name = models.CharField(max_length=30)
    goods_desc = models.CharField(max_length=80)
    goods_price = models.DecimalField(max_digits=7,decimal_places=2)
    goods_detail = HTMLField()
    img_path = models.ImageField(upload_to='static/uploads/')
    sale_count = models.IntegerField(default=0)

    # 一个分类有多个商品
    goods_sort = models.ForeignKey('GoodSort')
    pub_date = models.DateTimeField(default=timezone.now)
    extra = models.CharField(max_length=20,null=True,blank=True) #预留

    class Meta:
        db_table = 'goods'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.goods_name

# 商品评论
class GoodsComment(models.Model):
    username = models.CharField(max_length=30)
    comment_date = models.DateTimeField()
    comment = HTMLField()
    goods = models.ForeignKey('Goods')

    extra = models.CharField(max_length=20,null=True,blank=True) #预留

    class Meta:
        db_table = 'goodscomment'
        verbose_name_plural = '商品评论'

    def __str__(self):
        return self.username

# 购物车
class Cart(models.Model):
    goods_name = models.CharField(max_length=30)
    buy_count = models.IntegerField(default=1)
    is_delete = models.BooleanField(default=False)
    user_cart = models.ForeignKey('UserInfo')

    extra = models.CharField(max_length=20,null=True,blank=True) #预留

    class Meta:
        db_table = 'cart'
        verbose_name_plural = '购物车'

    def __str__(self):
        return self.goods_name

# 订单表
class Orders(models.Model):
    is_finish = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    order_time = models.DateTimeField()
    order_number = models.CharField(max_length=20,null=True,blank=True)
    user_order = models.ForeignKey('UserInfo')

    class Meta:
        db_table = 'orders'
        verbose_name_plural = '订单'

    def __str__(self):
        return self.order_number

# 订单详细表
class OrderDetail(models.Model):
    goods_name = models.CharField(max_length=30)
    goods_price = models.DecimalField(max_digits=7,decimal_places=2)
    buy_count = models.IntegerField()
    order = models.ForeignKey('Orders')
    goods = models.ForeignKey('Goods')

    class Meta:
        db_table = 'orderdetail'
        verbose_name_plural = '订单详细'

    def __str__(self):
        return self.goods_name

# 最近浏览
class RecentSee(models.Model):
    goods_name = models.CharField(max_length=30)
    extra = models.CharField(max_length=20, null=True, blank=True)  # 预留
    user = models.ForeignKey('UserInfo')

    class Meta:
        db_table = 'recentsee'
        verbose_name_plural = '最近浏览'

    def __str__(self):
        return self.goods_name