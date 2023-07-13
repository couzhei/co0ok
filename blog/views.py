# The logic of your application goes here; each view recieves an HTTP
# request, processes it, and returns a response

from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

# Now let's use some class-based views
from django.views.generic import ListView

# Create your views here.
from .models import Post, Comment

# Making use of our forms
from .forms import EmailPostForm

# This one for sending emails
from django.core.mail import send_mail  # , send_mass_mail

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


# a function-based view for handling forms
def post_share(request, post_id):
    """
    Takes the request obj and the post_id variable as params
    to handle both HTTP methods GET and POST where
    in case of the latter it'll send an email
    """

    # Retrieve post by its id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":  # POST method
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data  # a dict of form fields and their values
            # In case of failing is_valid(), cleaned_data attribute still got
            # valid fields
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                + f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "couzhei@gmail.com", [cd["to"]])
            sent = True

    # elif request.method == "GET":
    else:
        form = EmailPostForm()  # GET method

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


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
