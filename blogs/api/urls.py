from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.BlogListView.as_view(), name="blog_list"),
    url(r'^archive/(?P<pk>\d+)/$', views.BlogDetailView.as_view(), name="blog_detail"),
    url(r'^archive/(?P<pk>\d+)/edit/$', views.BlogUpdateView.as_view(), name="blog_update"),
    url(r'^post/$', views.BlogCreateView.as_view(), name="blog_post"),
    url(r'^search/$', views.BlogSearchView.as_view(), name="search"),
    url(r'^archive/(?P<pk>\d+)/comment/$', views.BlogCommentView.as_view(), name="blog_comment_list"),
    url(r'^comment/(?P<pk>\d+)/$', views.CommentListView.as_view(), name="comment_list"),
    url(r'^addComment/(?P<blog_id>[0-9]+)/$', views.CommentCreateView.as_view(), name="comment_post"),
    url(r'^addNestedComment/(?P<comment_id>[0-9]+)/$', views.NestedCommentCreateView.as_view(),
        name="nested_comment_post"),
    url(r'^comment/(?P<pk>\d+)/edit/$', views.CommentUpdateView.as_view(), name="comment_update"),
    url(r'^category/(?P<name>.+)/$', views.BlogCategoryListView.as_view(), name="category_list"),
]
