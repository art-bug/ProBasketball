from django.db import models

from .signals import *


@autoslug_by('title')
class News(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True)
    release = models.CharField(max_length=150, verbose_name='Анонс')
    content = models.TextField(blank=True, db_index=True, verbose_name='Текст')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
