from django.contrib import admin
from index import models

admin.site.register(models.UserInfo)
admin.site.register(models.AreaInfo)
admin.site.register(models.AddrInfo)
admin.site.register(models.GoodSort)
admin.site.register(models.Goods)
admin.site.register(models.RecentSee)
admin.site.register(models.Orders)
admin.site.register(models.OrderDetail)
admin.site.register(models.GoodsComment)
admin.site.register(models.Cart)




