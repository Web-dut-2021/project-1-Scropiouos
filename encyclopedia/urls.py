from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/",views.randoms,name="randoms"),
    path("create/",views.create,name="create"),
    path("edit/",views.edit,name="edit"),
    path("search/",views.search,name="search"),
    path("<str:title>",views.detail,name="detail"),
]
