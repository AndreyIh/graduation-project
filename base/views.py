# from ckeditor.widgets import LazyEncoder
# from django.core.serializers import serialize
# messages = serialize('json', messages, cls=LazyEncoder)
from django.shortcuts import render
from django.http import Http404, JsonResponse
from private_chat.models import Private_Message


def resume(request):
    return render(request, 'resume.html', )


def add_ajax(request):
    old_len = int(request.GET.get('len_mes'))
    user_1 = int(request.GET.get('user_1'))
    user_2 = int(request.GET.get('user_2'))
    new_len = len(Private_Message.objects.filter(interlocutors__id__exact=user_1).filter(
        interlocutors__id__exact=user_2))
    print(old_len, new_len, new_len - old_len)
    if request.is_ajax():
        if new_len - old_len > 0:
            response = {'private_messages': 'У вас есть новые сообщения. Показать', 'len_mes': (new_len - old_len)}
            return JsonResponse(response)
        else:
            response = {'private_messages': 'Новых сообщений нет', 'len_mes': (new_len - old_len)}
            return JsonResponse(response)
    else:
        raise Http404
