from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^archive/(?P<blog_id>[0-9]+)/$', views.archive, name="archive"),
    url(r'^post/$', views.post, name="post"),
    url(r'^search/$', views.search, name="search"),
    url(r'^addComment/(?P<blog_id>[0-9]+)/$', views.addComment, name="addComment"),
    url(r'^addNestedComment/(?P<comment_id>[0-9]+)/$', views.addNestedComment, name="addNestedComment"),
    url(r'^category/(?P<category>.+)/$', views.categoryBlogs, name="category"),
]
