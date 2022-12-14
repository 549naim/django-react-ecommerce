from itertools import product
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    prouser=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile/',blank=True,null=True)
    def __str__(self):
        return self.prouser.username

class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(upload_to='product/',blank=True,null=True)
    mar_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.title       

class Cart(models.Model):
    customer=models.ForeignKey(Profile,on_delete=models.CASCADE) 
    total=models.PositiveIntegerField()
    complete_status=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ManyToManyField(Product)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()
    def __str__(self):
        return f"Cart=={self.cart.id}==CartProduct=={self.id}==Quantity=={self.quantity}"            

ORDER_STATUS = {
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('Order On the way', 'Order On the way'),
    ('Order Completed', 'Order Completed'),
    ('Order Canceled', 'Order Canceled'),
}

class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    address=models.CharField(max_length=500)
    email=models.EmailField(max_length=254)
    total=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    orderStatus=models.CharField(max_length=100,choices=ORDER_STATUS,default='Order Received') 
    date=models.DateTimeField(auto_now_add=True)
    paymentStatus=models.BooleanField(default=False)    