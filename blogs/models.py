from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from pytils.translit import slugify


class Blog(models.Model):
    STATUS_CHOICES = (
        ('проект', 'Проект'),
        ('финал', 'Финал'),
    )
    title = models.CharField(max_length=255, verbose_name='Тема')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True)
    content = RichTextField(verbose_name='Пост')
    slug = models.SlugField(max_length=250, unique_for_date='create_time')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"{self.title} автор {self.author}"

    def save(self, *args, **kwargs):
        print('slug', slugify(self.title))
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('comments:comment', args=[self.create_time.year,
                                                 self.create_time.month, self.create_time.day, self.slug])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-create_time']
