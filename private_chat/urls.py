from django.urls import path
from .views import dialogs, chat, room


urlpatterns = [
    path('<str:room_name>/', room, name='room'),
    path('', dialogs, name='dialogs'),
    path('chat/<int:user_1>-<int:user_2>/', chat, name='chat'),
]
