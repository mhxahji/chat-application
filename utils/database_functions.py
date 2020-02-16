from chat.models import ChatRoom, ChatMessage


def create_room(name):
    room, _ = ChatRoom.objects.get_or_create(name=name)
    return room


def create_message(message, room, user):

    message = ChatMessage.objects.create(room=room, user=user, message=message)
    return message
