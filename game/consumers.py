from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Game

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
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def game_move(self, event):
        move = event['move']
        await self.send(text_data=move)
