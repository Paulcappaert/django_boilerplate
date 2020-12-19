from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.username = self.scope['user'].username
        else:
            self.username = 'anonymous'

        await self.channel_layer.group_add(
            'chat',
            self.channel_name
        )

        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'message': self.username + ' connected'
                }),
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'message': self.username + ' disconnected'
                }),
            }
        )

        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        json_data['message'] = self.username + ': ' + json_data['message']
        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': json.dumps(json_data),
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=message)
