from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.forms.models import model_to_dict
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.urls import reverse

from .models import Blog, BlogCategory, Comment, BlogDraft
from accounts.models import Profile
from .forms import BlogForm, BlogCommentForm
from .service import BlogService
from accounts.service import FollowService

# Create your views here.


def index(request):
    context = {}
    blog_list = Blog.objects.all().order_by('-publish_time')
    page = request.GET.get('page')
    blogs, page_list = BlogService.get_paginated_items(blog_list, page)
    context['blogs'] = blogs
    context['page_list'] = page_list
    context['title'] = _("Blogs")
    return render(request, "blogs/index.html", context)


def archive(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    profile = get_object_or_404(Profile, user=blog.author)
    comment_form = BlogCommentForm()
    comments = Comment.objects.filter(blog=blog)
    if request.user.is_authenticated and request.user != blog.author:
        is_follow = FollowService.is_fan_star(request.user, blog.author)
    else:
        is_follow = None
    # read count plus one
    blog.read_count += 1
    blog.save()

    context = {
        "blog": blog,
        'comment_form': comment_form,
        'nodes': comments,
        'is_follow': is_follow,
        'profile': profile,
        'max_comment_level': BlogService.max_comment_level
    }
    return render(request, "blogs/detail.html", context)


@login_required
def addComment(request, blog_id):
    form = BlogCommentForm(request.POST)
    blog = get_object_or_404(Blog, id=blog_id)
    if form.is_valid():
        BlogService.create_comment_from_string(request.user, blog, form.cleaned_data.get('text'), None)
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


@login_required
def addNestedComment(request, comment_id):
    form = BlogCommentForm(request.POST)
    parent_comment = get_object_or_404(Comment, id=comment_id)
    blog = parent_comment.blog
    if form.is_valid():
        BlogService.create_comment_from_string(request.user, blog, form.cleaned_data.get('text'), parent_comment)
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


def categoryBlogs(request, category):
    cate = BlogCategory.objects.filter(name=category)

    if cate.count() > 0:
        blogs = cate[0].blog.all()
        blog_list = blogs.order_by('-publish_time')
        page = request.GET.get('page')
        blogs, page_list = BlogService.get_paginated_items(blog_list, page)
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
        category_str = form.cleaned_data.get('categories')
        title_str = form.cleaned_data.get('title')
        user = request.user
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        text_str = request.POST.get("text")

        blog = BlogService.create_blog_from_string(user, title_str, text_str, category_str)
        return HttpResponseRedirect(reverse('blogs:index'))
    # see if there is draft
    try:
        draft = BlogDraft.objects.get(author=request.user)
        blog_initial = {
            'title': draft.title,
            'text': draft.text,
            'categories': draft.category,
        }
        form = BlogForm(initial=blog_initial)
    except Exception:
        pass
    return render(request, "blogs/post.html", {"form": form, "save_draft": True})


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
        category_str = form.cleaned_data.get('categories')
        title_str = form.cleaned_data.get('title')
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        text_str = request.POST.get("text")
        blog = BlogService.update_blog_from_string(blog_id, title_str, text_str, category_str)
        return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))
    return render(request, "blogs/post.html", {"form": form, "blog": blog})


def getComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    data = model_to_dict(comment)
    return JsonResponse(data)


@login_required
def updateComment(request, comment_id):
    form = BlogCommentForm(request.POST)
    comment = get_object_or_404(Comment, id=comment_id)
    blog = comment.blog
    if not(request.user == comment.author or request.user.is_superuser):
        raise PermissionDenied
    if form.is_valid():
        comment_str = form.cleaned_data.get('text')
        comment = BlogService.update_comment_from_string(comment_id, comment_str)
    return HttpResponseRedirect(reverse('blogs:archive', args=(blog.id,)))


def search(request):
    search_text = request.GET.get('search')
    if search_text:
        paras = dict(request.GET)
        try:
            query_list = BlogService.search_blogs(**paras)
        except Exception:
            query_list = []
    else:
        query_list = []

    page = request.GET.get('page')
    blogs, page_list = BlogService.get_paginated_items(query_list, page)

    context = {}
    context['blogs'] = blogs
    context['page_list'] = page_list
    context['title'] = search_text
    return render(request, "blogs/index.html", context)


@login_required
def saveDraft(request):
    if request.is_ajax():
        data = request.POST
        title = data.get("title")
        text = data.get("text")
        category = data.get("category")
        user = request.user
        BlogService.create_blog_draft_from_string(user, title, text, category)
        return JsonResponse({"result": "success"})
    else:
        raise Http404("Page not found!")


@login_required
def removeDraft(request):
    if request.is_ajax():
        BlogDraft.objects.filter(author=request.user).delete()
        return JsonResponse({"result": "success"})
    else:
        raise Http404("Page not found!")
