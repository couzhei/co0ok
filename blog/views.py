# The logic of your application goes here; each view recieves an HTTP
# request, processes it, and returns a response

from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Post


def post_list(request):  # my first view
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    # Dude, don't you have a model manager for published already?
    return render(
        request,
        "blog/post/list.html",
        {
            "posts": posts,
        },
    )
    # we could also create a customised model manager
    # the default django's model manager is objects


def post_detail(request,
                # id, # after deciding to make our URLs more SEO-friendly
                year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No such post found.")
    # or
    post = get_object_or_404(  # from django.shortcuts
        Post,
        # id=id,
        slug=post,
        published_on__year=year,
        published_on__month=month,
        published_on__day=day,
        status=Post.Status.PUBLISHED,
    )

    return render(
        request,
        "blog/post/detail.html",
        {"post": post},
    )
