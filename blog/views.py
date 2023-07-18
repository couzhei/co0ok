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
from .forms import EmailPostForm, CommentForm

# This one for sending emails
from django.core.mail import send_mail  # , send_mass_mail

# pagination is on the way
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# this is for comments' forms, we expect them to be submitted
# using HTTP POST method
from django.views.decorators.http import require_POST

# to utilize our tag system
from taggit.models import Tag


def post_list(request, tag_slug=None):  # my first view
    # posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    # I use model manager created for published posts
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page", 1)
    # posts = paginator.page(page_number) to handle errors

    try:
        posts = paginator.page(page_number)
    except EmptyPage:  # this way we can easily handle numbers that exceeds our pages
        if int(page_number) > paginator.num_pages:
            posts = paginator.page(paginator.num_pages)
        else:
            posts = paginator.page(1)
    # in case of not an integer number for pagination?
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(
        request,
        "blog/post/list.html",
        {
            "posts": posts,
            "tag": tag,
        },
    )
    # we could also create a customised model manager
    # the default django's model manager is objects


# farewell to function-based views for now
# oopsie doopsie, back to it after playing around with tags


class PostListView(ListView):
    """
    Listing posts
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/post/list.html"

    def get_queryset(self):
        """
        In Django, when a class-based view is used, several methods are
        automatically called during the request/response cycle. One of
        these methods is get_queryset(), which is called internally by
        Django when you use a class-based view that inherits from ListView.

        When you provide a URL with a tag, such as /tag/tag-slug/, Django's
        URL routing mechanism will match the URL pattern defined in your urls.py
        file, which maps to the PostListView class-based view. The PostListView
        is then instantiated, and its get_queryset() method is called.

        In this case, the tag_slug is extracted from the URL using
        self.kwargs.get("tag_slug"). If a tag slug is present in the URL, the
        method retrieves the corresponding Tag object from the database and
        filters the queryset to include only posts associated with that tag.
        If no tag slug is present, all published posts are returned.

        By overriding the get_queryset() method, you can dynamically modify
        the queryset based on the requested URL parameters or any other custom
        logic you want to implement.
        """
        # Retrieve the tag slug from the URL parameter
        tag_slug = self.kwargs.get("tag_slug")

        if tag_slug:
            # Get the tag object based on the slug
            tag = get_object_or_404(Tag, slug=tag_slug)
            # Filter the posts based on the specified tag
            queryset = Post.published.filter(tags__in=[tag])
        else:
            # If no tag is specified, retrieve all published posts
            queryset = Post.published.all()

        return queryset


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

    # List of active comments for this post
    comments = post.comments.filter(active=True)  # type: ignore
    # Form for users to comment
    form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )

    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {
            "post": post,
            "form": form,
            "comment": comment,
        },
    )
