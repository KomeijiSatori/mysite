from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import ProfileForm
from .models import Profile
from blogs.views import Blog, Comment
from blogs.service import BlogService

# Create your views here.


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def get_blog_posts_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        blog_list = Blog.objects.filter(author=user).order_by('-publish_time')

        page = request.GET.get('page')
        blogs, page_list = BlogService.get_paginated_items(blog_list, page)

        context = {}
        context['blogs'] = blogs
        context['page_list'] = page_list
        context['origin_ajax_url'] = request.get_full_path()

        return render(request, "accounts/blog_posts.html", context)
    else:
        raise Http404("Page not found!")


def get_comments_posts_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        comment_list = Comment.objects.filter(author=user).order_by('-publish_time')

        page = request.GET.get('page')
        comments, page_list = BlogService.get_paginated_items(comment_list, page)

        context = {}
        context['comments'] = comments
        context['page_list'] = page_list
        context['origin_ajax_url'] = request.get_full_path()

        return render(request, "accounts/comment_posts.html", context)
    else:
        raise Http404("Page not found!")


def get_comments_received_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        comment_list = Comment.objects.filter(Q(blog__author=user) | Q(parent__author=user)).distinct().order_by('-publish_time')

        page = request.GET.get('page')
        comments, page_list = BlogService.get_paginated_items(comment_list, page)
        context = {}
        context['comments'] = comments
        context['page_list'] = page_list
        context['origin_ajax_url'] = request.get_full_path()

        return render(request, "accounts/comment_received.html", context)
    else:
        raise Http404("Page not found!")


@login_required
def profile_edit(request):
    user_profile = Profile.objects.filter(user=request.user)
    if user_profile:
        user_profile = user_profile[0]
    else:
        return Http404("No such user file")

    if request.POST:
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.gender = profile.gender
            user_profile.birthday = profile.birthday
            user_profile.mobile = profile.mobile
            user_profile.residence = profile.residence
            user_profile.website = profile.website
            user_profile.microblog = profile.microblog
            user_profile.qq = profile.qq
            user_profile.wechat = profile.wechat
            user_profile.introduction = profile.introduction
            user_profile.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, "accounts/profile_edit.html", {"form": form})
