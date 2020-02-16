from bot.bot import is_bot_message, process_bot_message
from chat.models import ChatRoom, ChatMessage


def create_room(name):
    room, _ = ChatRoom.objects.get_or_create(name=name)
    return room


def create_message(message, room, user):
    if message.startswith('/'):
        if is_bot_message(message):
            code_bot, new_message = process_bot_message(message)
            message = ChatMessage.objects.create(room=room, user=user, message=new_message, bot_message=True)
        else:
            return None
    else:
        message = ChatMessage.objects.create(room=room, user=user, message=message)
    return message
