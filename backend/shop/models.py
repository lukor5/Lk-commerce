from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .utils import generate_voucher
from dateutil.relativedelta import relativedelta
import pytz  
from django.utils import timezone
from django.utils.crypto import get_random_string
class ProductType(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.type}"

class Product(models.Model):
    name = models.CharField(max_length=30)
    product_image = models.ImageField(upload_to='products', default="generic-product-image.jpg")
    body = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    brand = models.CharField(max_length=20, default='Generic Brand')
    total_rating = models.DecimalField(max_digits=2, decimal_places=1, default=3)
    is_bestseller = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10) 
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=15, blank=True, null=True)

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(
        max_digits = 2,
        decimal_places = 1,
        default = 3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    ip = models.CharField(max_length=40)

class Basket(models.Model):
    total_price = models.DecimalField(max_digits= 7, decimal_places = 2, default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="BasketItem", related_name='baskets')
    created_at = models.DateTimeField(auto_now_add=True)
    voucher_applied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"

class TemporaryBasket(models.Model):
    session_key = models.CharField(max_length=40, default='none')
    total_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    products = models.ManyToManyField(Product, through="TemporaryBasketItem", related_name='temporary_baskets')
    created_at = models.DateTimeField(auto_now_add=True)
    voucher_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"Temporary Basket {self.id}"
class TemporaryBasketItem(models.Model):
    temporary_basket = models.ForeignKey(TemporaryBasket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} in Basket for {self.temporary_basket}"

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} in Basket for {self.basket.user.username}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)  # Assuming prices can go up to 9999.99

    def __str__(self):
        return f"{self.name} (${self.price})"

class Delivery(models.Model):
    city = models.CharField(max_length=30, default="")
    street = models.CharField(max_length=50, default="")
    apartment_number = models.CharField(max_length=10, default="")
    zip_code = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.city} "

class DefaultDelivery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='default_delivery')
    city = models.CharField(max_length=30, default="")
    street = models.CharField(max_length=50, default="")
    apartment_number = models.CharField(max_length=10, default="")
    zip_code = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True, blank=True)
    temporary_basket = models.ForeignKey(TemporaryBasket, on_delete=models.CASCADE, null=True, blank=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Ordered', 'Ordered'),
        ('Paid', 'Paid'),
        ('Sent', 'Sent'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default='Ordered')

    def __str__(self):
        return f"{self.id}"

class Review(models.Model):
    product_rating = models.OneToOneField(ProductRating, on_delete=models.CASCADE, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField()
    body = models.TextField(verbose_name="Review Body")

    def __str__(self):
        return f"Review by {self.user.username if self.user else 'Anonymous'} for Rating ID {self.product_rating.id}"
    
class ProductsPromotion(models.Model):
    primary_product = models.ForeignKey(Product, related_name='primary_promotions', on_delete=models.CASCADE)
    discounted_product = models.ForeignKey(Product, related_name='discount_promotions', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.primary_product.name} -> {self.discounted_product.name} ({self.discount}% off)"
    
class VoucherTemplate(models.Model):
    name = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    required_cash_spent = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name
    
class Voucher(models.Model): 
    code = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    template = models.ForeignKey(VoucherTemplate, on_delete=models.CASCADE, blank=True, null=True)
    valid_from = models.DateTimeField(null=True, auto_now_add=True)
    valid_until = models.DateTimeField(null=True)
    is_spent = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id}"
    def save(self, *args, **kwargs):
        if not self.code:  # Only generate if code does not already exist
            potential_code = generate_voucher(12)
            while Voucher.objects.filter(code=potential_code).exists():
                potential_code = generate_voucher(12)
            self.code = potential_code
            self.valid_until = timezone.now() + relativedelta(years=1)
        super(Voucher, self).save(*args, **kwargs)

class RecoveryCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recovery_code')
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(12)
        super().save(*args, **kwargs)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number_obfuscated = models.CharField(max_length=19)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(blank=True)
    expiry_date = models.CharField(max_length=7, default='01/2026')
    
    def save(self, *args, **kwargs):
        if not self.card_number_obfuscated:
            raise ValueError("Card number should be obfuscated before saving.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment by {self.user} for {self.order} on {self.payment_date}"