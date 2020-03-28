from celery.schedules import crontab
from celery.task import periodic_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@periodic_task(run_every=(crontab(minute='*')), name="update_to_visitor", ignore_result=False)
def update_to_visitor():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_paul', {'type': 'notification', 'message': json.dumps({'game_code': 'tick'})}
    )