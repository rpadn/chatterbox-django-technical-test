# Technical Test Django
The project lets you create blogs and comments for each blog.

A blog contains a title, a description and an optional image.
A comment is plain text linked to a blog.

## Getting Started

These instructions will get you a clone of the project up and running on your local machine for development and testing purposes.
### Prerequisites
```
python 3.8
```
### Installing and Initial Setup

**[Optional]** 
Before the installation, a best practise would be setting a virtualenv for the project 

```
https://virtualenv.pypa.io/
```

All the necessary libraries are in requirements.txt
```
pip install -r requirements.txt
```

## Running the application

```
python manage.py runserver
```

You will need to setup the database the first time you run the app. In order to
do this simply run:
```

python manage.py migrate
```

### `/api/blog/`

The `/api/blog/` endpoint lets you list the existing blogs, and create a new
blog.

To list blogs:
```
GET /api/blog/
```

To create a blog you need to POST a form (multipart POST data):
```
POST /api/blog/
blog_title="A blog title"
blog_description="The blog description"
```

You can also upload an image when creating a blog:
```
POST /api/blog/
blog_title="A blog title"
blog_description="The blog description"
image=/path/to/image
```

### `/api/blog/<blog-id>/comment/`

The `/api/blog/<blog-id>/comment/` endpoint lets you create a comment for an
existing blog.

To create a comment you need to POST a form (multipart POST data):
```
POST /api/blog/1/comment/
blog=1
comment_text="A comment"
```

The application currently does not support listing existing comments.


## Running tests
Tests can be executed by simply running:
```
python manage.py test
```

## Known issues / design decisions
- Images are managed by a `django.db.models.FileField`: while this works, it is
  not as secure as `django.db.models.ImageField` (which checks that the
  uploaded file is a valid image). By installing `Pillow` this field can be
  replaced
- When posting a comment, the blog id needs to be passed both in the endpoint
  and in the data posted. This is redundant and ideally the application should
  be able to infer the blog-id from the URL directly.

## Notes
Although the guidelines were saying to complete the exercise in ~2 hours, it
took a bit longer (~3.5h). Time was mostly spent reading the documentation of
django and django-rest-framework, which I've never used before :)

