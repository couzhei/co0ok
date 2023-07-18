# This is where you register models to include them in the Django
# administration site (using this site is optional)

from django.contrib import admin
from .models import Post, Comment

# Register your models here.
# admin.site.register(Post) # or using the below decorator

# TODO: Complete CommentAdmin


# Customize the display of your models in adminstration site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """These are all pre-defined properties, so
    assigning them to the provided values, will indeed
    induces some functionalities
    """

    list_display = ["title", "slug", "author", "published_on", "updated_on", "status"]
    list_filter = ["status", "created_on", "published_on", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "published_on"
    ordering = ["status", "published_on"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin View for Comment"""

    list_display = ("name", "email", "post", "created_on", "active")
    list_filter = ("active", "created_on", "updated_on")
    search_fields = ("name", "email", "body")

    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ("",)
    # readonly_fields = ("",)

    # date_hierarchy = ""
    # ordering = ("",)
