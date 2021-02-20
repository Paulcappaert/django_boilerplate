from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import redis


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
                    'user': self.username,
                    'message': ' connected',
                }),
            }
        )

        await self.accept()

        self.r = redis.Redis(host='localhost', port=6379, db=0)

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'user': self.username,
                    'message': ' disconnected',
                }),
            }
        )

        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        json_data['user'] = self.username
        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': json.dumps(json_data),
            }
        )

        self.r.publish('user_updates', json.dumps(json_data))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=message)
