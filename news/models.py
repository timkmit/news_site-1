from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone


class Account(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,
                                primary_key = True)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name="Дата публикации")


class Likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    news = models.ForeignKey("News",
                             on_delete=models.CASCADE)


class Key_word(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ключевое слово"
        verbose_name_plural = "Ключевые слова"


class Ip(models.Model):
    ip = models.CharField(max_length=100,)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "ip"
        verbose_name_plural = "ip"


class News(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE,blank = True,
                              null=True, verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_ad = models.DateTimeField(default=timezone.now,
                                      verbose_name="Дата публикации")
    title_content = models.CharField(max_length=200,
                                     verbose_name="Завлекающая инфомация")
    updated_ad = models.DateTimeField(auto_now=True,
                                      verbose_name="Обновлено")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',
                              verbose_name="Фото", blank=True)
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 null=True, verbose_name="Категория")
    views = models.ManyToManyField(Ip, related_name="post_views",
                                   blank=True)
    key_word = models.ManyToManyField(Key_word, blank=True)

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()


    def total_likes(self):
        return self.likes_set.count()

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_ad']

    def Контент(self,):
        return self.content[:35]
    Контент.short_content = "Content"


class Category(models.Model):
    title = models.CharField(max_length=150,db_index=True,
                             verbose_name='Наименование категории ')

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ['-pk']

    def __str__(self):
        return self.title




