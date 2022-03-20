import datetime
from pathlib import Path
from unittest import mock

import pytz
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from blog.models import Blog, Comment

_TEST_DATA_DIR = Path(__file__).parent / "test_data"
_TEST_IMAGE = _TEST_DATA_DIR / "github-octocat.png"


class ListBlog(APITestCase):
    """
    Test cases for listing blogs.
    """

    def setUp(self):
        baker.make("blog.blog", _quantity=10)

    def test_list_response(self):
        """
        Ensure blog list response is correct.
        """
        url = reverse("blog:blog")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        blogs = response.json()
        self.assertEqual(len(blogs), 10)
        blog = blogs[0]
        self.assertIsInstance(blog["blog_title"], str)
        self.assertIsInstance(blog["blog_description"], str)


class CreateBlog(APITestCase):
    """
    Test cases creating a blog.
    """

    def _create_blog(self):
        url = reverse("blog:blog")
        with open(_TEST_IMAGE, mode="rb") as image_fp:
            data = {
                "blog_title": "A title",
                "blog_description": "A description",
                "image": image_fp,
            }
            return self.client.post(url, data=data, format="multipart")

    def test_create_response(self):
        """
        Ensure blog creation response is correct.
        """
        response = self._create_blog()
        self.assertEqual(response.status_code, 201)
        # Since uploaded image filename is auto-generated and unique we can't compare
        # the full response with a single statement
        response_body = response.json()
        self.assertEqual(
            sorted(response_body.keys()),
            sorted(["id", "blog_title", "blog_description", "image"]),
        )
        self.assertEqual(response_body["id"], 1)
        self.assertEqual(response_body["blog_title"], "A title")
        self.assertEqual(response_body["blog_description"], "A description")
        self.assertTrue(response_body["image"].startswith("http://testserver/uploads/"))

    def test_create_db(self):
        """
        Ensure blog creation in the database is correct.
        """
        self._create_blog()
        self.assertEqual(Blog.objects.count(), 1)
        blog = Blog.objects.get()
        self.assertEqual(blog.blog_title, "A title")
        self.assertEqual(blog.blog_description, "A description")


_DATE_CREATED = datetime.datetime(2022, 3, 1, 0, 0, 0, tzinfo=pytz.utc)


class CreateComment(APITestCase):
    """
    Test cases creating a blog comment.
    """

    def setUp(self):
        baker.make("blog.blog", _quantity=10)

    def _create_comment(self, blog_id):
        url = reverse("blog:blog-comment", args=(blog_id,))
        data = {"blog": blog_id, "comment_text": "A comment"}
        return self.client.post(url, data=data)

    @mock.patch("django.utils.timezone.now", return_value=_DATE_CREATED)
    def test_create_response(self, _):
        """
        Ensure comment creation response is correct.
        """
        response = self._create_comment(1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "blog": 1,
                "comment_text": "A comment",
                # .isoformat() returns '2022-03-01T00:00:00+00:00' rather than
                # '2022-03-01T00:00:00Z
                "creation_date": _DATE_CREATED.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        )

    @mock.patch("django.utils.timezone.now", return_value=_DATE_CREATED)
    def test_create_db(self, _):
        """
        Ensure comment creation in the database is correct.
        """
        self._create_comment(1)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get()
        self.assertEqual(comment.blog.id, 1)
        self.assertEqual(comment.comment_text, "A comment")
        self.assertEqual(comment.creation_date, _DATE_CREATED)
