from django.shortcuts import render
from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Post, Category, Comment
from .serializers import PostSerializer, CategorySerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# class CategoryPostViewSet(ReadOnlyModelViewSet):
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         return Post.objects.filter(category_id=self.kwargs['category_pk'])


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(posts_count=Count('posts')).all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer