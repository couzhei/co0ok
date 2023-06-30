from django.urls import path
from . import views

app_name = "blog"  # application namespace


# URL patterns allow you to map URLs to views
urlpatterns = [
    # post views
    path("", views.post_list, name="post_list"),
    path("<int:id>/", views.post_detail, name="post_detail"),
]

# all urlpattern are in form of a path
# with three arguments:
# 1.string pattern
# 2.a view
# 3.(optionally) a name that allows you to name the
# the URL pattern project-wide


# django runs through each URL pattern and stops at the first
# occurence

#
