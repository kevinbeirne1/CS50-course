from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create", views.create_listing_view, name="create"),


    path("active", views.active_listings_view, name="active"),
    path("watchlist/<int:user_id>", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>", views.specific_category_view, name="specific_category"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    # path("listing/<str:listing_id>", views.error, name="error"),

]
