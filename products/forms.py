from django.forms import ModelForm # Импортируем ModelForm из коробки джанго для создания формы                                                                                                             #type:ignore  # Импортируем класс ModelForm из модуля django.forms
from .models import Product  # Импортируем модель Product из текущего модуля

class ProductForm(ModelForm):  # Определяем класс ProductForm, который наследуется от ModelForm
    class Meta:  # Внутренний класс Meta для указания настроек формы
        model = Product  # Связываем форму с моделью Product
        fields = ['product_name', 'description', 'product_image', 'price', 'stock_quantity',
                  'category']  # Указываем поля модели, которые будут использоваться в форме
        
    def __init__(self, *args, **kwargs):  # Переопределяем метод __init__ для дополнительной настройки полей
        super(ProductForm, self).__init__(*args, **kwargs)  # Вызываем родительский метод __init__
        self.fields['product_name'].widget.attrs['placeholder']='Haryt ady'  # Добавляем placeholder для поля 'product_name'
        self.fields['description'].widget.attrs['placeholder']='Haryt barada'  # Добавляем placeholder для поля 'description'
        self.fields['price'].widget.attrs['placeholder']='Haryt bahasy'  # Добавляем placeholder для поля 'price'
        self.fields['stock_quantity'].widget.attrs['placeholder']='Haryt sany'  # Добавляем placeholder для поля 'stock_quantity'
        self.fields['category'].widget.attrs['placeholder']='Haryt kategoriyasy'  # Добавляем placeholder для поля 'category_name'
