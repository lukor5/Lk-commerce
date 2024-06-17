from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.parsers import JSONParser, MultiPartParser
from shop.models import *
from shop.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash, login
from rest_framework_simplejwt.tokens import AccessToken
from django.middleware.csrf import get_token
from django.core.files.uploadedfile import UploadedFile
from decimal import Decimal
from django.db.models import Count
from django.db.models import Avg
from django.db import transaction
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from utils.dummy_payment_gateway import process_payment
from utils.obfuscate_card_number import obfuscate_card_number
from django.db.models import Q
import json
# Create your views here.


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
    username = body_data.get('username')
    password = body_data.get('password')
    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password.'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        token = AccessToken.for_user(user)
        csrf_token = get_token(request)  # Get CSRF token
        login(request, user)
        if user.is_superuser:
            return JsonResponse({'user_id': user.id, 'token': str(token), 'csrf_token': csrf_token, 'superuser': True})
        else:
            return JsonResponse({'user_id': user.id, 'token': str(token), 'csrf_token': csrf_token, 'superuser': False})
    else:
        return JsonResponse({'error': 'Invalid username or password.'}, status=401)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
        username = body_data.get('username')
        password = body_data.get('password')
        email = body_data.get('email')
        first_name = body_data.get('first_name')
        last_name = body_data.get('last_name')
        if username is None or password is None:
            return JsonResponse({'error': 'Please provide both username and password.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=400)
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return JsonResponse({'success': 'user created'})
    else:
        return JsonResponse({'error': 'Wrong request method.'}, status=400)


def str_to_bool(s):
    """Converts a string to a boolean."""
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError("Cannot covert {} to a boolean value".format(s))


@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        parser_classes = (JSONParser, MultiPartParser)
        name = request.POST.get('name')
        category = request.POST.get('category')
        product = Product.objects.filter(name=name, category=category).exists()
        product_image = request.FILES.get('product_image')
        body = request.POST.get('body')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        # Default to 'false' if not provided
        is_bestseller_str = request.POST.get('is_bestseller', 'false')
        is_bestseller = str_to_bool(is_bestseller_str)
        category = request.POST.get('category')
        type = request.POST.get('type')
        variants_str = request.POST.get('variants')
        variants = json.loads(variants_str)
        product_type = ProductType.objects.get(id=type)

        if product:
            product = Product.objects.get(name=name, category=category)
            product.name = name
            product.body = body
            product.price = price
            product.discount = discount
            product.is_bestseller = is_bestseller
            product.category = category
            product.product_type = product_type
            if product_image:
                product.product_image = product_image
            for variant in variants:
                color = variant.get('color')
                size = variant.get('size')
                stock = variant.get('stock')
                product_variant, created = ProductVariant.objects.get_or_create(
                    product=product,
                    size=size,
                    color=color,
                    defaults={'stock': stock}
                )
                if not created:
                    product_variant.stock = stock
                    product_variant.size = size
                    product_variant.color = color
                    product_variant.save()
            product.save()
            return JsonResponse({'success': 'product updated'})
        elif not product:
            if product_image:
                product = Product.objects.create(name=name, body=body, price=price, discount=discount,
                                                 is_bestseller=is_bestseller, category=category, product_type=product_type, product_image=product_image)
            else:
                product = Product.objects.create(name=name, body=body, price=price, discount=discount,
                                                 is_bestseller=is_bestseller, category=category, product_type=product_type)
            for variant in variants:
                product_variant = ProductVariant.objects.create(
                    product=product, size=variant)
            return JsonResponse({'success': 'product created'})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
def rate_product(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        product_id = data.get('product_id')
        rating = data.get('rating')
        ip = data.get('ip')
        review_body = data.get('review_body')
        name = data.get('name')
        product_rating, created = ProductRating.objects.get_or_create(
            product_id=product_id, ip=ip)
        product_rating.rating = rating
        product_rating.save()
        product = Product.objects.get(pk=product_id)
        average_rating = ProductRating.objects.filter(
            product__id=product_id).aggregate(average=Avg('rating'))['average']
        product.total_rating = average_rating
        product.save()
        if review_body:
            review, created = Review.objects.get_or_create(
                product_rating=product_rating)
            if created:
                review.body = review_body
                review.name = name
                review.save()
            else:
                return JsonResponse({'error': 'Review already added'}, status=403)

        return JsonResponse({'success': 'rating added'})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
def add_to_basket(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        product_id = data.get('product_id')
        user_id = data.get('user_id')
        size = data.get('size')
        color = data.get('color')
        session_key = request.META.get('HTTP_X_SESSION_KEY')

        try:
            product = Product.objects.get(pk=product_id)
            variant = ProductVariant.objects.get(size=size, product=product, color=color) if size else None
            basket, basket_item = add_product_to_basket(user_id, session_key, product, variant)
            return JsonResponse({'success': 'Product added'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except ProductVariant.DoesNotExist:
            return JsonResponse({'error': 'Product variant not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def add_promotion_bundle_to_basket(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        primary_product_id = data.get('primary_product_id')
        discounted_product_id = data.get('discounted_product_id')
        user_id = data.get('user_id')
        size = data.get('size')
        color = data.get('color')
        session_key = request.META.get('HTTP_X_SESSION_KEY')
        discounted_size = data.get('discounted_size')
        discounted_color = data.get('discounted_color')

        try:
            primary_product = Product.objects.get(pk=primary_product_id)
            variant = ProductVariant.objects.get(size=size, product=primary_product, color=color) if size else None

            if not discounted_size or not discounted_color:
                return JsonResponse({'error': 'Both discounted size and color must be provided.'}, status=400)

            discounted_product = Product.objects.get(pk=discounted_product_id)
            promotion = ProductsPromotion.objects.get(primary_product=primary_product, discounted_product=discounted_product)
            discounted_variant = ProductVariant.objects.get(size=discounted_size, color=discounted_color, product=discounted_product)

            promotion_added = add_product_to_basket(
                user_id, session_key, discounted_product, discounted_variant, promotion.discount, check_existing=True
            )

            if not promotion_added:
                return JsonResponse({'error': 'Promotional product already in basket.'}, status=400)

            basket, basket_item = add_product_to_basket(user_id, session_key, primary_product, variant)
            return JsonResponse({'success': 'Promotion bundle added'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except ProductVariant.DoesNotExist:
            return JsonResponse({'error': 'Product variant not found.'}, status=404)
        except ProductsPromotion.DoesNotExist:
            return JsonResponse({'error': 'Promotion not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def add_product_to_basket(user_id, session_key, product, variant, discount=0, check_existing=False):
    if user_id:
        basket, _ = Basket.objects.get_or_create(
            user_id=user_id, order__isnull=True)
        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket, product=product)
    else:
        basket, _ = TemporaryBasket.objects.get_or_create(
            session_key=session_key, order__isnull=True)
        basket_item, created = TemporaryBasketItem.objects.get_or_create(
            temporary_basket=basket, product=product)
    if check_existing and not created:
        return False
    if not check_existing or created:
        basket_item.variant = variant
        basket_item.quantity += 1
        basket_item.save()
        basket.total_price += round(product.price * (product.discount), 2)
        if discount:
            basket.total_price -= discount
        basket.save()
    return basket, basket_item


@csrf_exempt
def update_basket(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        basket_id = data.get('basket_id')
        session_key = data.get('session_key')
        product_id = data.get('product_id')
        variant_data = data.get('variant')
        action = data.get('action')
        variant_id = variant_data.get('id')

        try:
            if basket_id:
                basket = Basket.objects.get(id=basket_id)
                basket_item = BasketItem.objects.get(
                    basket=basket, product_id=product_id, variant_id=variant_id)
            elif session_key:
                basket = TemporaryBasket.objects.filter(session_key=session_key).exclude(
                    order__isnull=False).order_by('-created_at').first()
                basket_item = TemporaryBasketItem.objects.get(
                    temporary_basket=basket, product_id=product_id, variant_id=variant_id)
            else:
                return JsonResponse({'error': 'Invalid basket identifier.'}, status=400)
            
            promotions = ProductsPromotion.objects.filter(
                Q(primary_product_id=product_id) | Q(discounted_product_id=product_id))

            total_discount_reduction = 0
            bundles_to_delete = []

            for promotion in promotions:
                primary_product_in_basket = BasketItem.objects.filter(
                    basket=basket, product=promotion.primary_product).first() if basket_id else \
                    TemporaryBasketItem.objects.filter(
                    temporary_basket=basket, product=promotion.primary_product).first()
                discounted_product_in_basket = BasketItem.objects.filter(
                    basket=basket, product=promotion.discounted_product).first() if basket_id else \
                    TemporaryBasketItem.objects.filter(
                    temporary_basket=basket, product=promotion.discounted_product).first()
                
                if primary_product_in_basket and discounted_product_in_basket:
                    if action == 'delete':
                        total_discount_reduction += (
                            round(primary_product_in_basket.product.price * primary_product_in_basket.product.discount, 2) * primary_product_in_basket.quantity +
                            round(discounted_product_in_basket.product.price * discounted_product_in_basket.product.discount,
                                  2) * discounted_product_in_basket.quantity + promotion.discount
                        )
                        bundles_to_delete.append((primary_product_in_basket, discounted_product_in_basket))
                    else:
                        return JsonResponse({'error': 'Both promotional products are in the basket. No action taken.'}, status=400)

            if action == 'delete' and bundles_to_delete:
                for primary_item, discounted_item in bundles_to_delete:
                    primary_item.delete()
                    discounted_item.delete()
                basket.total_price -= total_discount_reduction - sum([promotion.discount for promotion in promotions])
                basket.save()
                return JsonResponse({'success': 'Bundle(s) deleted'}, status=200)

            elif action == 'decrease':
                if basket_item.quantity > 1:
                    basket_item.quantity -= 1
                    basket.total_price -= round(basket_item.product.price *
                                                basket_item.product.discount, 2)
                    basket_item.save()
                else:
                    return JsonResponse({'error': 'Quantity cannot be less than 1.'}, status=400)
            elif action == 'increase':
                basket_item.quantity += 1
                basket.total_price += round(basket_item.product.price *
                                            basket_item.product.discount, 2)
                basket_item.save()
            elif action == 'delete':
                basket.total_price -= round(basket_item.product.price *
                                            basket_item.product.discount, 2) * basket_item.quantity
                basket_item.delete()
            else:
                return JsonResponse({'error': 'Invalid action.'}, status=400)

            basket.save()
            return JsonResponse({'total_price': str(basket.total_price)}, status=200)

        except (BasketItem.DoesNotExist, TemporaryBasketItem.DoesNotExist):
            return JsonResponse({'error': 'Basket item not found.'}, status=404)
        except Basket.DoesNotExist:
            return JsonResponse({'error': 'Basket not found.'}, status=404)

@csrf_exempt
def merge_baskets(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
        user_id = body_data.get('user_id')
        session_key = body_data.get('session_key')
        print("Received user_id:", user_id)
        print("Received session_key:", session_key)
        user = User.objects.get(pk=user_id)
        print("received user:", user)
        try:
            temporary_basket = TemporaryBasket.objects.get(
                session_key=session_key)
        except TemporaryBasket.DoesNotExist:
            return JsonResponse({'message': 'No temporary basket to merge'}, status=200)
        temporary_items = TemporaryBasketItem.objects.filter(
            temporary_basket=temporary_basket)
        basket, _ = Basket.objects.get_or_create(
            user=user, order__isnull=True)
        print("basket:", basket)
        print("basket_id", basket.id, basket.user)
        basket.total_price += temporary_basket.total_price
        for temporary_item in temporary_items:
            existing_item = BasketItem.objects.filter(
                basket=basket, product=temporary_item.product, variant=temporary_item.variant).first()
            if existing_item:
                existing_item.quantity += temporary_item.quantity
                existing_item.save()
            else:
                BasketItem.objects.create(basket=basket, product=temporary_item.product,
                                          quantity=temporary_item.quantity, variant=temporary_item.variant)
        basket.save()
        temporary_items.delete()
        temporary_basket.delete()
        return JsonResponse({'message': 'Baskets merged successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def user_basket(request, user_id=None):
    if request.method == 'GET':
        serialized_data = []
        session_key = request.META.get('HTTP_X_SESSION_KEY')
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            basket = get_object_or_404(Basket.objects.filter(
                user=user).exclude(order__isnull=False))
            basket_id = basket.id
            basket_items = BasketItem.objects.filter(basket=basket_id)
            for basket_item in basket_items:
                serialized_item = BasketItemSerializer(basket_item).data
                product = basket_item.product
                variant = basket_item.variant
                variant_details = ProductVariantSerializer(variant).data
                variant_details['id'] = variant.id
                product_details = ProductSerializer(product).data
                serialized_item['product'] = product_details
                serialized_item['variant'] = variant_details
                serialized_item['total_price'] = basket.total_price
                serialized_data.append(serialized_item)
            # Return the response here
            return JsonResponse(serialized_data, safe=False)
        else:
            if session_key:
                try:
                    basket = TemporaryBasket.objects.filter(session_key=session_key).exclude(
                        order__isnull=False).order_by('-created_at').first()
                    basket_id = basket.id
                    basket_items = TemporaryBasketItem.objects.filter(
                        temporary_basket=basket_id)

                    for basket_item in basket_items:
                        serialized_item = TemporaryBasketItemSerializer(
                            basket_item).data
                        product = basket_item.product
                        variant = basket_item.variant
                        variant_details = ProductVariantSerializer(
                            variant).data
                        variant_details['id'] = variant.id
                        product_details = ProductSerializer(product).data
                        serialized_item['product'] = product_details
                        serialized_item['variant'] = variant_details
                        serialized_item['total_price'] = basket.total_price
                        serialized_data.append(serialized_item)
                    return JsonResponse(serialized_data, safe=False)
                except TemporaryBasket.DoesNotExist:
                    return JsonResponse({'error': 'Basket not found for the given session key'}, status=404)


def product_list(request):
    if request.method == 'GET':
        product_type = request.GET.get('type')
        category = request.GET.get('category')
        one_week_ago = datetime.now() - timedelta(days=7)
        if category == 'New':
            if product_type == 'All':
                products = Product.objects.filter(created_at__gte=one_week_ago)
            else:
                products = Product.objects.filter(
                product_type__type=product_type, created_at__gte=one_week_ago)
        elif product_type == 'All':
            products = Product.objects.filter(category=category)
        elif product_type is None and category is None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(
                product_type__type=product_type, category=category)

        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)


def promotions_list(request):
    if request.method == 'GET':
        promotions = ProductsPromotion.objects.all()
        serializer = ProductsPromotionSerializer(promotions, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request methods'}, status=405)


def single_product(request, pk):
    if request.method == 'GET':
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            response_data = serializer.data
        except Product.DoesNotExist:
            return HttpResponse(status=404)
    return JsonResponse(response_data)


def bestsellers(request):
    if request.method == 'GET':
        bestseller_products = Product.objects.filter(is_bestseller=True)
        serializer = ProductSerializer(bestseller_products, many=True)
        return JsonResponse(serializer.data, safe=False)


def delivery_list(request):
    if request.method == 'GET':
        deliveries = Delivery.objects.all()
        try:
            serializer = DeliverySerializer(deliveries, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Delivery.DoesNotExist:
            return HttpResponse(status=404)


@csrf_exempt
def set_default_delivery(request):
    data = json.loads(request.body.decode('utf-8'))
    id = data.get('user_id')
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        city = data.get('city')
        zip_code = data.get('zipCode')
        street = data.get('street')
        apartment_number = data.get('apartmentNumber')
        email = data.get('email')
        phone = data.get('phone')
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        default_delivery, created = DefaultDelivery.objects.get_or_create(
            user=user)
        default_delivery.city = city
        default_delivery.zip_code = zip_code
        default_delivery.street = street
        default_delivery.apartment_number = apartment_number
        default_delivery.email = email
        default_delivery.phone = phone
        default_delivery.first_name = first_name
        default_delivery.last_name = last_name
        default_delivery.save()
        return JsonResponse({'success': 'Order created'}, status=200)
    else:
        return JsonResponse({'error', 'Invalid request method'}, status=405)


def get_default_delivery(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    try:
        default_delivery = DefaultDelivery.objects.get(user=user)
    except DefaultDelivery.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DefaultDeliverySerializer(default_delivery)
        return JsonResponse(serializer.data)


def single_delivery(request, pk):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Delivery.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DeliverySerializer(delivery)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request, pk=pk)
        serializer = DeliverySerializer
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def user_delivery(request, id):
    try:
        delivery = Delivery.objects.filter(user__id == id)
    except Delivery.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DeliverySerializer(delivery)
        return JsonResponse(serializer.data)


def product_type(request):
    data = request.GET
    category = data.get('category')
    product_types = ProductType.objects.all()

    if category is not None:
        
        product_count_per_type = {}
        if category == 'New':
            one_week_ago = datetime.now() - timedelta(days=7)
            for product_type in product_types:
                count = Product.objects.filter(
                     product_type=product_type, created_at__gte=one_week_ago).count()
                product_count_per_type[product_type.id] = count
        else:
            for product_type in product_types:
                count = Product.objects.filter(
                    category=category, product_type=product_type).count()
                product_count_per_type[product_type.id] = count
        serializer_data = ProductTypeSerializer(product_types, many=True).data
        for item in serializer_data:
            item['count'] = product_count_per_type.get(item['id'], 0)
        return JsonResponse(serializer_data, safe=False)
    else:
        serializer = ProductTypeSerializer(product_types, many=True)
        return JsonResponse(serializer.data, safe=False)


def categories_list(request):
    categories = [choice[1] for choice in Product.CATEGORY_CHOICES]
    if request.method == 'GET':
        return JsonResponse({'categories': categories}, safe=False)


def product_variants(request, id):
    try:
        product_variants = ProductVariant.objects.filter(product__id == id)
    except ProductVariant.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductVariantSerializer(product_variants, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        session_key = request.META.get('HTTP_X_SESSION_KEY')
        user_id = data.get('user_id')
        cvv = data.get('cvv')
        card_number = data.get('card_number')
        expiry_date = data.get('expiry_date')
        order_id = data.get('order_id')
        order = Order.objects.get(pk=order_id)
        if user_id:
            user = User.objects.get(pk=user_id)
            basket = order.basket
        else:
            basket = order.temporary_basket
        total_price = basket.total_price
        success, message, error = process_payment(
            total_price, card_number, expiry_date, cvv)
        if not success:
            return JsonResponse({'error': message, 'details': error}, status=400)
        else:
            order.status = 'Paid'
            order.save()
            payment_date = datetime.now()
            obfuscated_card_number = obfuscate_card_number(card_number)
            Payment.objects.create(
                user=user,
                order=order,
                card_number_obfuscated=obfuscated_card_number,
                amount=total_price,
                expiry_date = expiry_date,
                payment_date = payment_date
            )
            eligible_templates = VoucherTemplate.objects.filter(
                required_cash_spent__lte=total_price).order_by('-required_cash_spent')
            if eligible_templates.exists():
                selected_template = eligible_templates.first()
                email = order.delivery.email
                if user:
                    voucher = Voucher.objects.create(
                        template=selected_template, user=user)
                else:
                    voucher = Voucher.objects.create(
                        template=selected_template)
                subject = 'You received a new voucher!'
                valid_until = voucher.valid_until.strftime('%d-%m-%Y')
                message = (
                    f'Your new voucher is: {voucher.code}.\n\n'
                    f'This voucher gives you {
                        voucher.template.discount} $ discount on your new purchase.\n\n'
                    f'The voucher is valid to use until {valid_until}\n\n'
                    'Happy shopping!'
                )
                email_from = 'lkcommercetest@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
            return JsonResponse({'success': message}, status=200)


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        session_key = request.META.get('HTTP_X_SESSION_KEY')
        delivery_name = data.get('delivery_method')
        delivery_method = DeliveryMethod.objects.get(name=delivery_name)
        if user_id:
            user = User.objects.get(pk=user_id)
            basket = Basket.objects.filter(user=user).exclude(
                order__isnull=False).order_by('-created_at').first()
            delivery_defaults = {
                'city': data.get('city'),
                'street': data.get('street'),
                'zip_code': data.get('zip_code'),
                'phone': data.get('phone'),
                'user': user,
                'apartment_number': data.get('apartment_number'),
                'delivery_method': delivery_method,
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email')
            }
            delivery = Delivery.objects.create(**delivery_defaults)
            order = Order.objects.create(
                basket=basket, delivery=delivery, user=user)
            staff_users = User.objects.filter(is_staff=True)
            message = (
                  f'New order with Id {order.id} has been created'
            )
            for staff_user in staff_users:
                notification = Notification.objects.create(user=staff_user, message = message)
                notification.save()
            return JsonResponse({'success': 'Order created', 'order_id': order.id}, status=200)
        elif session_key:
            temporary_basket = TemporaryBasket.objects.filter(session_key=session_key).exclude(
                order__isnull=False).order_by('-created_at').first()
            delivery_defaults = {
                'city': data.get('city'),
                'street': data.get('street'),
                'zip_code': data.get('zip_code'),
                'phone': data.get('phone'),
                'apartment_number': data.get('apartment_number'),
                'delivery_method': delivery_method,
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email')
            }
            delivery = Delivery.objects.create(**delivery_defaults)
            Order.objects.create(
                temporary_basket=temporary_basket, delivery=delivery)
            return JsonResponse({'success': 'Order created'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


def order_list(request):
    if request.method == 'GET':

        orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def review_list(request, id):
    if request.method == 'GET':
        ratings = ProductRating.objects.filter(product_id=id)
        serializer = ProductRatingSerializer(ratings, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def order(request, pk):
    if request.method == 'GET':
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def user_orders(request, user_id):
    if request.method == 'GET':
        orders = Order.objects.filter(user=user_id)
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_order(request):
    body_data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        order_id = body_data.get('order_id')
        status = body_data.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        if status == 'Paid':
            try:
                user = None
                total_price = 0.00
                if getattr(order, 'basket', None) is not None:
                    user = order.user
                    total_price = order.basket.total_price
                elif getattr(order, 'temporary_basket', None) is not None:
                    total_price = order.temporary_basket.total_price
                else:
                    return JsonResponse({'error': 'No basket found'}, status=404)
                eligible_templates = VoucherTemplate.objects.filter(
                    required_cash_spent__lte=total_price
                ).order_by('-required_cash_spent')

                if eligible_templates.exists():
                    selected_template = eligible_templates.first()
                    email = order.delivery.email
                    if user:
                        voucher = Voucher.objects.create(
                            template=selected_template, user=user)
                    else:
                        voucher = Voucher.objects.create(
                            template=selected_template)
                    subject = 'You received a new voucher!'
                    valid_until = voucher.valid_until.strftime('%d-%m-%Y')
                    message = (
                        f'Your new voucher is: {voucher.code}.\n\n'
                        f'This voucher gives you {
                            voucher.template.discount} $ discount on your new purchase.\n\n'
                        f'The voucher is valid to use until {valid_until}\n\n'
                        'Happy shopping!'
                    )
                    email_from = 'lkcommercetest@gmail.com'
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list)
                    return JsonResponse({'success': 'Order updated and voucher generated'})
                else:
                    return JsonResponse({'success': 'Order updated, no voucher generated'})

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        order.save()
        return JsonResponse({'success': 'Order updated'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def apply_voucher(request):
    data = JSONParser().parse(request)
    if request.method == 'POST':
        code = data.get('code')
        try:
            voucher = Voucher.objects.get(code=code)
            if voucher.is_spent is False:
                discount = voucher.template.discount
                print(f"Discount: {discount}")

                temporary_basket_id = data.get('temporary_basket')
                basket_id = data.get('basket')
                with transaction.atomic():
                    if basket_id is not None:
                        basket = Basket.objects.get(id=basket_id)
                        new_total = max(basket.total_price - discount, 0)
                        if new_total > 0:
                            basket.total_price = new_total
                            basket.voucher_applied = True
                            basket.save()
                            voucher.is_spent = True
                            voucher.save()
                        else:
                            return JsonResponse({'error': 'Basket total price after voucher must be above 0'}, status=403)
                    elif temporary_basket_id is not None:
                        temporary_basket = TemporaryBasket.objects.get(
                            id=temporary_basket_id)
                        new_total = max(
                            temporary_basket.total_price - discount, 0)
                        if new_total > 0:
                            temporary_basket.total_price = new_total
                            temporary_basket.voucher_applied = True
                            temporary_basket.save()
                            voucher.is_spent = True
                            voucher.save()
                        else:
                            return JsonResponse({'error': 'Basket total price after voucher must be above 0'}, status=403)
                return JsonResponse({'success': 'Voucher applied successfully'})
            else:
                return JsonResponse({'error': 'Voucher already spent'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
def user_vouchers(request, user_id):
    if request.method == 'GET':
        try:
            vouchers = Voucher.objects.filter(user=user_id)
            serializer = VoucherSerializer(vouchers, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Voucher.DoesNotExist:
            return JsonResponse({'error': 'No vouchers found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def send_test_email(request):
    subject = 'Hello from Django'
    message = 'This is a test email sent from a Django application.'
    email_from = 'lkcommercetest@gmail.com'
    recipient_list = ['oleslukasz7@gmail.com']

    send_mail(subject, message, email_from, recipient_list)

    return HttpResponse("Email sent successfully")


@csrf_exempt
def change_password(request, user_id):
    try:
        data = json.loads(request.body)
        password = data.get('password')
        new_password = data.get('new_password')
        user = User.objects.get(id=user_id)
        authenticated = authenticate(
            username=user.username, password=password, request=request)
        if authenticated:
            if not new_password:
                return JsonResponse({'error': 'New password should not be empty'}, status=400)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': 'Password changed successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Wrong password'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def send_recovery_code(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        user = User.objects.get(email=email)
        RecoveryCode.objects.filter(user=user).delete()
        recovery_code = RecoveryCode.objects.create(user=user)
        recovery_code.save()

        subject = 'Password recovery code'
        message = f'Your recovery code is: {recovery_code.code}'
        email_from = 'lkcommercetest@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, email_from, recipient_list)

        return JsonResponse({'success': 'Recovery code sent successfully'}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def recover_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        data = json.loads(request.body)
        code = data.get('recovery_code')
        email = data.get('email')
        if not code:
            return JsonResponse({'error': 'Recovery code is required'}, status=400)

        user = User.objects.get(email=email)
        recovery_code = RecoveryCode.objects.get(user=user)
        if recovery_code.code == code:
            return JsonResponse({'success': 'Recovery code matches'}, status=200)
        else:
            return JsonResponse({'error': 'Wrong recovery code'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def set_recovered_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        data = json.loads(request.body)
        new_password = data.get('new_password')
        email = data.get('email')
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'success': 'New password set succesfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt 
def create_promotion_bundle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        primary_product_id = data.get('primary_product')
        discounted_product_id = data.get('discounted_product')
        primary_product = Product.objects.get(id=primary_product_id)
        discounted_product = Product.objects.get(id=discounted_product_id)
        discount = data.get('discount')
        id = data.get('id')
        if primary_product_id == discounted_product_id:
            return JsonResponse({'error': 'Bundle can not consist of two same products'}, status=403)
        else:
            if id is not None:
                promotion = ProductsPromotion.objects.get(id=id)
                promotion.primary_product = primary_product
                promotion.discounted_product = discounted_product
                promotion.discount = discount
                promotion.save()
                return JsonResponse({'success': 'Bundle created successfully'}, status=200)
            else:
                promotion, created = ProductsPromotion.objects.get_or_create(primary_product=primary_product, discounted_product=discounted_product, discount=discount)
                if not created: 
                    return JsonResponse({'error': 'Bundle already exists'}, status=403)
                else:
                    promotion.save()
                    return JsonResponse({'success': 'Bundle created successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error', 'Invalid request method'}, status=400)
@csrf_exempt
def email_customer(request):
    parser_classes = (JSONParser, MultiPartParser)

    if request.method == 'POST':
        user_data = request.POST.get('user')
        user = json.loads(user_data)
        email = user.get('email')
        if User.objects.filter(email=email).exists():
            subject = request.POST.get('subject')
            body = request.POST.get('body')
            email_from = 'lkcommercetest@gmail.com'
            recipient_list = [email]
            email_message = EmailMessage(subject, body, email_from, recipient_list)
            for key, file in request.FILES.items():
                if hasattr(file, 'name'):
                    email_message.attach(file.name, file.read(), file.content_type)
            email_message.send()
        else:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        return JsonResponse({'success': 'Email send succesfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def payment_list(request):
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def popular_types(request):
    types = ProductType.objects.all()
    type_counts = []
    for type in types:
        type_dict = {"type": type.type, "count": 0}
        type_counts.append(type_dict)
    if request.method == 'GET':  
        orders = Order.objects.all()       
        for order in orders:
            if order.basket:
                basket = order.basket
            else:
                basket = order.temporary_basket
            for product in basket.products.all():
                product_type = product.product_type.type
                for type_dict in type_counts:
                    if type_dict["type"] == product_type:
                        type_dict["count"] += 1
                        break 
        return JsonResponse({"type_counts": type_counts})
    else:
        return JsonResponse({'error': 'Invalid request methods'}, status=400) 
    
def popular_products(request):
    products = Product.objects.all()
    product_counts = []
    for product in products:
        product_dict = {"product": product.id, "product_name": product.name, "product_category": product.category, "count": 0}
        product_counts.append(product_dict)
    if request.method == 'GET':  
        orders = Order.objects.all()       
        for order in orders:
            if order.basket:
                basket = order.basket
            else:
                basket = order.temporary_basket
            for product in basket.products.all():
                for product_dict in product_counts:
                    if product_dict["product"] == product.id:
                        product_dict["count"] += 1
                        break 
        sorted_product_counts = sorted(product_counts, key=lambda x: x['count'], reverse=True)
        top_10_products = sorted_product_counts[:10]
        return JsonResponse({"product_counts": top_10_products})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400) 

@csrf_exempt    
def unread_notifications(request):
    notifications = Notification.objects.filter(is_read=False)
    if request.method == 'GET':
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt    
def all_notifications(request):
    notifications = Notification.objects.all()
    if request.method == 'GET':
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def notification_read(request):
    data = json.loads(request.body)
    notification_id = data.get('notification_id')
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(notification = notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': 'Notification read'})
        except notification.DoesNotExist:
            return JsonResponse({'error': 'Notification does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt    
def mark_all_as_read(request):
    data = json.loads(request.body)
    user = data.get('user_id')
    if request.method == 'POST':
        notifications = Notification.objects.filter(user=user)
        for notification in notifications:
            notification.is_read = True
            notification.save()
        return JsonResponse({'success': 'All notifications marked as read'})
    else: 
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    