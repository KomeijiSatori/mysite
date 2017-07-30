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

    # avatar urls
    url(r'^profile/avatar/', include('avatar.urls')),

    # ajax urls
    url(r'ajax/blog/posts', views.get_blog_posts_content, name="user_blog_posts"),
    url(r'ajax/comment/posts', views.get_comments_posts_content, name="user_comment_posts"),
    url(r'ajax/comment/received', views.get_comments_received_content, name="user_comment_received"),

    # make included account url at the bottom
    url(r'', include('registration.backends.default.urls')),
]
