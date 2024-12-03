from rest_framework import serializers
from .models import Post, Category, Comment



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'created_at', 'category']


class CategorySerializer(serializers.ModelSerializer):
    # posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='category-posts-list')
    class Meta:
        model = Category
        fields = ['id', 'title', 'posts_count']

    posts_count = serializers.IntegerField(read_only=True)



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'commenter', 'placed_at', 'body']

        