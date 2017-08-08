from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.BlogListView.as_view(), name="list"),
    url(r'^archive/(?P<pk>\d+)/$', views.BlogDetailView.as_view(), name="detail"),
    url(r'^archive/(?P<pk>\d+)/edit/$', views.BlogUpdateView.as_view(), name="blog_update"),
    url(r'^post/$', views.BlogCreateView.as_view(), name="post"),
    # url(r'^search/$', views.search, name="search"),
    # url(r'^comment/(?P<comment_id>[0-9]+)/$', views.getComment, name="getComment"),
    # url(r'^addComment/(?P<blog_id>[0-9]+)/$', views.addComment, name="addComment"),
    # url(r'^addNestedComment/(?P<comment_id>[0-9]+)/$', views.addNestedComment, name="addNestedComment"),
    # url(r'^updateComment/(?P<comment_id>[0-9]+)/$', views.updateComment, name="updateComment"),
    # url(r'^category/(?P<category>.+)/$', views.categoryBlogs, name="category"),
]
