from django.contrib.auth.models import User                                                                 #type:ignore
from .models import Profile

# Импортируем сигнал post_save из django.db.models.signals    
from django.db.models.signals import post_save, post_delete                                                         #type:ignore

# Определяем функцию-обработчик сигнала post_save
def new_user_created(sender, instance, created, **kwargs):
    # Проверяем, был ли создан новый объект (создан ли новый пользователь)
    if created:
        taze_user = instance  # Присваиваем вновь созданного пользователя переменной taze_user
        # Создаём профиль для нового пользователя
        Profile.objects.create(
            user=taze_user,  # Устанавливаем связь профиля с пользователем
            phone=taze_user.username,  # Присваиваем номер телефона из username пользователя полю phone
            firstname = taze_user.first_name,
            lastname = taze_user.last_name,
        )
    else:
        try:
            profile=Profile.objects.get(user=instance)
            profile.phone = instance.username
            profile.save()
        except:
            pass

# Подключаем функцию new_user_created к сигналу post_save для модели User
post_save.connect(new_user_created, sender=User)

# Определяем функцию-обработчик сигнала post_delete
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user  # Получаем объект пользователя, связанный с экземпляром профиля
        user.delete()  # Удаляем объект пользователя из базы данных
    except:
        pass

# Подключаем функцию deleteUser к сигналу post_delete для модели Profile
post_delete.connect(deleteUser, sender=Profile)  