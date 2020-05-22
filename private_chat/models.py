from django.db import models
from django.contrib.auth.models import User


class Private_Message(models.Model):
    interlocutors = models.ManyToManyField(User)
    messages = models.TextField(verbose_name='Комментарий')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    new_message = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='author', default='1')
    #opponent = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['create_time']
