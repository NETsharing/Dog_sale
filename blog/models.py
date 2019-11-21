from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post (models.Model):
    STATUS_CHOICE = (('draft', 'Draft'),('published', 'Published'),)
    title = models.CharField(max_length=250, verbose_name='заголовок сообщения')
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name="URL")                      #SEO-дружественных URL-адресов
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField(null=True, verbose_name='Текст объявления', blank=True, editable=True)
    publish = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    object = models.Manager
    published = PublishedManager()
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
