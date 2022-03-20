from django.db import models


class Blog(models.Model):
    """
    Create blog model with corresponding requirements
    """

    blog_title = models.CharField(max_length=50)
    blog_description = models.TextField()
    # FIXME: this does not validate the uploaded file format! With Pillow available
    # an ImageField could be used to validate the uploaded file
    image = models.FileField(upload_to="uploads/%Y/%m/%d/", default=None)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    """
    Comment blog model with corresponding requirements
    """

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_text = models.TextField()
    creation_date = models.DateTimeField("date_created", auto_now_add=True)

    def __str__(self):
        return self.comment_text
