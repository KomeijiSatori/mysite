from django.conf.urls import url, include
from . import views

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail

urlpatterns = [
    # modify default django auth url
    url(r'^register/$', RegistrationViewUniqueEmail.as_view(),
        name='registration_register'),
    url(r'^password/reset/$', auth_views.password_reset,
        {
            'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
            'html_email_template_name': 'registration/password_reset_email.html',
        }, name='auth_password_reset'),

    # other profile urls
    url(r'^profile/$', views.dashboard, name="dashboard"),
    url(r'^profile/edit/$', views.profile_edit, name="profile_edit"),
    url(r'^profile/api_key/generate/$', views.generate_api_key, name="api_key_gen"),

    # avatar urls
    url(r'^profile/avatar/', include('avatar.urls')),

    # ajax urls
    url(r'ajax/blog/posts/$', views.get_blog_posts_content, name="user_blog_posts"),
    url(r'ajax/comment/posts/$', views.get_comments_posts_content, name="user_comment_posts"),
    url(r'ajax/comment/received/$', views.get_comments_received_content, name="user_comment_received"),
    url(r'ajax/account/unread_reply_count/$', views.get_unread_comment_count, name="unread_comment_count"),
    url(r'ajax/account/mark_notification/$', views.read_notification, name="read_notification"),
    url(r'ajax/account/add_follow/$', views.add_follow, name="add_follow"),
    url(r'ajax/account/delete_follow/$', views.delete_follow, name="delete_follow"),
    url(r'ajax/account/subscribe_blogs_content/$', views.get_subscribe_blogs_content, name="subscribe_blogs"),
    url(r'ajax/account/unread_subscribe_blog_count/$', views.get_unread_subscribe_blog_count,
        name="unread_subscribe_blog_count"),
    url(r'ajax/account/at_content/$', views.get_at_content, name="user_at_received"),
    url(r'ajax/account/unread_at_notification/$', views.get_unread_at_count, name="unread_at_count"),
    url(r'ajax/account/unread_notification_count/$', views.get_unread_notification_count,
        name="unread_notification_count"),

    # make included account url at the bottom
    url(r'', include('registration.backends.default.urls')),
]
