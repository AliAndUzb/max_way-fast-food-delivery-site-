from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from food.models import *
from django.contrib.auth.decorators import login_required
from .services import *
from .forms import *
from django.contrib import messages




def login_required_decorator(func):
    return login_required(func, "login_page")


def login_page(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    categories_products = []
    table_list = get_table()
    for category in categories:
        categories_products.append(
            {
            'category': category.title,
            'product': len(Product.objects.filter(category_id=category.id))
             }
        )
    ctx = {
        'counts': {
            'categories': len(categories),
            'products': len(products),
            'orders': len(orders),
            'customers': len(customers),
        },
        'categories_products': categories_products,
        'table_list': table_list,
    }
    return render(request, 'dashboard/index.html', ctx)

@login_required_decorator
def product_list(request):
    products = Product.objects.all()
    ctx = {
        'products': products
    }
    return render(request, 'dashboard/product/list.html', ctx)


@login_required_decorator
def product_create(request):
    model = Product()
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('product_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_edit(request, pk):
    model = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        return redirect('product_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_delete(request, pk):
    model = get_object_or_404(Product, pk=pk)
    model.delete()
    messages.success(request, 'Product successfully deleted!')
    return redirect('product_list')


@login_required_decorator
def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories
    }
    return render(request, 'dashboard/category/list.html', ctx)


@login_required_decorator
def category_create(request):
    model = Category()
    form = CategoryForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_edit(request, pk):
    model = get_object_or_404(Category,pk=pk)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_delete(request, pk):
    model = get_object_or_404(Category, pk=pk)
    model.delete()
    messages.success(request, 'Category successfully deleted!')
    return redirect('category_list')


@login_required_decorator
def user_list(request):
    users = Customer.objects.all()
    ctx = {
        'users': users
    }
    return render(request, 'dashboard/user/list.html', ctx)


@login_required_decorator
def user_create(request):
    model = Customer()
    form = UserForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/user/form.html', ctx)


@login_required_decorator
def user_edit(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    form = UserForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/user/form_list', ctx)


@login_required_decorator
def user_delete(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    model.delete()
    messages.success(request, 'User successfully deleted!')
    return redirect('user_list')


@login_required_decorator
def order_list(request):
    orders = Order.objects.all()
    ctx = {
        'orders': orders
    }
    return render(request, 'dashboard/order/list.html', ctx)


@login_required_decorator
def customer_order_list(request, id):
    customer_orders = get_order_by_user(id=id)
    ctx = {
        'customer_orders': customer_orders
    }
    return render(request, 'dashboard/customer_order/list.html', ctx)


@login_required_decorator
def order_product_list(request, id):
    product_orders = get_product_by_order(id=id)
    ctx = {
        'product_orders': product_orders
    }
    return render(request, 'dashboard/productorder/list.html', ctx)













