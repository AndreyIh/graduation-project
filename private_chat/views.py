from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Private_Message
from .forms import MessageForm
from django.http import Http404, JsonResponse


@login_required(login_url='/accounts/login/')
def dialogs(request):
    users = User.objects.exclude(id=get_user(request).id)
    print(get_user(request).id)
    for user in users:
        user.len_mes = len(Private_Message.objects.filter(interlocutors__id__exact=user.id).filter(
            interlocutors__id__exact=get_user(request).id))
        
    return render(request, 'private_chat/dialogs.html', {'users': users})


@login_required(login_url='/accounts/login/')
def chat(request, user_1, user_2):
    if user_2 == get_user(request).id and user_2 != user_1:   
        messages = Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(interlocutors__id__exact=user_2)
        form = MessageForm(request.POST or None)
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
                len_mes= len(messages)
                return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                                  'private_messages': messages, 'form': form,
                                                                  'len_mes': len_mes})
            len_mes = len(messages)
            form = MessageForm()
            return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                              'private_messages': messages, 'form': form, 'len_mes': len_mes})
        len_mes = len(messages)
        form = MessageForm()
        return render(request, 'private_chat/chat.html', {'user_1': user_1, 'user_2': user_2,
                                                          'private_messages': messages, 'form': form, 'len_mes': len_mes})
    else:
        return redirect('/dialogs/')


def add_ajax(request):
    old_len = int(request.GET.get('len_mes'))
    user_1 = int(request.GET.get('user_1'))
    user_2 = int(request.GET.get('user_2'))
    new_len = len(Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(
        interlocutors__id__exact=user_2))
    if request.is_ajax():
        if new_len - old_len > 0:
            response = {'private_messages': 'У вас есть новые сообщения. Показать', 'len_mes': (new_len - old_len)}
            return JsonResponse(response)
        else:
            response = {'private_messages': 'Новых сообщений нет', 'len_mes': (new_len - old_len)}
            return JsonResponse(response)
    else:
        raise Http404