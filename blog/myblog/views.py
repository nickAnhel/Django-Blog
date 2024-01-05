from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse  # Http404

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

from .models import Post
from .forms import EmailPostForm, CommentForm


# View for processing a list of posts
# Function
# def post_list(request: HttpRequest) -> HttpResponse:
#     post_list = Post.published.all()

#     # Pagination
#     paginator = Paginator(post_list, 2)
#     page_number = request.GET.get('page', 1)

#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages) # Return the last page if page index out of range
#     except PageNotAnInteger:
#         posts = paginator.page(1) # Return the first page if page number not an integer

#     return render(request, 'myblog/post/list.html', {'posts': posts})


# Class
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "myblog/post/list.html"


# View for processing a single post page with comments
def post_detail(
    request: HttpRequest, year: int, month: int, day: int, post
) -> HttpResponse:
    """
    # Solution with try/except
    try:
        post = Post.published.get(publish__year=year, publish__month=month, publish__day=day, slug=post)
    except Post.DoesNotExist:
        raise Http404('Post not found')
    """

    # Solution with shortcut function (MVC)
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(
        request,
        "myblog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


# View for processing email form
def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # cd - dictonary type {"form_field": data}
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'c comments: {cd['comments']}"
            )

            send_mail(subject, message, "anhimovn1@gmail.com", [cd["to"]])
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request, "myblog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


# View for processing comment form
@require_POST
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)  # Not save to db
        comment.post = post
        comment.save()

    return render(
        request,
        "myblog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
