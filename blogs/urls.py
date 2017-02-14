from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^page/(?P<page>[0-9]+)/$', views.index, name="page_show"),
]
