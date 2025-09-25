from django.urls import path
from django.shortcuts import render, redirect
from . import ctgs, news


def index(request):
    if request.user.is_anonymous or request.user.user_type != 1 or not request.user.is_staff:
        return redirect("home")

    return render(request, "dashboard/index.html")



urlpatterns = [
    path("", index, name='dashboard-home'),

    # ctgs
    path("ctg/list/", ctgs.list, name='ctg-list'),
    path("ctg/add/", ctgs.add_ctg, name='ctg-add'),
    path("ctg/edit/<int:pk>/", ctgs.add_ctg, name='ctg-edit'),
    path("ctg/delete/<int:pk>/", ctgs.delete, name='ctg-delete'),

    # news
    path("news/list/", news.list_or_one, name='news-list'),
    path("news/detail/<int:pk>/", news.list_or_one, name='news-detail'),
    path("news/add/", news.add_edit, name='news-add'),
    path("news/edit/<int:pk>/", news.add_edit, name='news-edit'),
    path("news/delete/<int:pk>/", news.delete, name='news-delete'),

]





