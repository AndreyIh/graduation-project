import os
#import locale
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Private_Message
from .forms import MessageForm
import redis
from django.conf import settings

# For local
#locale.setlocale(locale.LC_ALL, "ru_ru.UTF-8")
#r = redis.StrictRedis(host=settings.REDIS_HOST,
#                      port=settings.REDIS_PORT,
#                      db=settings.REDIS_DB)

# for heroku
r = redis.from_url(os.environ.get("REDIS_URL"))


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
    return render(request, 'private_chat/room.html', {
        'room_name': room_name, 'private_messages': messages, 'opponent': opponent
    })
