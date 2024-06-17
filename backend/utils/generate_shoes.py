import random
import sys
import os
import django
from django.core.files import File
sys.path.append(r'/home/ubuntu/Lk-commerce/backend')
from lkcommerce import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lkcommerce.settings')

# Configure Django settings
django.setup()

from django.db import transaction
from shop.models import Product, ProductType, ProductVariant
from decimal import Decimal

# Sample data for generating random products, types, and variants
PRODUCT_NAMES = ["Product"]
PRODUCT_TYPES = ["Boots", "Sneakers"]
SIZES = ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
COLORS = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Black', 'White', 'Gray', 'Brown', 'Beige']
BRAND_CHOICES = ['StyleVista', 'UrbanWeave', 'GlamourGlitz', 'TrendThread', 'ChicShack', 'VogueValley', 'ModeMosaic', 'FabricFable', 'AttireAura', 'WearWhisper', 'OutfitOracle', 'FashionFlare']
MAX_STOCK = 100
CATEGORY_CHOICES = ['Men', 'Women', 'Kids']
sys.path.append(r'/home/ubuntu/Lk-commerce/backend/media')
# Function to create random products, types, and variants


@transaction.atomic
def create_random_products(num_products):
    # Choose random product name, type, and other attributes
    counters = {product_type: 0 for product_type in PRODUCT_TYPES}
    for _ in range(num_products):
        # Choose random product name, type, and other attributes
        body = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec aliquet fringilla lorem sit amet posuere. In aliquet tincidunt aliquet."
        product_type = random.choice(PRODUCT_TYPES)
        counters[product_type] += 1
        counter = counters[product_type]
        brand = random.choice(BRAND_CHOICES)
        name = f"{product_type} {counter}"
        price = round(random.uniform(10, 100), 2)
        stock = random.randint(0, MAX_STOCK)
        is_bestseller = random.choices([True, False], weights=[1, 4], k=1)[0]
        discount = round(random.uniform(0.25, 0.95), 2)
        category = random.choice(CATEGORY_CHOICES)  # Random category value

        # Create or get product type
        type_instance, _ = ProductType.objects.get_or_create(type=product_type)

        # Create product
        product = Product.objects.create(
            name=name,
            body=body,
            brand=brand,
            price=Decimal(price),
            product_type=type_instance,
            is_bestseller=is_bestseller,
            discount=Decimal(discount),
            category=category,
        )
        num_sizes = min(random.randint(1, 5), len(SIZES))
      
        product_sizes = random.sample(SIZES, num_sizes)
        
    # Create variants for the product
        for size in product_sizes:
            num_colors = min(random.randint(1, 5), len(COLORS))
            product_colors = random.sample(COLORS, num_colors)
            for color in product_colors:
                ProductVariant.objects.create(
                    color=color,
                    product=product,
                    size=size,
                    stock=stock
                )


# Usage example
create_random_products(20)  # Generates 10 random products with variants
