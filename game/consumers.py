from channels.generic.websocket import AsyncWebsocketConsumer

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

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']  
        self.group_name = f'user_{self.username}'
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
    async def notification(self, event):
        message = event['message']
        await self.send(text_data=message)