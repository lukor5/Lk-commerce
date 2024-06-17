import random
import sys
import os
import django
from django.core.files import File
sys.path.append(r'C:\Users\Light\lkcommerce\backend')
from lkcommerce import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lkcommerce.settings')

# Configure Django settings
django.setup()

from django.db import transaction
from shop.models import Product, ProductVariant
from decimal import Decimal


COLORS = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Black', 'White', 'Gray', 'Brown', 'Beige']
BRAND_CHOICES = ['StyleVista', 'UrbanWeave', 'GlamourGlitz', 'TrendThread', 'ChicShack', 'VogueValley', 'ModeMosaic', 'FabricFable', 'AttireAura', 'WearWhisper', 'OutfitOracle', 'FashionFlare']
raw_path = r'C:\Users\Light\lkcommerce\backend\media'

@transaction.atomic
def appendColorsAndBrands():
    products = Product.objects.all()
    variants = ProductVariant.objects.all()
    for product in products:
        product.brand = random.choice(BRAND_CHOICES)
        product.save()
    for variant in variants:
        variant.color = random.choice(COLORS)
        variant.save()

appendColorsAndBrands()