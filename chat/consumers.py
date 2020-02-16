from asgiref.sync import async_to_sync
from channels.auth import login
from channels.generic.websocket import WebsocketConsumer
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict

from bot.bot import error_bot_response
from chat.models import ChatRoom
from utils.database_functions import create_message
from utils.utils import get_date_with_template_format


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
        message_object = create_message(message, self.room, self.user)
        if message_object is not None:
            # Prepare message
            message_dict = model_to_dict(message_object)
            message_dict['user_to_show'] = message_object.user_to_show
            message_dict['creation_date'] = get_date_with_template_format(message_object.creation_date)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_dict
                }
            )
        else:
            # When the message has no the correct format
            self.send(text_data=json.dumps(error_bot_response()))


    # Receive message from room group
    def chat_message(self, event):
        self.send(text_data=json.dumps(event['message']))
