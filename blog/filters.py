from django_filters.rest_framework import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'category_id': ['exact'],
        }