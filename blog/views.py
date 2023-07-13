# The logic of your application goes here; each view recieves an HTTP
# request, processes it, and returns a response

from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

# Now let's use some class-based views
from django.views.generic import ListView

# Create your views here.
from .models import Post

# pagination is on the way
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):  # my first view
#     # posts = Post.objects.filter(status=Post.Status.PUBLISHED)
#     # I use model manager created for published posts
#     post_list = Post.published.all()

#     # Pagination with 3 posts per page
#     paginator = Paginator(post_list, 5)
#     page_number = request.GET.get("page", 1)
#     # posts = paginator.page(page_number) to handle errors

#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:  # this way we can easily handle numbers that exceeds our pages
#         posts = paginator.page(paginator.num_pages)
#     # in case of not an integer number for pagination?
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(
#         request,
#         "blog/post/list.html",
#         {
#             "posts": posts,
#         },
#     )
#     # we could also create a customised model manager
#     # the default django's model manager is objects
# farewell to function-based views for now


class PostListView(ListView):
    """
    Listing posts
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/post/list.html"


def post_detail(
    request,
    # id, # after deciding to make our URLs more SEO-friendly
    year,
    month,
    day,
    post,
):
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
