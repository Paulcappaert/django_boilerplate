import redis
import time
import django
import os
import json
from asgiref.sync import async_to_sync

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()

pubsub.subscribe('user_updates')

count = 0

while True:
    message = pubsub.get_message()
    if message and message['type'] == 'message':
        count += 1
        data = json.loads(message['data'])
        print(data['message'])
        async_to_sync(channel_layer.group_send)(
            "chat", {"type": "chat_message", "message": json.dumps({
                "message": f"{count} messages",
                "user": "background"
            })})

    time.sleep(1)
