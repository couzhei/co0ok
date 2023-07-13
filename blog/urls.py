from django.urls import path
from . import views

app_name = "blog"  # application namespace
# namespaces have to be unique across your entire project

# URL patterns allow you to map URLs to views
urlpatterns = [
    # post views
    # path("", views.post_list, name="post_list"),
    # modifying urlpatterns to access class-based view instead of function-based
    path("", views.PostListView.as_view(), name="post_list"),
    # in the following we use angle brackets to capture some parameters
    # since any value captured is by default string, we can convert them
    # with path converters the way shown below <int:year>
    path("<int:id>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
]

# modifying urlpatterns to use publication date and slug for the post
# # detail URL.
urlpatterns[1] = path(
    "<int:year>/<int:month>/<int:day>/<slug:post>/",
    views.post_detail,
    name="post_detail",
)


# all urlpattern are in form of a path
# with three arguments:
# 1.string pattern
# 2.a view
# 3.(optionally) a name that allows you to name the
# the URL pattern project-wide


# django runs through each URL pattern and stops at the first
# occurence

#
