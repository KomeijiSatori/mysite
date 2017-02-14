from django.shortcuts import render
from .models import Blog, BlogCategory
from .forms import BlogForm

# Create your views here.

blog_show_per_page = 10
blog_home_char_show = 100


def index(request, page = 0):
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
            if res is None:
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









