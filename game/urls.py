from django.urls import path
from . import views

urlpatterns = [
    path('<str:game_code>', views.join_game, name='join-game'),
]