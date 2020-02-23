from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_game, name='create-game'),
    path('<str:game_code>', views.join_game, name='join-game'),
]