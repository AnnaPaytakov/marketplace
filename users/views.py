from django.shortcuts import render, redirect                                                                                             #type:ignore
from django.contrib.auth.models import User                                                                                              #type:ignore
from django.contrib.auth import login, authenticate, logout                                                                                #type:ignore
from django.contrib import messages                                                                                                       #type:ignore                                                                                        # type:ignore
from .models import Profile, ProfileVisit  
from products.models import Product                                 
from .forms import CustomRegisterForm, AccountForm, AccountFormAlyjy
from django.contrib.auth.decorators import login_required                                                                               #type:ignore
from django.utils import timezone                                                                               #type:ignore
from datetime import timedelta                                                                                  #type:ignore

def track_profile_visit(profile, visitor):
    # Получаем текущее время
    current_time = timezone.now()

    # Создаем объект времени начала сегодняшнего дня (00:00:00.000000)
    today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Проверяем, посещал ли посетитель этот профиль сегодня
    visit_today = ProfileVisit.objects.filter(
        visitor=visitor,               # Фильтруем по посетителю
        profile=profile,               # Фильтруем по профилю
        visited_at__gte=today_start    # Фильтруем по времени посещения начиная с начала сегодняшнего дня
    ).exists()
    
    if not visit_today:
        # Если посещений сегодня нет, увеличиваем счетчик посещений профиля
        profile.profile_visit += 1
        profile.save()
        
        # Создаем новую запись о посещении
        ProfileVisit.objects.create(visitor=visitor, profile=profile)

# Create your views here.
def profile(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.user.is_authenticated:
        if request.user.profile == profile:
            return redirect('account')

    all_products = Product.objects.filter(seller=profile)

    if request.user.is_authenticated:
        track_profile_visit(profile, request.user)

    context = {
        'profile':profile,
        'all_products':all_products,
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    all_products = Product.objects.filter(seller=profile)

    context = {
        'profile': profile,
        'all_products': all_products,
    }  
    
    return render(request, 'users/account.html', context)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('products')

    if request.method == "POST":  # Если метод запроса равен "POST"
        username = request.POST['phone']  # Получаем значение телефона из POST данных и сохраняем его в переменной username
        password = request.POST['password']  # Получаем значение пароля из POST данных и сохраняем его в переменной password

        try:
            user = User.objects.get(username=username)  # Пытаемся найти пользователя в базе данных по username
        except:
            messages.error(request, "Bular yaly ulanyjy yok")  # Если пользователь не найден, выводим сообщение, что такого пользователя нет

        user = authenticate(username=username, password=password)  # Аутентифицируем пользователя с полученными username и password

        if user:  # Если аутентификация прошла успешно и пользователь существует
            login(request, user)  # Выполняем вход пользователя в систему
            return redirect('products')  # Перенаправляем пользователя на страницу с продуктами
        else:
            messages.error(request, "Parolynyzy yalnysh girizdiniz")  # Если аутентификация не удалась, выводим сообщение об ошибке пароля

    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = CustomRegisterForm()
    
    if request.method == 'POST':  # Проверяем, является ли текущий запрос POST-запросом
        form = CustomRegisterForm(request.POST)  # Пересоздаем форму передавая в неё данные из POST-запроса
        if form.is_valid():  # Проверяем, прошла ли форма валидацию (все поля заполнены корректно)
            user = form.save(commit=False)  # Сохраняем данные формы в объект user, но не сохраняем его в базу
            user.save()  # Сохраняем объект user в базу данных
            
            profile = user.profile
            user_role = form.cleaned_data.get('user_role')  # Получаем выбранную роль пользователя из формы
            profile.user_role=user_role  # профилю присваиваем его роль
            profile.save()

            login(request, user)  # Выполняем вход для только что созданного пользователя
            return redirect('products')  # Перенаправляем пользователя на главную страницу 'products'


    context = {
       'form':form, 
    }
    return render(request, 'users/register.html', context)

def edit_account(request, pk):  # Определяем функцию edit_account, которая принимает запрос и первичный ключ
    account = Profile.objects.get(id=pk)  # Получаем экземпляр Profile по его первичному ключу (id)
    if account.user_role == 'Satyjy':
        form = AccountForm(instance=account)  # Инициализируем форму AccountForm, используя данные текущего аккаунта
    else:
        form = AccountFormAlyjy(instance=account)

    if request.method == 'POST':  # Проверяем, был ли запрос методом POST (пользователь отправил данные формы)
        
        if account.user_role == 'Satyjy':
            form = AccountForm(request.POST, request.FILES, instance=account)  # Переинициализируем форму с данными из запроса POST и файлами
        else:
            form = AccountFormAlyjy(request.POST, request.FILES, instance=account)

        if form.is_valid():  # Проверяем, является ли форма действительной (без ошибок)
            account = form.save(commit=False)  # Сохраняем форму без сохранения изменений в базе данных сразу

            if account.user.username != request.POST['phone']:  # Проверяем, изменился ли номер телефона пользователя
                account.user.username = request.POST['phone']  # Обновляем имя пользователя на новое значение телефона
                account.user.save()  # Сохраняем изменения в модели User
                print('Ulanyjy telefonyny chalshdy')  # Выводим сообщение в консоль (можно заменить на функцию отправки SMS)

            account.save()  # Сохраняем изменения в модели Profile
            return redirect('account')  # Перенаправляем пользователя на страницу 'account'
        else:
            messages.error(request, 'Formany dogry doldurmagynyzy gerek')  # Отображаем сообщение об ошибке, если форма недействительна


    context = {
        'form': form,  # Передаем форму (с данными ) в шаблон для отображения
    }
    return render(request, 'users/account-form.html', context)  # Рендерим шаблон