from django.contrib.auth.models import User
from django.test import TestCase

from bot.bot import error_bot_response, get_name_code_from_message
from utils.constants import BOT_NAME, USER_ERROR_COMMAND, MESSAGE_ERROR_COMMAND, STOCK_CODE
from utils.database_functions import create_message, create_room
from .models import ChatRoom, ChatMessage


class ChatRoomTestCase(TestCase):

    def setUp(self):
        self.room = ChatRoom.objects.create(name="chat 1")
        self.user = User.objects.create(username="user 1", password='asbckjasn')

    def test_user_show_name(self):
        """Getting the complete name when user has first and last name, only first when not last and
         only username when no first neither last"""
        user_obj = User.objects.create(username="user test", password='asbckjasn', first_name='first',
                                       last_name='last')
        user_2_obj = User.objects.create(username="user test 2", password='asbckjasn', first_name='first')
        self.assertEquals(user_obj.show_name, 'first last')
        self.assertEquals(user_2_obj.show_name, 'first ')
        self.assertEquals(self.user.show_name, 'user 1')

    def test_creating_one_and_then_get_the_same_room(self):
        """Same name of room is not creating again"""
        obj_1 = create_room("new room")
        obj_2 = create_room("new room")
        self.assertEqual(obj_1.id, obj_2.id)

    def test_creating_one_message(self):
        """Message in room is counted"""
        create_message("first message", self.room, self.user)
        self.assertEqual(self.room.count_messages, 1)

    def test_return_the_last_50_messages(self):
        """Get the last 50 Messages from room """
        for i in range(100):
            ChatMessage.objects.create(message="message " + str(i), room=self.room,
                                                      user=self.user)
        last_50_messages = list(self.room.messages_last_50)
        self.assertEquals(len(last_50_messages), 50)

    def test_create_bot_message(self):
        """Creating bot message"""
        message_command = "/stock=ajjds"
        message_obj = create_message(message_command, self.room, self.user)
        self.assertEquals(message_obj.bot_message, True)
        self.assertEquals(message_obj.user_to_show, BOT_NAME)
        self.assertEquals(get_name_code_from_message(message_command), STOCK_CODE['name'])

    def test_show_user_from_normal_message(self):
        """Creating bot message"""
        message_obj = create_message("normal message", self.room, self.user)
        self.assertEquals(message_obj.bot_message, False)
        self.assertEquals(message_obj.user_to_show, self.user.show_name)

    def test_try_to_create_bot_message_with_incorrect_command_format(self):
        """Sending incorrect format for creating bot message"""
        message_command = "/stock=ajjds sjhds"
        message_obj = create_message(message_command, self.room, self.user)
        self.assertEquals(message_obj, None)

    def test_error_message_with_incorrect_command_format(self):
        """Seeing the message error when incorrect command format"""
        message = error_bot_response()
        self.assertEquals(message['user_to_show'], USER_ERROR_COMMAND)
        self.assertEquals(message['message'], MESSAGE_ERROR_COMMAND)
