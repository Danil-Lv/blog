from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'author')
    # list_display_links = ('text', 'author')
    search_fields = ['text']





admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow)
admin.site.register(Category)