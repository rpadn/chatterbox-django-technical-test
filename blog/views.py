from rest_framework.generics import CreateAPIView, ListCreateAPIView

from blog.models import Blog
from blog.serializers import BlogSerializer, CommentSerializer


class BlogAPIView(ListCreateAPIView):
    """
    View for listing all blogs.
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentAPIView(CreateAPIView):
    """
    View for creating a blog comment.
    """

    serializer_class = CommentSerializer
