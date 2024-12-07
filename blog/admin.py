from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'category']
    prepopulated_fields = {
        'slug': ['title']
    }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'commenter']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass