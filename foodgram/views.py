from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from recipes.models import Recipe, Favorite, Follow, Tag, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model
from recipes.forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

def getIngredientsFromPOST(request):
    raw_data = request.POST.dict()
    ingredient_titles = [raw_data[key] for key in raw_data if 'nameIngredient' in key]
    ingredient_value = [raw_data[key] for key in raw_data if 'valueIngredient' in key]
    ingredient_unit = [raw_data[key] for key in raw_data if 'unitsIngredient' in key]
    ingredients = zip(ingredient_titles,ingredient_value, ingredient_unit)
    # print(items)

    # ingredients = {}
    # for title, value in items:
    #     ingredients[title] = value

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
    username = request.user
    ingredients = zip(recipe.ingredients.all(), recipe.recipeingredient_set.all())
    return render(request, 'singlePage.html', {'recipe' : recipe, 'username' : username, 'ingredients' : ingredients})


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
        form = RecipeForm(request.POST, instance=recipe)
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
            print(ingredients)
            print(tags)
            return render(request, 'formChangeRecipe.html', {'form': form, 'recipe':recipe, 'tags':tags, 'ingredients':ingredients})
            
        return redirect('recipe', recipe_id=recipe.id)

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
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page, 'paginator': paginator})

def buing_list(request):
    pass
