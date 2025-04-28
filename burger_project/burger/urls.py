
from django.urls import path

from . import views
from .views import index, quiz, register, custom_login  # Используем index вместо home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),  # Главная страница
    path('quiz/', quiz, name='quiz'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chat/', views.chat, name='chat'),
]
