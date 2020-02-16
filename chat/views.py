# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from chat.models import ChatRoom
from utils.database_functions import create_room


@login_required
def index(request):
    room_name = request.GET.get('new')
    if room_name:
        new_room = create_room(room_name)
        return redirect('room', room_id=new_room.id)
    return render(request, 'chat/index.html', {'rooms': ChatRoom.objects.all()})


@login_required
def room(request, room_id):
    room_object = ChatRoom.objects.get(pk=room_id)
    return render(request, 'chat/room.html', {
        'room': room_object,
        'rooms': ChatRoom.objects.all()
    })
