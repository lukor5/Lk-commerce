import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
sys.path.append(r'/home/ubuntu/Lk-commerce/backend')
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lkcommerce.settings')
django.setup()
from django.contrib.auth.models import User
from shop.models import Payment, Order

def generate_random_card_number():
    """Generate a random card number in the format **** **** **** ****"""
    return str(random.randint(1000, 9999)) + " **** **** " + str(random.randint(1000, 9999))

def random_date_within_6_months():
    """Generate a random date within the last 6 months"""
    today = datetime.now()
    start_date = today - timedelta(days=180)
    random_date = start_date + (today - start_date) * random.random()
    return random_date

def generate_random_amount():
    """Generate a random payment amount"""
    return round(Decimal(random.uniform(10.00, 1000.00)), 2)

def create_random_payment():
    users = list(User.objects.all())
    orders = list(Order.objects.all())

    if not users or not orders:
        print("No users or orders found. Please ensure you have data in these tables.")
        return

    random_user = random.choice(users)
    random_order = random.choice(orders)
    payment = Payment(
        user=random_user,
        order=random_order,
        card_number_obfuscated=generate_random_card_number(),
        amount=generate_random_amount(),
        payment_date=random_date_within_6_months(),
        expiry_date='01/2026'
    )
    payment.save()
    print(f'Payment created with ID: {payment.id}')

# Generate a specified number of random payments
def generate_payments(count=10):
    for _ in range(count):
        create_random_payment()

# Example usage
generate_payments(50)  # Generate 50 random payments