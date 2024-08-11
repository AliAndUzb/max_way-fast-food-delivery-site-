from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cost = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Customer(models.Model):
    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    e_mail = models.EmailField(null=True, blank=True, unique=True, help_text='Enter your e-mail', verbose_name='e_mail')
    region = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    payment_type = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=True, default=1)
    address = models.CharField(null=False, blank=False, max_length=250)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(null=False, blank=False)
    count = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)



