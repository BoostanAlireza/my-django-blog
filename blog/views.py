from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from .models import Post, Category, Comment
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from .filters import PostFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = PostFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'author']
    ordering_fields = ['created_at']


# class CategoryPostViewSet(ReadOnlyModelViewSet):
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         return Post.objects.filter(category_id=self.kwargs['category_pk'])


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(posts_count=Count('posts')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]