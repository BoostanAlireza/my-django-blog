from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from .models import Post, Category, Comment, Profile, PostImage
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, ProfileSerializer, PostImageSerializer
from .filters import PostFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = PostFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'author']
    ordering_fields = ['created_at']


class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    #This is for getting the specific image that we want to display and not all images
    def get_queryset(self):
        return PostImage.objects.filter(post_id=self.kwargs['post_pk'])

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


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer