from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from .models import Post, Category, Comment, PostImage, Author
from .serializers import PostSerializer, CategorySerializer, CommentSerializer,  PostImageSerializer, AuthorSerializer
from .filters import PostFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrAuthenticated, IsAuthorOrAdmin, IsAdminOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = PostFilter
    permission_classes = [IsAdminOrAuthenticated, IsAuthorOrAdmin]
    search_fields = ['title', 'author']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    
class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'post_pk': self.kwargs['post_pk']}

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
    serializer_class = CommentSerializer
    # permission_classes = [IsCommenter]

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_pk).all()

    def get_serializer_context(self):
        return {'post_pk': self.kwargs['post_pk']}
    

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser] #Only admin users can access all ations

    #Each authenticated user should have access to his/her profile
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        author = Author.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AuthorSerializer(author, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

