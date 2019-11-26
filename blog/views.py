from django.shortcuts import render
from blog.forms import CommentForm
from blog.models import Post, Comment


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {"posts": posts}
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)

    form = CommentForm()
    if request.method == "POST":
        # make copy of blank form to show if comment submitted successfully
        pDict = request.POST.copy()
        form = CommentForm(pDict)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            form = CommentForm

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog_detail.html", context)
