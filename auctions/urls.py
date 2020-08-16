from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),    
    path("create", views.create_listing, name="create"),   
    path("categories", views.show_categories, name="categories"), 
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("listing/<int:item>", views.show_listing, name="listing"),
    path("<str:category>", views.show_cat_listings, name="category")
]