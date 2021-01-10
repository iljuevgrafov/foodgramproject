import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from recipes.models import Recipe, Favorite, Follow
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
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
        
@method_decorator(csrf_exempt, name='dispatch')
class Subscription(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        authorid = req_.get("id", None)
        author = get_object_or_404(User, id=authorid)
        print(author)
        if author is not None and author != request.user:
            obj, created = Follow.objects.get_or_create(user=request.user, author=author)

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return JsonResponse({"success": True})

# Create your views here.

