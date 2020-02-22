from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Game

@login_required
def create_game(request):
    game = Game.objects.create(

    )
    

def spectate_game(request, game_code):
    game = Game.objects.get(code=game_code)

@login_required
def join_game(request, game_code):
    game = Game.objects.get(code=game_code)
    if request.user.id == game.p1.id:
        color = 'w'
    elif request.user.id == game.p2.id:
        color = 'b'
    else:
        return redirect('spectate', game_code)
    
    return render(request, 'game/game.html', {
        'color': color,
        'fen': game.fen,
        'group_name': game_code,
    })
