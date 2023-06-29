from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # very sophisticated user abstraction


# Create your models here.
class Post(models.Model):
    """Model definition for Post."""

    class Status(models.TextChoices):
        """an enumeration class for the post status
        with available choices DRAFT and published_onED
        with their respective values DF and PB
        and their labels for readable name are
        Draft and published_oned
        """

        DRAFT = "DF", "Draft"
        published_onED = "PB", "published_oned"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )  # models.CASCADE ?!?!!??! What does it?!

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=250)
    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Post."""

        # verbose_name = "Post"
        # verbose_name_plural = "Posts"
        ordering = ["-published_on"]
        indexes = [
            models.Index(fields=["-published_on"]),
        ]

    def __str__(self):
        """Unicode representation of Post."""
        return self.title
