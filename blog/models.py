from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .utils import get_slug



User = get_user_model()


class Category(models.Model):
    """Категория"""
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Post(models.Model):
    """Пост"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    date_post = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', verbose_name='Категория',
                                 null=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'url': self.slug})

    # @property
    def is_today(self):
        return date.today() == date(self.date_post.year, self.date_post.month, self.date_post.day)

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ('-id',)


class Comment(models.Model):
    """Комментарий"""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True,
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ('-id',)


class Follow(models.Model):
    """Подписка"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True,
                             verbose_name='Подписчик', help_text='Кто подписался')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', null=True, verbose_name='Автор',
                               help_text='На кого подписался')

    # def __str__(self):
    #     return f'{self.user} - {self.author}'

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
