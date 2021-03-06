import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from recipes.models import Recipe, Favorite, Follow, Ingredient, ShopList
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import IngredientsSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model() 

class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id = recipe_id)
            obj, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Favorite, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})
        
# @method_decorator(csrf_exempt, name='dispatch')
class Subscription(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        authorid = req_.get("id", None)
        author = get_object_or_404(User, id=authorid)
        if author is not None and author != request.user:
            obj, created = Follow.objects.get_or_create(user=request.user, author=author)

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_name):
        author = get_object_or_404(User, username=author_name)
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return JsonResponse({"success": True})

class Purchases(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        if recipe is not None:
            shop_list, obj = ShopList.objects.get_or_create(user=request.user)
            if recipe not in shop_list.recipes.all():
                shop_list.recipes.add(recipe)
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        print(recipe_id)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if recipe is not None:
            shop_list = ShopList.objects.get(user=request.user)
            print(shop_list)
            shop_list.recipes.through.objects.get(recipe=recipe).delete()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=404)

class Ingredients(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',] 


        

