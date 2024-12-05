from django.urls import path                                                         #type:ignore
from . import views

urlpatterns = [
    path('biz-barada/', views.about_us, name='biz-barada'),
    path('kontaktlarymyz/', views.contacts, name='kontaktlarymyz'),
]