import random
from django.db import transaction
from models import Product, ProductType, ProductVariant
from decimal import Decimal

# Sample data for generating random products, types, and variants
PRODUCT_NAMES = ["Product"]
PRODUCT_TYPES = ["Boots", "Sneakers"]
SIZES = ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
MAX_STOCK = 100
CATEGORY_CHOICES = ['Men', 'Women', 'Kids']

# Function to create random products, types, and variants


@transaction.atomic
def create_random_products(num_products):
    # Choose random product name, type, and other attributes
    counter = 1  # Initialize counter
    for _ in range(num_products):
        # Choose random product name, type, and other attributes
        name = f"Product {counter}"
        counter += 1  # Increment counter
        product_type = random.choice(PRODUCT_TYPES)
        price = round(random.uniform(10, 1000), 2)
        stock = random.randint(0, MAX_STOCK)
        is_bestseller = random.choice([True, False])
        discount = round(random.uniform(0.25, 0.95), 2)
        category = random.choice(CATEGORY_CHOICES)  # Random category value
    # Create or get product type
    type_instance, _ = ProductType.objects.get_or_create(type=product_type)

    # Create product
    product = Product.objects.create(
        name=name,
        price=Decimal(price),
        product_type=type_instance,
        stock=stock,
        is_bestseller=is_bestseller,
        discount=Decimal(discount),
        category=category
    )

    # Create variants for the product

# Usage example
create_random_products(20)  # Generates 10 random products with variants
