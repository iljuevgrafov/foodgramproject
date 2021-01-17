from django.contrib import admin
from django.urls import path
from . import views as foodgramviews
from users import views as usersviews
from api import views as apiviews

from django.urls import include, path, re_path
from django.contrib.flatpages import views
from django.views.generic import RedirectView
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ingredients/', apiviews.Ingredients.as_view()),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("signup/", usersviews.SignUp.as_view(), name="signup"),
    path('new_recipe/', foodgramviews.new_recipe, name="new_recipe"),
    path('purchases', apiviews.Purchases.as_view()),
    path('purchases/<int:recipe_id>', apiviews.Purchases.as_view()),
    path('favorite/', foodgramviews.favorite, name="favorite"),
    path('favorites', apiviews.Favorites.as_view()),
    path('favorites/<int:recipe_id>', apiviews.Favorites.as_view()),
    path('follow/', foodgramviews.follow, name="follow"),
    path('subscriptions', apiviews.Subscription.as_view()),
    path('subscriptions/<str:author_name>', apiviews.Subscription.as_view()),
    path('recipe/<int:recipe_id>/', foodgramviews.recipe, name="recipe"),
    path('change_recipe/<int:recipe_id>/', foodgramviews.change_recipe, name="change_recipe"),
    path('delete_recipe/<int:recipe_id>/', foodgramviews.delete_recipe, name="delete_recipe"),
    path("shop_list/", foodgramviews.shop_list, name='shop_list'),
    path("download_shop_list/", foodgramviews.download_shop_list, name='download_shop_list'),
    path('<str:author>/', foodgramviews.authors_recipes, name="authors_recipes"),
    path("",foodgramviews.index, name='index'),
]   