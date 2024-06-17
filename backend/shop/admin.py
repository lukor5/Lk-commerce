from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(Delivery)
admin.site.register(ProductType)
admin.site.register(Order)
admin.site.register(ProductVariant)
admin.site.register(TemporaryBasket)
admin.site.register(DeliveryMethod)
admin.site.register(ProductRating)
admin.site.register(Review)
admin.site.register(VoucherTemplate)
admin.site.register(Voucher)
admin.site.register(DefaultDelivery)
admin.site.register(ProductsPromotion)
admin.site.register(Payment)

# Register your models here.
