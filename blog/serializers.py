from rest_framework import serializers
from .models import BlogPost, Comment


# ✅ Serializer for blog posts
class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'image', 'created_at', 'updated_at', 'likes_count']


# ✅ Serializer for comments (this was missing)
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['author', 'post', 'created_at']
