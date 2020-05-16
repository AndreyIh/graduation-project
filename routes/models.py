from django.db import models
from trains.models import Train

class Route(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Название марута', unique=True)
    from_city = models.CharField(max_length=100, verbose_name='Откуда')
    to_city=models.CharField(max_length=100, verbose_name='Куда')
    trains = models.ManyToManyField(Train, blank=True,
                                    verbose_name='Список поездов')
    travel_times = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta():
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']



