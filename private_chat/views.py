from datetime import datetime
import locale
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Private_Message
from .forms import MessageForm
from django.http import Http404, JsonResponse
import redis
from django.conf import settings


locale.setlocale(locale.LC_ALL, "ru_ru")
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required(login_url='/accounts/login/')
def dialogs(request):
    users = User.objects.exclude(id=get_user(request).id)
    return render(request, 'private_chat/dialogs.html', {'users': users})


@login_required(login_url='/accounts/login/')
def chat(request, user_1, user_2):

    if user_2 == get_user(request).id and user_2 != user_1:
        key_user = [str(user_1), str(user_2)]
        key_user.sort()
        key_user = ''.join(key_user)
        messages = Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(
            interlocutors__id__exact=user_2)
        r.set(key_user, len(messages))
        total_messeges = int(r.get(key_user))
        if request.method == 'POST':
            form = MessageForm(request.POST or None)
            if form.is_valid():
                data = form.cleaned_data
                message = data['message']
                privat_message = Private_Message(messages=message, author=get_user(request))
                privat_message.save()
                privat_message.interlocutors.add(user_1)
                privat_message.interlocutors.add(user_2)
                messages = Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(
                    interlocutors__id__exact=user_2)
                form = MessageForm()
                len_mes = len(messages)
                total_messeges = r.incr(key_user)
                return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                                  'private_messages': messages, 'form': form,
                                                                  'len_mes': len_mes, 'total_messages': total_messeges})
            len_mes = len(messages)
            form = MessageForm()
            return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                              'private_messages': messages, 'form': form,
                                                              'len_mes': len_mes, 'total_messages': total_messeges})
        len_mes = len(messages)
        form = MessageForm()
        return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                          'private_messages': messages, 'form': form,
                                                          'len_mes': len_mes, 'total_messages': total_messeges})
    else:
        return redirect('/dialogs/')


def add_ajax(request):
    key_user = [request.GET.get('user_1'), request.GET.get('user_2')]
    key_user.sort()
    key_user = ''.join(key_user)
    if request.is_ajax():
        total_messages = int(request.GET.get('total_messages'))
        new_messages = int(r.get(key_user)) - total_messages
        if new_messages:
            user_1 = int(request.GET.get('user_1'))
            user_2 = int(request.GET.get('user_1'))
            new_mes = Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(
                interlocutors__id__exact=user_2).order_by('-create_time').first()
            print(new_mes.messages)
            message_create_time = datetime.strftime(new_mes.create_time, '%d %B %Y г. %H:%M')
            response = {'private_messages': 'У вас есть новые сообщения. Показать',
                        'new_messages': new_messages,
                        'total_messages': int(r.get(key_user)),
                        "message": new_mes.messages,
                        'author': new_mes.author.username,
                        'time': message_create_time}
            return JsonResponse(response)
        else:
            return JsonResponse({'private_messages': 'Новых сообщений нет',
                                 'new_messages': 0, 'total_messages': total_messages})
    else:
        raise Http404


def add_ajax1(request):
    print('ajax1')
    for i in request.session.keys():
        print(i, request.session[i])

    if request.is_ajax():
        return JsonResponse({'ok': 'ok'})
    else:
        raise Http404
