from django.contrib import admin
from django.utils.html import format_html
from . import models


class PostImageInline(admin.TabularInline):
    model = models.PostImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'category']
    prepopulated_fields = {
        'slug': ['title']
    }
    inlines = [PostImageInline]

    class Media:
        css = {
            'all': ['blog/styles.css']
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