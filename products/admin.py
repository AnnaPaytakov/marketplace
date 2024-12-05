from django.contrib import admin                                                                                #type:ignore
from .models import Product, Category, Favorite, Cart, CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(CartItem)
