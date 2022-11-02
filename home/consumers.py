# chat/consumers.py
import json
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask,IntervalSchedule
class StockConsumer(WebsocketConsumer):
    def add_to_celery_beat(self,stockpicker):
        task = PeriodicTask.objects.filter(name='every-10-seconds')
        if len(task) > 0:
            
            task = task.first()
            args = json.loads(task.args)
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps(args)
        else:
            schedule,created = IntervalSchedule.objects.get_or_create(every=10,period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule,name='every-10-seconds',task='home.tasks.update_stock',args=json.dumps(stockpicker))
        task.save()
        
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_track' 
        print('connected succesfully 1')
        print(self.room_group_name)
        print(self.room_name)
        
        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # parse_querystring
        print('connected succesfully 2')
        query_params = self.scope["query_string"].decode()
        query_params = query_params.split('+')[1:]
        #celery beat
        self.add_to_celery_beat(query_params)
        print('connected succesfully 3')
        self.accept()
        

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_stock_update',
                'message': message
            }
        )

    # Receive message from room group
    async def stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message':message}))
    
    
