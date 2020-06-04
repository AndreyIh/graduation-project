from django.urls import path
from .views import dialogs, room


urlpatterns = [
    path('', dialogs, name='dialogs'),
    path('<str:room_name>/', room, name='room'),
]
