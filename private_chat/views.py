from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Private_Message
from accounts.models import Profile


@login_required(login_url='/accounts/login/')
def dialogs(request):
    users = User.objects.exclude(id=get_user(request).id)
    return render(request, 'private_chat/index.html', {'users': users})


@login_required(login_url='/accounts/login/')
def room(request, room_name):
    users = room_name.split('-')
    messages = Private_Message.objects.filter(interlocutors__id__exact=users[0]).filter(
        interlocutors__id__exact=users[1])
    opponent = users[1] if int(users[0]) == get_user(request).id else users[0]
    profile_author = Profile.objects.filter(id=get_user(request).id).first()
    profile_opponent = Profile.objects.filter(id=opponent).first()
    return render(request, 'private_chat/room.html', {
        'room_name': room_name, 'private_messages': messages, 'opponent': opponent,
        'profile_author': profile_author, 'profile_opponent': profile_opponent
        })
