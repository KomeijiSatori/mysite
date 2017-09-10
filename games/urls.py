from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^minesweeper/$', views.minesweeper, name="minesweeper"),
]
