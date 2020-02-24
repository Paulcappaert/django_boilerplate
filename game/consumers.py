from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.auth import get_user
from .models import Game
from channels.db import database_sync_to_async
from django.db import close_old_connections

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game']     
        self.group_name = f'chess_{self.game_code}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        close_old_connections()
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        source = text_data_json['source']
        target = text_data_json['target']

        if await self.make_move(source, target):
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'game_move',
                    'move': json.dumps({
                        'source': source,
                        'target': target,
                    })
                }
            )

    # Receive message from room group
    async def game_move(self, event):
        move = event['move']
        await self.send(text_data=move)

    @database_sync_to_async
    def make_move(self, source, target):
        close_old_connections()
        game = Game.objects.get(code=self.game_code)
        user = self.scope['user']
        if game.can_move(user):
            game.make_move(source, target)
            return True
        else:
            return False
