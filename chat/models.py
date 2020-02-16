# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from utils.additional_user_properties import props_to_user
from django.contrib.auth.models import User
import datetime

from utils.constants import BOT_NAME


class ChatRoom(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('name'))
    creation_date = models.DateField(default=datetime.date.today, verbose_name=_('creation date'))

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    @property
    def count_messages(self):
        return self.messages.count()

    class Meta:
        ordering = ('name',)
        verbose_name = _('Chat Room')
        verbose_name_plural = _('Chat Rooms')


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE,
                             verbose_name=_('chat room'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('user'))
    message = models.TextField(verbose_name=_('message'))
    creation_date = models.DateTimeField(default=timezone.now, verbose_name=_('creation date'))
    bot_message = models.BooleanField(default=False, verbose_name=_('bot message'))

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.message

    @property
    def user_to_show(self):
        if self.bot_message:
            return BOT_NAME
        else:
            return self.user.show_name

    class Meta:
        ordering = ('creation_date',)
        verbose_name = _('Chat Room')
        verbose_name_plural = _('Chat Rooms')


props_to_user()
