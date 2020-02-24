from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_game, name='create-game'),
    path('join/<str:game_code>', views.join_game, name='join-game'),
    path('move/<str:game_code>', views.make_move, name='make-move'),
]