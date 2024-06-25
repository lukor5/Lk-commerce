import random
import sys
import os
import django
from django.core.files import File
from django.db.models import Avg
sys.path.append(r'/home/ubuntu/Lk-commerce/backend')
from lkcommerce import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lkcommerce.settings')

# Configure Django settings
django.setup()

from django.db import transaction
from shop.models import Product, ProductRating, Review
from django.contrib.auth.models import User
from decimal import Decimal

# Predefined data
RATINGS = [1.0, 2.0, 3.0, 4.0, 5.0]
NAMES = [
    'SpeedyGonzalez', 'GreenThumbLucy', 'PixelWizard', 'BookwormBeth', 'SneakerHeadTom',
    'ChefMike', 'TechSavvyTina', 'FrequentFlyer', 'PianoMaster', 'CraftyCara'
]
review_data = {
    1.0: {"review": "Horrible experience! The product broke down the first time I used it and the support was non-existent. Completely a waste of money!"},
    2.0: {"review": "Somewhat disappointed. It functions, but not up to the level advertised. I had higher expectations based on the product description."},
    3.0: {"review": "It's okay, does the job but nothing to write home about. Could use some improvements but it works well enough for now."},
    4.0: {"review": "Quite good! There are a few minor issues, but overall it’s a solid product. I'm happy with what I got for the price."},
    5.0: {"review": "Absolutely perfect! Exceeds all my expectations and I'm thoroughly impressed. Would definitely buy again and recommend to everyone!"}
}

@transaction.atomic
def create_random_ratings(nums):
    products = Product.objects.all()
    for product in products:
        for _ in range(nums):
            rating = random.choice(RATINGS)
            ProductRating.objects.create(product_id = product.id, rating=rating)
        average_rating = ProductRating.objects.filter(product=product).aggregate(average=Avg('rating'))['average']
        product.total_rating = average_rating
        product.save()
    product_ratings = ProductRating.objects.all()
    for product_rating in product_ratings:
        rating = product_rating.rating
        name = random.choice(NAMES)
        body = review_data[rating]["review"]
        Review.objects.create(product_rating_id = product_rating.id, body=body, name=name)


# Create ratings and reviews
create_random_ratings(20)