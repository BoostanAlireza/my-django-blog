from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
 

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.CharField(max_length=255)
    body = models.TextField()
    placed_at = models.DateTimeField(auto_now_add=True)
    