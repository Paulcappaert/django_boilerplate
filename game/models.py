from django.db import models
from core.models import User
import secrets
import chess
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Move(models.Model):
    source = models.CharField(max_length=2)
    target = models.CharField(max_length=2)
    next_move = models.OneToOneField(
        'Move',
        on_delete=models.CASCADE,
        null=True,
        related_name='prev_move',
    )

class Game(models.Model):
    code = models.CharField(max_length=24, unique=True)
    p1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='p1_games',
    )
    p2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='p2_games',
    )
    fen = models.CharField(max_length=100)
    move_index = models.IntegerField()
    first_move = models.OneToOneField(
        Move, 
        on_delete=models.CASCADE, 
        related_name='first',
        null=True,
    )
    last_move = models.OneToOneField(
        Move,
        on_delete=models.CASCADE,
        related_name='last',
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_hex(12)
            self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            self.move_index = 0
        return super().save(*args, **kwargs)

    def can_move(self, user):
        p_number = self.move_index % 2
        if ((p_number == 0 and user.id == self.p1.id) or
            (p_number == 1 and user.id == self.p2.id)):
            return True
        return False

    def make_move(self, source, target):
        new_move = Move.objects.create(source=source, target=target)
        self.move_index += 1

        # update fen string here
        board = chess.Board(self.fen)
        move = chess.Move.from_uci(source + target)
        board.push(move)
        self.fen = board.fen()

        if self.first_move:
            self.last_move.next_move = new_move
            self.last_move.save()
            self.last_move = new_move
            self.save()
        else:
            self.first_move = new_move
            self.last_move = new_move
            self.save()

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        # f'chess_{self.code}', 
        # {
        #     "type": "game_move",
        #     'move': json.dumps({
        #         'source': source,
        #         'target': target,
        #     })
        # })