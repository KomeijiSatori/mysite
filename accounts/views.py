from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from .forms import ProfileForm
from .models import Profile, Notification
from blogs.views import Blog, Comment
from blogs.service import BlogService
from .service import FollowService, NotificationService

# Create your views here.


@login_required
def dashboard(request):
    try:
        api_key = Token.objects.get(user=request.user)
    except Exception:
        api_key = None
    return render(request, "accounts/dashboard.html", {"api_key": api_key})


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


# use notification model to handle comment receive
def get_comments_received_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        notification_list = NotificationService.get_comment_reply_notifications(user)
        comment_list = list()
        # get comment list
        for notification in notification_list:
            comment = notification.content_object
            # add related notification field
            comment.related_notification_id = notification.id
            comment.unread = notification.unread
            comment_list.append(comment)
        comment_list = sorted(comment_list, key=lambda x: x.publish_time, reverse=True)

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


@login_required
def generate_api_key(request):
    origin_token = Token.objects.filter(user=request.user)
    if len(origin_token) == 1:
        origin_token[0].delete()
    elif len(origin_token) > 1:
        raise Exception("Get token failed, Please contact the admin team")
    token = Token.objects.create(user=request.user)
    return JsonResponse({"api-key": token.key})


@login_required
def get_unread_comment_count(request):
    if request.is_ajax():
        count = NotificationService.get_unread_comment_reply_count(request.user)
        return JsonResponse({"count": count})
    else:
        raise Http404("Page not found!")


@login_required
def read_notification(request):
    if request.is_ajax():
        notification_id = request.GET.get("notification_id")
        notification = get_object_or_404(Notification, id=notification_id)
        if request.user == notification.user:
            notification.unread = False
            notification.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    else:
        raise Http404("Page not found!")


@login_required
def add_follow(request):
    if request.is_ajax():
        fan_id = request.GET.get("fan")
        star_id = request.GET.get('star')
        fan = get_object_or_404(User, id=fan_id)
        star = get_object_or_404(User, id=star_id)
        result = FollowService.add_fan_star(fan, star)
        return JsonResponse({"success": result})
    else:
        raise Http404("Page not found!")


@login_required
def delete_follow(request):
    if request.is_ajax():
        fan_id = request.GET.get("fan")
        star_id = request.GET.get('star')
        fan = get_object_or_404(User, id=fan_id)
        star = get_object_or_404(User, id=star_id)
        result = FollowService.remove_fan_star(fan, star)
        return JsonResponse({"success": result})
    else:
        raise Http404("Page not found!")


@login_required
def get_subscribe_blogs_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        notification_list = NotificationService.get_subscribe_blog_notifications(user)
        blog_list = list()
        # get blog list
        for notification in notification_list:
            blog = notification.content_object
            # add related notification field
            blog.related_notification_id = notification.id
            blog.unread = notification.unread
            blog_list.append(blog)
        blog_list = sorted(blog_list, key=lambda x: x.publish_time, reverse=True)

        page = request.GET.get('page')
        blogs, page_list = BlogService.get_paginated_items(blog_list, page)
        context = {}
        context['blogs'] = blogs
        context['page_list'] = page_list
        context['origin_ajax_url'] = request.get_full_path()

        return render(request, "accounts/blog_posts.html", context)
    else:
        raise Http404("Page not found!")


@login_required
def get_unread_subscribe_blog_count(request):
    if request.is_ajax():
        count = NotificationService.get_unread_subscribe_blog_count(request.user)
        return JsonResponse({"count": count})
    else:
        raise Http404("Page not found!")


@login_required
def get_at_content(request):
    if request.is_ajax():
        user_id = request.GET.get("user_id")
        user = get_object_or_404(User, id=user_id)
        at_blog_notification_list = NotificationService.get_at_blog_notifications(user)
        at_comment_notification_list = NotificationService.get_at_comment_notifications(user)

        at_notifications = []
        for ind in range(len(at_blog_notification_list)):
            at_blog_notification_list[ind].src = "blog"
            at_notifications.append(at_blog_notification_list[ind])

        for ind in range(len(at_comment_notification_list)):
            at_comment_notification_list[ind].src = "comment"
            at_notifications.append(at_comment_notification_list[ind])

        at_list = list()
        # get obj list
        for notification in at_notifications:
            obj = notification.content_object
            # add related notification field
            obj.related_notification_id = notification.id
            obj.unread = notification.unread
            obj.src = notification.src
            at_list.append(obj)

        at_list = sorted(at_list, key=lambda x: x.publish_time, reverse=True)

        page = request.GET.get('page')
        items, page_list = BlogService.get_paginated_items(at_list, page)
        context = {}
        context['items'] = items
        context['page_list'] = page_list
        context['origin_ajax_url'] = request.get_full_path()

        return render(request, "accounts/at_received.html", context)
    else:
        raise Http404("Page not found!")


@login_required
def get_unread_at_count(request):
    if request.is_ajax():
        count = NotificationService.get_unread_at_count(request.user)
        return JsonResponse({"count": count})
    else:
        raise Http404("Page not found!")


@login_required
def get_unread_notification_count(request):
    if request.is_ajax():
        count = NotificationService.get_unread_notification_count(request.user)
        return JsonResponse({"count": count})
    else:
        raise Http404("Page not found!")
