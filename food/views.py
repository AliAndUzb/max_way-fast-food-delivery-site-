import json
from config.settings import MEDIA_ROOT
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .services import *
from .forms import *
from .models import Customer, Product, OrderProduct, Category



# def index_page(request):
#     return HttpResponse("Bu yerda index_page ko'rinishi kerak")

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get('orders')
    total_price = request.COOKIES.get('total_price', 0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                    'product': get_object_or_404(Product, pk=int(key)),
                    'count': val
                }
            )
    context = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price
    }
    return render(request, 'food/index.html', context)




# def index(request):
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     orders = []
#
#     orders_list = request.COOKIES.get('orders')
#     total_price = request.COOKIES.get('total_price', 0)
#
#     try:
#         # Convert total_price to a numeric value if needed
#         total_price = float(total_price)
#     except ValueError:
#         total_price = 0
#
#     if orders_list:
#         try:
#             orders_dict = json.loads(orders_list)
#         except json.JSONDecodeError:
#             return HttpResponseBadRequest("Invalid cookie format")
#
#         # Collect all product IDs
#         product_ids = list(map(int, orders_dict.keys()))
#         products = Product.objects.filter(pk__in=product_ids)
#
#         # Create a dictionary of products for quick lookup
#         product_dict = {product.pk: product for product in products}
#
#         for key, val in orders_dict.items():
#             product = product_dict.get(int(key))
#             if product:
#                 orders.append(
#                     {
#                         'product': product,
#                         'count': val
#                     }
#                 )
#
#     context = {
#         'categories': categories,
#         'products': products,
#         'orders': orders,
#         'total_price': total_price
#     }
#     return render(request, 'food/index.html', context)


def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get('product', 0))
        return JsonResponse(product, safe=False)


def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number", 0))
        return JsonResponse(user, safe=False)


# def main_order(request):
#     # Attempt to retrieve or create a new Customer instance
#     customer, created = None, False
#
#     if request.POST:
#         # Try to retrieve the customer based on phone number
#         phone_number = request.POST.get('phone_number', "")
#         if phone_number:
#             customer, created = Customer.objects.get_or_create(phone_number=phone_number)
#
#         # Bind the CustomerForm to the POST data
#         form = CustomerForm(request.POST, instance=customer)
#
#         if form.is_valid():
#             customer = form.save()  # Save the customer form
#
#             # Create and bind the OrderForm
#             formOrder = OrderForm(request.POST)
#             if formOrder.is_valid():
#                 order = formOrder.save(commit=False)
#                 order.customer = customer
#                 order.save()  # Save the order with the customer linked
#
#                 # Handling the products in the order from cookies
#                 orders_list = request.COOKIES.get('orders', '{}')
#                 try:
#                     orders_dict = json.loads(orders_list)
#                 except json.JSONDecodeError:
#                     return HttpResponseBadRequest("Invalid orders cookie format")
#
#                 # Save each product in the order
#                 for key, value in orders_dict.items():
#                     product = get_object_or_404(Product, pk=int(key))
#                     count = value
#                     OrderProduct.objects.create(
#                         count=count,
#                         price=product.price,
#                         product=product,
#                         order=order
#                     )
#
#                 return redirect('index')
#             else:
#                 print(formOrder.errors)
#         else:
#             print(form.errors)
#
#     # If not POST, prepare the context for the order form
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     orders = []
#     orders_list = request.COOKIES.get('orders', '{}')
#     total_price = request.COOKIES.get('total_price', 0)
#
#     try:
#         orders_dict = json.loads(orders_list)
#     except json.JSONDecodeError:
#         orders_dict = {}
#
#     for key, value in orders_dict.items():
#         product = get_object_or_404(Product, pk=int(key))
#         orders.append({
#             'product': product,
#             'count': value
#         })
#
#     ctx = {
#         'categories': categories,
#         'products': products,
#         'orders': orders,
#         'total_price': total_price,
#         'MEDIA_ROOT': MEDIA_ROOT
#     }
#     return render(request, 'food/order.html', ctx)

def main_order(request):
    model = Customer()
    if request.POST:
        try:
            model = Customer.objects.get('phone_number', "")
        except:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order())
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                print("order :", order)
                orders_list = request.COOKIES.get('orders')

                for key, value in json.loads(orders_list).items():
                    product = get_product_by_id(product_id=int(key))
                    count = value
                    order_product = OrderProduct(
                        count=count,
                        price=product['price'],
                        product_id=product['id'],
                        order_id=order.id
                    )
                    order_product.save()
                return redirect('index')
            else:
                print(formOrder.errors)
        else:
            print(form.errors)
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get('orders')
    total_price = request.COOKIES.get('total_price')
    if orders_list:
        for key, value in json.loads(orders_list).items():
            orders.append({
                'products': Product.objects.get(pk=int(key)),
                'count': value
            })
    ctx = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }
    return render(request, 'food/order.html', ctx)








