
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("page/<int:page_nr>", views.index, name="page"),
    path("edit", views.edit, name="edit"), 
    path("addlike", views.addlike, name="addlike"), 
    path("remlike", views.remlike, name="remlike"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/follow", views.follow, name="follow"),
    path("profile/unfollow", views.unfollow, name="unfollow")
]
