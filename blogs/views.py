import math
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Blog, BlogCategory, BlogComment, BlogNestedComment
from .forms import BlogForm, BlogCommentForm

# Create your views here.

blog_show_per_page = 10
blog_home_char_show = 100
blog_display_page = 7  # should be odd number


def getPageList(cur_page, page_count):
    left = int(cur_page - (blog_display_page - 1) / 2)
    right = int(cur_page + (blog_display_page - 1) / 2)
    if left <= 2:
        if blog_display_page <= page_count - 1:
            right = 1 + blog_display_page
        else:
            right = page_count
    if right >= page_count - 1:
        if blog_display_page <= page_count - 1:
            left = page_count - blog_display_page
        else:
            left = 1

    if left <= 2:
        left = 1
    if right >= page_count - 1:
        right = page_count

    if left == 1:
        res = [str(x) for x in range(left, 1 + right)]
    else:
        res = ['1', '...'] + [str(x) for x in range(left, right + 1)]
    if right <= page_count - 2:
        res += ['...', str(page_count)]
    return res


def index(request, page=1):
    page = int(page) - 1
    start_ind = page * blog_show_per_page

    context = {}
    form = BlogForm(request.POST or None)

    if form.is_valid():
        categories = form.cleaned_data.get('categories').split(' ')

        blog = Blog()
        blog.title = form.cleaned_data.get('title')
        blog.author = request.user
        blog.text = form.cleaned_data.get('text')
        blog.save()

        for category in categories:
            res = BlogCategory.objects.filter(name=category)
            if res.count() == 0:
                blog_category = BlogCategory()
                blog_category.name = category
                blog_category.save()
            else:
                blog_category = res[0]
            blog_category.blog.add(blog)
        return HttpResponseRedirect(reverse('blogs:index'))

    elif len(form.data) > 0:
        context['anchor'] = 'post_form'

    blogs = Blog.objects.all().order_by('-publish_time')[start_ind:start_ind + blog_show_per_page]

    page_list = getPageList(page, math.ceil(Blog.objects.count() / blog_show_per_page))
    # only render first 100 character
    for blog in blogs:
        if len(blog.text) > blog_home_char_show:
            blog.text = blog.text[:blog_home_char_show] + "......"

    context['blogs'] = blogs
    context['form'] = form
    context['page_list'] = page_list
    context['page'] = page + 1
    return render(request, "blogs/index.html", context)


def archive(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    blogs = Blog.objects.all().order_by('-publish_time')
    # the related page to that blog
    page = str(int([x.id for x in blogs].index(int(blog_id)) / blog_show_per_page) + 1)

    comment_form = BlogCommentForm()
    nested_comment_form = BlogCommentForm()
    return render(request, "blogs/detail.html", {"blog": blog, 'comment_form': comment_form,
                                                 'nested_comment_form': nested_comment_form,
                                                 'page': page, },)


def addComment(request, blog_id):
    form = BlogCommentForm(request.POST)
    if form.is_valid():
        comment = BlogComment()
        comment.author = request.user
        comment.text = form.cleaned_data.get('text')
        comment.blog = get_object_or_404(Blog, id=blog_id)
        comment.save()
        return HttpResponseRedirect(reverse('blogs:archive', args=(blog_id,)))
    else:
        raise Http404("Page not found")


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
    else:
        raise Http404("Page not found")







