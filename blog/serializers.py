from rest_framework import serializers
from blog.models import Blog, Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment.
    """
    class Meta:
        model = Comment
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog.
    """
    class Meta:
        model = Blog
        fields = '__all__'
