from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from .models import Blog, BlogCategory, Comment
from .forms import BlogForm, BlogCommentForm

# Create your views here.

blog_show_per_page = 10
blog_display_page = 7  # should be odd number


def getPageList(cur_page, page_count):
    cur_page = int(cur_page)

    if page_count <= blog_display_page:
        left = 1
        right = page_count
    else:
        left = int(cur_page - ((blog_display_page - 1) / 2 - 1))
        right = int(cur_page + ((blog_display_page - 1) / 2 - 1))
        if left < 2:
            right += 2 - left
            left = 2
        elif right > page_count - 1:
            left -= right - page_count + 1
            right = page_count - 1

    if left == 1:
        res = [x for x in range(left, 1 + right)]
    elif left == 2:
        res = [1] + [x for x in range(left, right + 1)]
    else:
        res = [1, "..."] + [x for x in range(left, right + 1)]
    if right <= page_count - 2:
        res += ['...', page_count]
    elif right == page_count - 1:
        res += [page_count]
    return res


def index(request):
    context = {}
    blog_list = Blog.objects.all().order_by('-publish_time')
    paginator = Paginator(blog_list, blog_show_per_page)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        blogs = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        blogs = paginator.page(page)

    page_list = getPageList(page, paginator.num_pages)

    for blog in blogs:
        blog.publish_time = timezone.localtime(blog.publish_time)

    context['blogs'] = blogs
    context['page_list'] = page_list
    context['title'] = "Blogs"
    return render(request, "blogs/index.html", context)


def archive(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    comment_form = BlogCommentForm()
    comments = Comment.objects.filter(blog=blog)
    return render(request, "blogs/detail.html", {"blog": blog, 'comment_form': comment_form, 'nodes': comments, },)


def addComment(request, blog_id):
    form = BlogCommentForm(request.POST)
    blog = get_object_or_404(Blog, id=blog_id)
    if form.is_valid():
        comment = Comment()
        comment.author = request.user
        comment.text = form.cleaned_data.get('text')
        comment.blog = blog
        comment.save()
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


def addNestedComment(request, comment_id):
    form = BlogCommentForm(request.POST)
    parent_comment = get_object_or_404(Comment, id=comment_id)
    blog = parent_comment.blog
    if form.is_valid():
        comment = Comment()
        comment.parent = parent_comment
        comment.author = request.user
        comment.text = form.cleaned_data.get('text')
        comment.blog = blog
        comment.save()
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


def categoryBlogs(request, category):
    cate = BlogCategory.objects.filter(name=category)

    if cate.count() > 0:
        blogs = cate[0].blog.all()
        blog_list = blogs.order_by('-publish_time')
        paginator = Paginator(blog_list, blog_show_per_page)
        page = request.GET.get('page')
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
            blogs = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.num_pages
            blogs = paginator.page(page)

        for blog in blogs:
            blog.publish_time = timezone.localtime(blog.publish_time)

        page_list = getPageList(page, paginator.num_pages)
    else:
        blogs = []
        page_list = []

    context = {}
    context['blogs'] = blogs
    context['title'] = category
    context['page_list'] = page_list

    return render(request, "blogs/index.html", context)


@login_required
def post(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        categories = form.cleaned_data.get('categories').split(' ')
        categories = list(filter(None, categories))

        blog = Blog()
        blog.title = form.cleaned_data.get('title')
        blog.author = request.user
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        blog.text = request.POST.get("text")
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
    return render(request, "blogs/post.html", {"form": form})


@login_required
def blog_update(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # check if it is the author
    if not(request.user == blog.author or request.user.is_superuser):
        raise PermissionDenied

    category_str = " ".join([x.name for x in blog.blogcategory_set.all()])
    blog_initial = {
        'title': blog.title,
        'text': blog.text,
        'categories': category_str,
    }
    form = BlogForm(request.POST or None, initial=blog_initial)

    if form.is_valid():
        categories = form.cleaned_data.get('categories').split(' ')
        categories = list(filter(None, categories))

        blog.title = form.cleaned_data.get('title')
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        blog.text = request.POST.get("text")
        blog.last_update_time = timezone.now()
        blog.save()

        former_categories = blog.blogcategory_set.all()
        for former_category in former_categories:
            # if old category is removed
            if former_category.name not in categories:
                former_category.blog.remove(blog)
                # if the category has no associated blogs
                if former_category.blog.count() == 0:
                    former_category.delete()

        for category in categories:
            if category not in former_categories:
                res = BlogCategory.objects.filter(name=category)
                if res.count() == 0:
                    blog_category = BlogCategory()
                    blog_category.name = category
                    blog_category.save()
                else:
                    blog_category = res[0]
                # add new related categories
                blog_category.blog.add(blog)
        return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))
    return render(request, "blogs/post.html", {"form": form, "author": blog.author})


def getComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    data = model_to_dict(comment)
    return JsonResponse(data)


def updateComment(request, comment_id):
    form = BlogCommentForm(request.POST)
    comment = get_object_or_404(Comment, id=comment_id)
    blog = comment.blog
    if not(request.user == comment.author or request.user.is_superuser):
        raise PermissionDenied
    if form.is_valid():
        comment.text = form.cleaned_data.get('text')
        comment.last_update_time = timezone.now()
        comment.save()
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


def search(request):
    search_text = request.GET.get('search')
    if search_text:
        blog_list = Blog.objects.all()
        query_list = blog_list.filter(
            Q(title__icontains=search_text) |
            Q(text__icontains=search_text) |
            Q(author__username__icontains=search_text)
        )
        cate = BlogCategory.objects.filter(name=search_text)
        if cate.count() > 0:
            blogs = cate[0].blog.all()
            query_list = query_list | blogs
        query_list = query_list.distinct()

    else:
        query_list = []
    paginator = Paginator(query_list, blog_show_per_page)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        blogs = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        blogs = paginator.page(page)

    for blog in blogs:
        blog.publish_time = timezone.localtime(blog.publish_time)

    page_list = getPageList(page, paginator.num_pages)

    context = {}
    context['blogs'] = blogs
    context['page_list'] = page_list
    context['title'] = search_text
    return render(request, "blogs/index.html", context)
