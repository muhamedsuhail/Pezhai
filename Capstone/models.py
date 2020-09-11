from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    total_cost = models.IntegerField(default=0) 
    shipping_address = models.CharField(max_length=1000)
    contact = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField()
    
    def __str__(self):
        return f"{self.user}-₹{self.total_cost}"

    def address_as_lines(self):
        return self.shipping_address.split(',')

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    cart_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}-₹{self.cart_total}"

class Product(models.Model):
    name = models.CharField(max_length=500)
    img_link = models.CharField(max_length=500)
    rating = models.IntegerField()
    price = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    shipping_price = models.CharField(max_length=100)
    total_cost = models.IntegerField()
    category = models.CharField(max_length=50)
    order = models.ManyToManyField(Order,blank=True,related_name="ordered_items",through="ordered_quantity")
    cart = models.ManyToManyField(Cart,blank=True,related_name="cart_items",through="cart_quantity")
    
    def __str__(self):
        return f"{self.id}-{self.name}"    

class cart_quantity(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item = models.OneToOneField(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.product_name} x {self.quantity}"

class ordered_quantity(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.product_name} x {self.quantity}"