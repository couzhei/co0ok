# This includes the data models of your applications. All Django apps
# need to have a models.py file but it can be left empty.

from django.db import models
from django.utils import timezone

# very sophisticated user abstraction
from django.contrib.auth.models import User

# introduced for using canonical URLs
from django.urls import reverse

# from django.core.urlresolvers import reverse
# this is what I get for get_ab autocompletion

# for tagging our blogs (pip install django-taggit)
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    # my first model manager please use mngr snippet
    def get_queryset(self):
        return (
            super(PublishedManager, self)
            .get_queryset()
            .filter(status=Post.Status.PUBLISHED)
        )


# Create your models here.
class Post(models.Model):
    """Model definition for Post."""

    class Status(models.TextChoices):
        """an enumeration class for the post status
        with available choices DRAFT and PUBLISHED
        with their respective values DF and PB
        and their labels for readable name are
        Draft and published.
        """

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    tags = TaggableManager()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )  # models.CASCADE ?!?!!??! What does it do?!

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique_for_date="published_on")
    # unique_for_date added since I decided to use slug for creating
    # canonical urls, so what's their point not being uniquely defined?
    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    # model managers for post
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager

    class Meta:
        """Meta definition for Post."""

        # verbose_name = "Post"
        # verbose_name_plural = "Posts"
        ordering = ["-published_on"]
        # Blog posts are usually displayed in reverse chronological order
        # (from newest to oldest)
        indexes = [
            models.Index(fields=["-published_on"]),
        ]

    def __str__(self):
        """Unicode representation of Post."""
        return self.title

    def get_absolute_url(self):
        """
        The reverse() function will build the URL dynamically using the
        URL name defined in the URL patterns. If check out blog/urls.py

        path("<int:id>/", views.post_detail, name="post_detail")

        We have used the blog namespace followed by a colon and the URL
        name post_detail. Remember that the blog namespace is defined in
        the main urls.py file of the project when including the URL
        patterns from blog.urls. The post_detail URL is defined above.
        The resulting string, blog:post_detail, can be used globally in
        your project to refer to the post detail URL. This URL has a
        required parameter that is id in this case.
        """
        return reverse(
            "blog:post_detail",
            args=[  # self.id,
                self.published_on.year,
                self.published_on.month,
                self.published_on.day,
                self.slug,
            ],
        )

    # def get_absolute_url(self):
    # # The canonical URL for a blog post detail view currently looks like /blog/1/
    #     from django.core.urlresolvers import reverse
    #     return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """A Model to handle comments given to a post, which
    is a many to one relationship."""

    post = models.ForeignKey(  # type: ignore
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    # this related_name is funny! it allows us to name the
    # attribute that you use for the relationship from
    # related object back to this one

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Comment."""

        ordering = ["created_on"]
        indexes = [
            models.Index(fields=["created_on"]),
        ]

    def __str__(self):
        """Unicode representation of Comment."""
        return f"Comment by {self.name} on {self.post}"

