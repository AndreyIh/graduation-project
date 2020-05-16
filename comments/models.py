from django.db import models
from blogs.models import Blog
from django.contrib.auth.models import User


class Comment(models.Model):
    blog_origin = models.ForeignKey(Blog, on_delete=models.CASCADE,
                                    related_name='comments', verbose_name='Комментарий к блогу')
    comment_text = models.TextField(verbose_name='Комментарий')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_origin = models.IntegerField(default=0, verbose_name='подкомментарий')
    lvl = models.IntegerField(default=0, verbose_name='уровень ветки')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['create_time']
