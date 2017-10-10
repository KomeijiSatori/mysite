from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^archive/(?P<blog_id>[0-9]+)/$', views.archive, name="archive"),
    url(r'^archive/(?P<blog_id>[0-9]+)/edit/$', views.blog_update, name="blog_update"),
    url(r'^post/$', views.post, name="post"),
    url(r'^search/$', views.search, name="search"),
    url(r'^comment/(?P<comment_id>[0-9]+)/$', views.getComment, name="getComment"),
    url(r'^addComment/(?P<blog_id>[0-9]+)/$', views.addComment, name="addComment"),
    url(r'^addNestedComment/(?P<comment_id>[0-9]+)/$', views.addNestedComment, name="addNestedComment"),
    url(r'^updateComment/(?P<comment_id>[0-9]+)/$', views.updateComment, name="updateComment"),
    url(r'^category/(?P<category>.+)/$', views.categoryBlogs, name="category"),

    url(r'^ajax/saveDraft/$', views.saveDraft, name="saveDraft"),
    url(r'^ajax/removeDraft/$', views.removeDraft, name="removeDraft"),
]
