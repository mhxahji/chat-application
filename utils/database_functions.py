from django.forms import model_to_dict

from bot.bot import is_bot_message, process_bot_message, error_bot_response
from chat.models import ChatRoom, ChatMessage
from utils.utils import get_date_with_template_format


def create_room(name):
    room, _ = ChatRoom.objects.get_or_create(name=name)
    return room


def create_message(message, room, user):
    if message.startswith('/'):
        if is_bot_message(message):
            code_bot, new_message = process_bot_message(message)
            if isinstance(new_message, dict):
                return False, new_message
            message = ChatMessage.objects.create(room=room, user=user, message=new_message, bot_message=True)
        else:
            return False, error_bot_response()
    else:
        message = ChatMessage.objects.create(room=room, user=user, message=message)
    return True, prepare_model_dict(message)


def prepare_model_dict(message_object):
    message_dict = model_to_dict(message_object)
    message_dict['user_to_show'] = message_object.user_to_show
    message_dict['creation_date'] = get_date_with_template_format(message_object.creation_date)
    return message_dict
