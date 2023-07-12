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

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )  # models.CASCADE ?!?!!??! What does it do?!

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=250,
                            unique_for_date="published_on")
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
        return reverse('blog:post_detail',
                       args=[  # self.id,
                           self.published_on.year,
                           self.published_on.month,
                           self.published_on.day,
                           self.slug])

    # def get_absolute_url(self):
    #     from django.core.urlresolvers import reverse
    #     return reverse('blog:post_detail', kwargs={'pk': self.pk})
