from django.db import models                                                                                      #type:ignore
from decimal import Decimal
import uuid
from users.models import Profile
from django.contrib.auth.models import User                                                                  #type:ignore


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          unique=True, editable=False)
    
    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True )
    product_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True, default='default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default = 0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # taze pole
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          unique=True, editable=False)
    
    def __str__(self):
        return self.product_name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"
    
    def get_total_price(self):
        total = 0  # Начинаем с общей суммы, равной 0
        for item in self.cartitem_set.all():  # Проходим по всем товарам в корзине
            total += item.get_total_price()  # Добавляем к общей сумме цену каждого товара
        return total  # Возвращаем общую сумму всех товаров в корзине


class CartItem(models.Model):  
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=0) 
   
    class Meta:  
        unique_together = ('cart', 'product')  
        # Задает ограничение, которое не позволяет добавлять один и тот же продукт в одну корзину более одного раза

    def __str__(self): 
        return f"{self.quantity} x {self.product.product_name} in Cart {self.cart.id}"  
        # Возвращает строку, например: "2 x Ноутбук в Корзине 1".

    def get_total_price(self):  
        # Метод для вычисления общей стоимости товара в корзине (цена продукта умноженная на его количество).
        return self.quantity * self.product.price  
        # Возвращает общую стоимость товара на основе количества и цены продукта.


