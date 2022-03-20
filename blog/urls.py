from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("blog/", views.BlogAPIView.as_view(), name="blog"),
    path("blog/<int:pk>/comment/", views.CommentAPIView.as_view(), name="blog-comment"),
]
