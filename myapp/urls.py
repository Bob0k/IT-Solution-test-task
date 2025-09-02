from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("index/", views.index, name="index"),
    path("index/like/", views.like_quote, name="like"),
    path("index/dislike/", views.dislike_quote, name="dislike"),
    path("add/", views.add_quote, name="add"),
    path("board/", views.board, name="board")
]
