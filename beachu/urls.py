from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("insert", views.insertnew, name="insert"),
    path("establist", views.establist, name="establist"),
    path("estabfav", views.estabfav, name="estabfav"),
    path("estabook", views.estabook, name="estabook"),
    path("estabsearch", views.estabsearch, name="estabsearch"),
    path("estabpage/<int:estabid>", views.estabpage, name="estabpage"),
    path("addfav", views.addfav, name="addfav"),
    path("remfav", views.remfav, name="remfav"),
    path("incumb", views.increaseUmb, name="incumb"),
    path("decumb", views.decreaseUmb, name="decumb"),
    path("addcomment", views.addcomment, name="addcomment"),
    path("editcomment", views.editcomment, name="editcomment"),
    path("addbook", views.addbook, name="addbook"),
    path("rembook", views.rembook, name="rembook")
]