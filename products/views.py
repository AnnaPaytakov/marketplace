from django.shortcuts import render, redirect                                                                                       #type:ignore
from .models import Product, Category, Favorite, Cart, CartItem
from .forms import ProductForm
from django.contrib.auth.decorators import login_required                                                                          #type:ignore
from django.contrib import messages                                                                                                #type:ignore
from django.http import JsonResponse   # для отправки данных в формате JSON в ответ на HTTP-запрос                                                                                                                                     #type:ignore
from django.db.models import Q         # используется для создания сложных запросов                                                                                                #type:ignore
import json


# Create your views here.
def products(request):
    q_name = request.GET.get('q_name', '')
    q_category = request.GET.get('q_category', '')

    all_products = Product.objects.all()
    
    # if q_name:
    #     all_products = all_products.filter(product_name__icontains=q_name)
    # if q_category:
    #     all_products = all_products.filter(category__name__icontains=q_category)
    if q_name or q_category:
        all_products = all_products.filter(Q(product_name__icontains=q_name), Q(category__name__icontains=q_category))

    categories = Category.objects.all()

    # Проверяем, является ли запрос AJAX-запросом (проверяем заголовок X-Requested-With)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Преобразуем QuerySet all_products в список с вложенными словарями, содержащих указанные поля
        products_list = list(all_products.values('id', 'product_name', 'product_image', 'price', 'description', 
                                                'stock_quantity', 'category__name', 'seller__id', 'seller__firstname', 
                                                'seller__lastname'))
        return JsonResponse({'products': products_list})# Возвращаем список продуктов в формате JSON

    context = {
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    status = False
    if request.user.is_authenticated:
        status = Favorite.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product' : product,
        'status':status
    }
    return render(request, 'products/product.html', context)

@login_required 
def add_to_favorites(request, pk):
    product = Product.objects.get(id=pk)  # Получаем продукт из базы данных по (id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)  
    # Ищем объект "Favorite" для текущего пользователя и продукта. Если не существует, создаем его

    if not created:  # Если объект уже существует (created=False), значит продукт уже в избранном
        favorite.delete()  # Удаляем продукт из избранного
        return JsonResponse({'added': False})  # Возвращаем ответ, что продукт был удален из избранного

    return JsonResponse({'added': True})  # Если объект был создан возвращаем True


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites': favorites
    }
    return render(request, 'products/favorites.html', context)

@login_required  # Декоратор, проверяющий, что пользователь аутентифицирован.
def add_to_cart(request):  # Определяем функцию для добавления товара в корзину.
    if request.method == 'POST':  # Проверяем, что запрос сделан методом POST.
        data = json.loads(request.body)  # Загружаем данные запроса из JSON-формата в объект Python.
        pk = data.get('product_id')  # Получаем идентификатор продукта из данных запроса.
        product = Product.objects.get(id=pk)  # Извлекаем объект продукта из базы данных по его идентификатору.

        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)  
        # Извлекаем (или создаем, если не существует) корзину, связанную с текущим пользователем, которая активна.

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  
        # Извлекаем (или создаем, если не существует) товар корзины для этого продукта в текущей корзине.

        if cart_item.quantity < product.stock_quantity:  # Проверяем, меньше ли количество товара чем на складе.
            cart_item.quantity += 1  # Увеличиваем количество товара на 1.
            cart_item.save()  # Сохраняем изменения в базе данных.
            context = {
                'quantity': cart_item.quantity,  # Количество товара в корзине.
                'status': 'success'  # Статус ответа: успешно.
            }
        else:  # Если количество товара в корзине достигло количества на складе.
            context = {
                'quantity': cart_item.quantity,  # Количество товара в корзине.
                'status': 'error',  # Статус ответа: ошибка.
                'message': 'Haryt limitly'  # Сообщение об ошибке: превышен лимит товара на складе.
            }
        return JsonResponse(context)  # Возвращаем ответ в формате JSON с данными о количестве и статусом.

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)  
    # Если запрос не является POST, возвращаем ответ об ошибке в формате JSON с кодом 400.


@login_required  # Декоратор, проверяющий, что пользователь аутентифицирован.
def subtract_from_cart(request):  # Определяем функцию для уменьшения количества товара в корзине.
    if request.method == 'POST':  # Проверяем, что запрос сделан методом POST.
        data = json.loads(request.body)  # Загружаем данные запроса из JSON-формата в объект Python.
        pk = data.get('product_id')  # Получаем идентификатор продукта из данных запроса.
        product = Product.objects.get(id=pk)  # Извлекаем объект продукта из базы данных по его идентификатору.

        try:
            cart = Cart.objects.get(user=request.user, is_active=True)  # Получаем корзину, связанную с пользователем, которая активна.
            cart_item = CartItem.objects.get(cart=cart, product=product)  # Получаем товар корзины для указанного продукта.

            if cart_item.quantity > 0:  # Проверяем, больше ли нуля количество товара в корзине.
                cart_item.quantity -= 1  # Уменьшаем количество товара на 1.
                if cart_item.quantity == 0:  # Если количество товара становится равным нулю.
                    cart_item.delete()  # Удаляем товар из корзины.
                    context = {'quantity': 0, 'status': 'success'}  # Устанавливаем количество 0 и статус "успешно".
                else:
                    cart_item.save()  # Сохраняем изменения в базе данных.
                    context = {'quantity': cart_item.quantity, 'status': 'success'}  # Возвращаем новое количество и статус "успешно".
            else:
                context = {'quantity': 0, 'status': 'success'}  # Если количество товара уже 0, возвращаем нулевое количество и статус "успешно".
        except CartItem.DoesNotExist:  # Если товар не найден в корзине.
            context = {'quantity': 0, 'status': 'error', 'message': 'Goshulan haryt yok'}  # Возвращаем ошибку, что товар отсутствует в корзине.

        return JsonResponse(context)  # Возвращаем ответ в формате JSON с данными о количестве и статусе.

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)  
    # Если запрос не является POST, возвращаем ответ об ошибке в формате JSON с кодом 400.


@login_required
def cart_items(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'products/cart-items.html', context)


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pk = data.get('product_id')
        product = Product.objects.get(id=pk)

        cart = Cart.objects.get(user=request.user, is_active=True)
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete() 
            context = {'status': 'success'}
        except CartItem.DoesNotExist:
            context = {'status': 'error', 'message': 'Haryt sebetde tapylmady'}

        return JsonResponse(context)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            haryt = form.save(commit=False)
            haryt.seller = request.user.profile
            haryt.save()
            return redirect('account')
        else:
            messages.error(request, 'Formany dogry doldurmagynyz gerek')

    context = {
        'form':form,
    }
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form':form,
    }
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('account')

    context = {
        'product':product,
    }
    return render(request, 'products/delete-form.html', context)