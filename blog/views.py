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


def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404("No such post found.")
    # or
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED,
    )

    return render(
        request,
        "blog/post/detail.html",
        {"post": post},
    )
