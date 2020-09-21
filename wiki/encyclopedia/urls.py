from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.editpage, name="editpage"),
    path("wiki/<str:entry>", views.title, name="page")    
]
