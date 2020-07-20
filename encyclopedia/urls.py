from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index"),  
    path("wiki/search", views.show_search, name="search"), 
    path("wiki/new", views.show_new, name="new"),
    path("wiki/edit/<str:entry>/", views.show_edit, name="edit"),  
    path("wiki/random", views.show_random, name="random"),
    path("wiki/<str:entry>", views.show_entry, name="entry")   
]