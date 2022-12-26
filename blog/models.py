from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from time import time
from blog.utils import rus_to_eng


# Create your models here.


def get_slug(url):
    return slugify(rus_to_eng(url)) + f'-{int(time())}'


User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    date_post = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', verbose_name='Категория', null=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'url': self.slug})

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ('-id', )
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True, verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ('-id', )


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True, verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', null=True, verbose_name='Автор (На кого подписались)')

    # def __str__(self):
    #     return f'{self.user} - {self.author}'

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'



