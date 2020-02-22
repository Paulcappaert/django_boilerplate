from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user
from .models import Game

class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game']
        if Game.objects.filter(code=self.game_code).exists():      
            self.group_name = f'chess_{self.game_code}'
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        source = text_data_json['source']
        target = text_data_json['target']
        
        game = Game.objects.get(code=self.game_code)
        user = self.scope['user']

        if game.can_move(user):
            game.make_move(source, target)
            async_to_sync(self.channel_layer.group_send)(
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
    def game_move(self, event):
        move = event['move']

        # Send message to WebSocket
        self.send(text_data=move)