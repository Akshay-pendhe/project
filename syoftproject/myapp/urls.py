from .views import register, login, create_product,get_product,update_product,delete_product
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('create_product/', create_product, name='create_product'),
    path('get_product/', get_product, name='get_product'),
    path('update_product/', update_product, name='update_product'),
    path('delete_product/', delete_product, name='delete_product'),
    
]