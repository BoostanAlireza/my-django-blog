from django.contrib import admin
from django.db.models import Count
from django.urls import reverse 
from django.utils.http import urlencode
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
    list_display = ['title', 'author',
                    'created_at', 'category',
                    'num_of_comments']
    prepopulated_fields = {
        'slug': ['title']
    }
    inlines = [PostImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request)\
                      .prefetch_related('comments')\
                      .annotate(comments_count=Count('comments'))


    @admin.display(ordering='comments_count', description='# comments')
    def num_of_comments(self, post):
        url = (
            reverse('admin:blog_comment_changelist')
            + '?'
            + urlencode({
                'post__id': post.id
            })
        )
        return format_html('<a href="{}">{}</a>', url, post.comments_count)

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


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

    def first_name(self, author):
        return author.user.first_name
    
    def last_name(self, author):
        return author.user.last_name
    
    def email(self, author):
        return author.user.email
    