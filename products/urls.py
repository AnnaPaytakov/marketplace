from django.urls import path                                                                   #type:ignore
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product/<str:pk>/', views.product, name='product'),
    path('add-product/', views.add_product, name='add-product'),
    path('update-product/<str:pk>/', views.update_product, name='update-product'),
    path('delete-product/<str:pk>/', views.delete_product, name='delete-product'),
    path('add_to_favorites/<str:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('user-favorites/', views.favorites_list, name='user-favorites'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('subtract-from-cart/', views.subtract_from_cart, name='subtract_from_cart'),
    path('cart/', views.cart_items, name='cart-items'),
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
]