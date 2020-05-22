from django.urls import path
from .views import dialogs, chat


urlpatterns = [
    path('', dialogs, name='dialogs'),
    path('chat/<int:user_1>-<int:user_2>/', chat, name='chat'),
]
