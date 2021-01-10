from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from recipes.models import Recipe, Favorite, Follow
from django.contrib.auth import get_user_model
from recipes.forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()

def index(request):
    #recipe_list = Recipe.objects.order_by('-pub_date').all()
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'indexAuth.html', {'page': page, 'paginator': paginator})

def authors_recipes(request, author):
    #recipe_list = Recipe.objects.order_by('-pub_date').all()
    author = get_object_or_404(User, username=author)
    recipe_list = author.recipes.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'authorRecipe.html', {'page': page, 'paginator': paginator, 'author' : author})

def recipe(request, recipe_id):
    # def post_view(request, username, post_id):
    # user = get_object_or_404(User, username=author)
    # count = user.posts.all().count
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    username = request.user
    # form = CommentForm()
    return render(request, 'singlePage.html', {'recipe' : recipe, 'username' : username})

@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


@csrf_exempt
def purchases(request):
    return render(request, 'new_recipe.html')

def favorite(request):
    favorites_pks = Favorite.objects.filter(user=request.user).values('recipe')
    favorites = Recipe.objects.filter(pk__in=favorites_pks).all()
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {'page': page, 'paginator': paginator})

def follow(request):
    follows = Follow.objects.filter(user=request.user).values('author')
    authors = User.objects.filter(id__in=follows)
    following = {}
    for author in authors:
        recipes= Recipe.objects.filter(author=author)   
        following[author]= recipes
    print(following)
    paginator = Paginator(following, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page, 'paginator': paginator})

# def profile(request, username):
#     user = get_object_or_404(User, username=username)
#     posts = user.posts.all()
#     following = request.user.is_authenticated and Follow.objects.filter(
#         user=request.user, author=user).exists()

#     paginator = Paginator(posts, 5)

#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)

#     return render(request, 'profile.html', {'page': page, 'paginator': paginator, 'author': user, 'following': following})