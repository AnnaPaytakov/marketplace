from django.contrib.auth.models import User                                                                                                     #type:ignore Импортируем модель User из встроенной системы аутентификации Django
from django.contrib.auth.forms import UserCreationForm                                                                                           #type:ignore                                             

from django import forms                                                                                                                        #type:ignore
from .models import Profile  
from django.forms import ModelForm                                                                                                               #type:ignore
from django.forms.widgets import ClearableFileInput                                                                                              #type:ignore
from django.utils.translation import gettext_lazy as _  # для перевода текстов в приложении на разные языки                                      #type:ignore

class CustomClearableFileInput(ClearableFileInput):  # Пользовательский виджет, наследующий от ClearableFileInput, чтобы изменить текстовые метки.
    initial_text = _('Shu wagtky suratynyz')  # Настраиваем текст "Currently" для отображения текущего изображения.
    input_text = _('Chalshmak')  # Настраиваем текст "Change" для отображения кнопки выбора файла.
    clear_checkbox_label = _('Pozmak')  # Настраиваем текст "Clear" для отображения флажка удаления изображения.

class AccountForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone', 'firstname', 'lastname', 'profile_image', 
            'email', 'bio', 'address', 'start_time', 'finish_time'
        ]
        widgets = {
            'profile_image': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'finish_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['placeholder'] = '+993...'
        self.fields['firstname'].widget.attrs['placeholder'] = 'Adyňyz'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Familýaňyz'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['bio'].widget.attrs['placeholder'] = 'Barada'
        self.fields['address'].widget.attrs['placeholder'] = 'Adresyňyz'
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control-file'
        })

class AccountFormAlyjy(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone', 'firstname', 'lastname', 'profile_image', 
            'email', 'address', 
        ]
        widgets = {
            'profile_image': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AccountFormAlyjy, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['placeholder'] = '+993...'
        self.fields['firstname'].widget.attrs['placeholder'] = 'Adyňyz'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Familýaňyz'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['address'].widget.attrs['placeholder'] = 'Adresyňyz'
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control-file'
        })

# Создаем пользовательскую форму для регистрации, наследуя встроенную форму UserCreationForm
class CustomRegisterForm(UserCreationForm):

    USER_ROLE_TYPE = (
        ('Satyjy', 'Satyjy'),
        ('Alyjy', 'Alyjy'),
    )

    user_role = forms.ChoiceField(choices=USER_ROLE_TYPE)

    # Вложенный класс Meta используется для указания метаданных для формы
    class Meta:
        model = User  # Указываем модель, для которой создается форма (модель User)

        # Указываем поля, которые будут отображаться в форме
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'user_role']  

        # # Определяем пользовательские метки (labels) для полей формы
        # labels = {  
        #     'username': 'Telefon belgiňiz',  # Устанавливаем метку для поля username
        #     'first_name': 'Adyňyz',  # Устанавливаем метку для поля first_name
        #     'last_name': 'Familýaňyz',  # Устанавливаем метку для поля last_name
        # }

    # Переопределяем метод инициализации для добавления дополнительных настроек
    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)  # Вызываем инициализацию родительского класса
        self.fields['password1'].label = 'Parol'  # Устанавливаем пользовательскую метку для поля password1
        self.fields['password2'].label = 'Paroly gaýtalaň'  # Устанавливаем пользовательскую метку для поля password2

        self.fields['username'].widget.attrs['placeholder'] = '+993...'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Adyňyz'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Familýaňyz'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parol'
        self.fields['password2'].widget.attrs['placeholder'] = 'Paroly gaýtalaň'
        



