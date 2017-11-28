from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^minesweeper/$', views.minesweeper, name="minesweeper"),

    url(r'^ajax/minesweeper/post_score/$', views.mine_score_post, name="mine_score_post"),
    url(r'^ajax/minesweeper/get_score/$', views.mine_score_get, name="mine_score_get"),
]
