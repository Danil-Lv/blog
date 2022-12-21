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


class Post(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_post = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'url': self.slug})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', null=True)

    def __str__(self):
        return f'{self.user} - {self.author}'



