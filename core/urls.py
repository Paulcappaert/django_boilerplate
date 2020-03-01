from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='core/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('api/confirm/', views.confirm, name='confirm'),
    path('api/is-confirmed/', views.is_confirmed, name='is-confirmed'),
    path('api/chat/', views.receieve_chat, name='receive-chat'),
]