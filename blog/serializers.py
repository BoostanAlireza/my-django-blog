from rest_framework import serializers
from .models import Post, Category, Comment,  PostImage, Author


class PostImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        post_id = self.context['post_pk']
        return PostImage.objects.create(post_id=post_id, **validated_data)

    class Meta:
        model = PostImage
        fields = ['id', 'image']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'created_at', 'category', 'images']



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

       
class AuthorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Author
        fields = ['id', 'user_id', 'bio', 'birth_date', 'phone', 'user_photo']