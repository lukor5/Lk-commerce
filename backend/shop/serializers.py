from rest_framework import serializers
from shop.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined']
        
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['city', 'street', 'apartment_number', 'phone', 'user', 'delivery_method', 'zip_code']

class DefaultDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultDelivery
        fields = ['city', 'street', 'apartment_number', 'phone', 'user', 'zip_code', 'first_name', 'last_name', 'email']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'type']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'stock', 'color']
class ProductRatingSerializer (serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['id', 'rating', 'ip' ]

class ProductSerializer (serializers.ModelSerializer):
    product_variants = ProductVariantSerializer(many=True, source='productvariant_set')
    product_ratings = ProductRatingSerializer(many=True, source='productrating_set')
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_image', 'body', 'status', 'price', 'category', 'product_type', 'product_variants', 'product_ratings', 'total_rating', 'discount', 'is_bestseller', 'brand', 'created_at']

class ProductsPromotionSerializer(serializers.ModelSerializer):
    primary_product = ProductSerializer()
    discounted_product = ProductSerializer()
    class Meta:
        model = ProductsPromotion
        fields = ['id', 'primary_product', 'discounted_product', 'discount']

class TemporaryBasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variant = ProductVariantSerializer()
    class Meta:
        model = TemporaryBasketItem
        fields = ['temporary_basket', 'product', 'variant' ,'quantity']

class TemporaryBasketSerializer(serializers.ModelSerializer):
    items = TemporaryBasketItemSerializer(many=True, source='temporarybasketitem_set')
    class Meta:
        model = Basket
        fields = ['total_price', 'items']
        
class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variant = ProductVariantSerializer()
    class Meta:
        model = BasketItem
        fields = ['basket', 'product', 'variant' ,'quantity']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, source='basketitem_set')
    class Meta:
        model = Basket
        fields = ['total_price', 'user', 'items']

class OrderSerializer(serializers.ModelSerializer):
    basket = BasketSerializer(read_only=True)
    temporary_basket = TemporaryBasketSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'basket','temporary_basket', 'delivery','status', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'body', 'product_rating']

class ProductRatingSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=False, read_only=True)
    class Meta:
        model = ProductRating
        fields = ['product', 'rating', 'review', 'created_at']
class VoucherTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherTemplate
        fields = ['name', 'discount']

class VoucherSerializer(serializers.ModelSerializer):
    template = VoucherTemplateSerializer(read_only=True)
    class Meta:
        model = Voucher
        fields = ['code', 'valid_from', 'valid_until', 'is_spent', 'template']

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    order = OrderSerializer(read_only = True) 
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'card_number_obfuscated', 'amount', 'payment_date', 'expiry_date']

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']