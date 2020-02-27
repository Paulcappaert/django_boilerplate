from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import GameForm
from core.models import User
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.start_game(request.user)
            return redirect('join-game', game.code)
    else:
        form = GameForm()
    
    return render(request, 'game/create.html', {'form': form})

@require_GET
def join_game(request, game_code):
    game = Game.objects.get(code=game_code)
    if request.user.id == game.p1.id:
        color = 'w'
    elif request.user.id == game.p2.id:
        color = 'b'
    else:
        color = ''

    if game.start_timer():
        if color == 'b':
            time = 100 - (game.p2_last - game.started).seconds
            opTime = 100 - (game.p1_last - game.started).seconds
        else:
            time = 100 - (game.p2_last - game.started).seconds
            opTime = 100 - (game.p1_last - game.started).seconds
    else:
        time = 0
        opTime = 0

    if color == 'w' and game.move_index % 2 == 0:
        your_turn = True
    else:
        your_turn = False
    
    return render(request, 'game/game.html', {
        'color': color,
        'fen': game.fen,
        'group_name': game_code,
        'time': time,
        'opTime': opTime,
        'your_turn': your_turn
    })

@csrf_exempt
@require_POST
@login_required
def make_move(request, game_code):
    user = request.user
    game = get_object_or_404(Game, code=game_code)
    source = request.POST['source']
    target = request.POST['target']
    if game.can_move(user):
        game.make_move(source, target)
        data = {'success': True}
    else:
        data = {'success': False}
    
    return JsonResponse(data)