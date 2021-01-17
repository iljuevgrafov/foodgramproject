from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from recipes.models import Recipe, Favorite, Follow, Tag, Ingredient, RecipeIngredient, ShopList
from django.contrib.auth import get_user_model
from recipes.forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import csv
from django.http import HttpResponse

User = get_user_model()

def getIngredientsFromPOST(request):
    raw_data = request.POST.dict()
    ingredient_titles = [raw_data[key] for key in raw_data if 'nameIngredient' in key]
    ingredient_value = [raw_data[key] for key in raw_data if 'valueIngredient' in key]
    ingredient_unit = [raw_data[key] for key in raw_data if 'unitsIngredient' in key]
    ingredients = zip(ingredient_titles,ingredient_value, ingredient_unit)
    return ingredients

def getTagsFromPOST(request):
    tags_from_POST = []
    for tag in 'breakfast','lunch','dinner':
        if tag in request.POST.dict():
            tags_from_POST.append(tag)
    tags = [Tag.objects.get(en_title=tag).id for tag in tags_from_POST]
    return tags

def index(request):
    tags = request.GET.get('tag') or None
    if tags is not None:
        tags = list(map(str, request.GET.get('tag').split(',')))
        recipe_list = Recipe.objects.filter(tag__en_title__in=tags)
        paginator = Paginator(recipe_list, 6)   
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'indexAuth.html', {'page': page, 'paginator': paginator})
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)   
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'indexAuth.html', {'page': page, 'paginator': paginator})

def authors_recipes(request, author):
    author = get_object_or_404(User, username=author)
    recipe_list = author.recipes.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'authorRecipe.html', {'page': page, 'paginator': paginator, 'author' : author})

def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    in_favorites = None
    if str(request.user) != 'AnonymousUser':
        username = request.user
        in_favorites = Favorite.objects.filter(user=username, recipe=recipe).first()
    ingredients = zip(recipe.ingredients.all(), recipe.recipeingredient_set.all())
    return render(request, 'singlePage.html', {'recipe' : recipe, 'ingredients' : ingredients, 'in_favorites': in_favorites})


@login_required
def new_recipe(request):
    if request.method == 'POST':

        form = RecipeForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            
            ingredients = getIngredientsFromPOST(request)
            ingredients_ids = []
            
            for title, value, unit in ingredients:
                ingredientobj = Ingredient.objects.get(title=title)
                RecipeIngredient.objects.create(ingredient=ingredientobj, recipe=new_recipe, amount=value)
                ingredients_ids.append(ingredientobj.id)

            for ingredient_id in ingredients_ids:
                new_recipe.ingredients.add(ingredient_id)
                
            tags = getTagsFromPOST(request)    
            new_recipe.tag.set(tags)
            new_recipe.save()

            return redirect('recipe', recipe_id=new_recipe.id)
        else:
            return render(request, 'new_recipe.html', {'form': form})
    else:
        form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})

@login_required
def change_recipe(request, recipe_id):
    if request.method == 'GET':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        tags = [tag.en_title for tag in recipe.tag.all()]

        titles = [title['title'] for title in recipe.ingredients.values('title')]
        dimensions = [dimension['dimension'] for dimension in recipe.ingredients.values('dimension')]
        amounts = [amount['amount'] for amount in recipe.recipeingredient_set.values('amount')]
        ingredients = zip(titles, amounts, dimensions)

        form = RecipeForm(instance=recipe)
        return render(request, 'formChangeRecipe.html', {'form': form, 'recipe':recipe, 'tags':tags, 'ingredients':ingredients})

    if request.method == 'POST':
        tags = getTagsFromPOST(request)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        print('files', request.FILES)
        form = RecipeForm(request.POST, instance=recipe, files=request.FILES or None)
        ingredients = getIngredientsFromPOST(request)
        
        if form.is_valid():
            changed_recipe = form.save(commit=False)
            RecipeIngredient.objects.filter(recipe=changed_recipe).delete()
            ingredients_ids = []

            for title, value, unit in ingredients:
                ingredientobj = Ingredient.objects.get(title=title)
                RecipeIngredient.objects.create(ingredient=ingredientobj, recipe=changed_recipe, amount=value)
                ingredients_ids.append(ingredientobj.id)

            for ingredient_id in ingredients_ids:
                changed_recipe.ingredients.add(ingredient_id)
                
            tags = getTagsFromPOST(request)    
            changed_recipe.tag.set(tags)
            changed_recipe.save()

        else:
            return render(request, 'formChangeRecipe.html', {'form': form, 'recipe':recipe, 'tags':tags, 'ingredients':ingredients})
            
        return redirect('recipe', recipe_id=recipe.id)

@login_required
def delete_recipe(request, recipe_id): 
    if request.method == 'GET':
        return render(request, 'deletionConfirm.html', {'recipe_id':recipe_id})

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipe', recipe_id=recipe.id)
    recipe.delete()
    return redirect('index')

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
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page, 'paginator': paginator})

def shop_list(request):
    shop_list, obj = ShopList.objects.get_or_create(user=request.user)
    print(shop_list)
    return render(request, 'shopList.html', {'shop_list': shop_list})

def download_shop_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.txt"'
    
    user = User.objects.get(username=request.user)
    recipes = user.shoplist.recipes.all()
    ingredients_to_buy = RecipeIngredient.objects.filter(recipe__in=recipes).values('ingredient__title').annotate(summa = Sum('amount'))
    writer = csv.writer(response)
    writer.writerow(['Дорогой %s, это перечень ингридиентов для приготовления рецептов'% user.username])
    
    writer.writerow(['Ингридиент', 'Количество', 'Еденица измерения'])
    for ingredient in ingredients_to_buy:
        new_line = [ingredient['ingredient__title'], str(ingredient['summa']), Ingredient.objects.get(title=ingredient['ingredient__title']).dimension]
        writer.writerow(new_line)
    writer.writerow([])
    writer.writerow(['С любовью, Ваш foodgramproject'])
    return response

