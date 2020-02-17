from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from chat.models import ChatRoom
from utils.database_functions import create_message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = ChatRoom.objects.get(pk=self.room_id)
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        created, message_dict = create_message(message, self.room, self.user)
        if created:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_dict
                }
            )
        else:
            # When the message has no the correct format or has empty response
            self.send(text_data=json.dumps(message_dict))


    # Receive message from room group
    def chat_message(self, event):
        self.send(text_data=json.dumps(event['message']))
