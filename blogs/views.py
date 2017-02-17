from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Blog, BlogCategory, BlogComment, BlogNestedComment
from .forms import BlogForm, BlogCommentForm

# Create your views here.

blog_show_per_page = 10
blog_home_char_show = 100


def index(request, page=0):
    page = int(page)
    start_ind = page * blog_show_per_page

    form = BlogForm(request.POST or None)
    if form.is_valid():
        categories = form.cleaned_data.get('categories').split(' ')

        blog = Blog()
        blog.title = form.cleaned_data.get('title')
        blog.author = request.user
        blog.text = form.cleaned_data.get('text')
        blog.save()

        for category in categories:
            res = BlogCategory.objects.filter(name = category)
            if res.count() == 0:
                blog_category = BlogCategory()
                blog_category.name = category
                blog_category.save()
            else:
                blog_category = res[0]
            blog_category.blog.add(blog)

    blogs = Blog.objects.all().order_by('-publish_time')[start_ind:start_ind + blog_show_per_page]
    # only render first 100 character
    for blog in blogs:
        if len(blog.text) > blog_home_char_show:
            blog.text = blog.text[:blog_home_char_show] + "......"

    form = BlogForm()
    return render(request, "blogs/index.html", {"blogs": blogs, "form": form})


def archive(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comment_form = BlogCommentForm()
    nested_comment_form = BlogCommentForm()
    return render(request, "blogs/detail.html", {"blog": blog, 'comment_form': comment_form,
                                                 'nested_comment_form': nested_comment_form})


def addComment(request, blog_id):
    form = BlogCommentForm(request.POST)
    if form.is_valid():
        comment = BlogComment()
        comment.author = request.user
        comment.text = form.cleaned_data.get('text')
        comment.blog = get_object_or_404(Blog, id=blog_id)
        comment.save()
        return HttpResponseRedirect(reverse('blogs:archive', args=(blog_id,)))


def addNestedComment(request, comment_id):
    form = BlogCommentForm(request.POST)
    if form.is_valid():
        nested_comment = BlogNestedComment()
        nested_comment.author = request.user
        nested_comment.text = form.cleaned_data.get('text')
        nested_comment.blog_comment = get_object_or_404(BlogComment, id=comment_id)
        nested_comment.save()

        comment = get_object_or_404(BlogComment, id=comment_id)
        return HttpResponseRedirect(reverse('blogs:archive', args=(comment.blog.id,)))







