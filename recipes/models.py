from django.db import models
# from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    title = models.CharField(max_length=50,null=True, verbose_name='Название')
    dimension = models.CharField(max_length=10,null=True, verbose_name='Еденица измерения')

    def __str__(self):
        return self.title

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='static/images/recipes/', blank=True, null=True)
    text = models.TextField(null=True)
    ingredients = models.ManyToManyField(Ingredient, through='recipeingredient') 
    tag = models.ManyToManyField('Tag')
    preparing_time = models.PositiveSmallIntegerField(default=0, null=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, default = '0')
    amount = models.PositiveSmallIntegerField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE, default = '0')
    

    def __str__(self):
        return str(self.ingredient)
    
class Tag(models.Model):
    title = models.CharField(max_length=100)
    en_title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")   # кто подписан
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")  # на кого подписан

    class Meta:
        unique_together = ("user", "author",)

class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='hasinfavorites', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='favorites',on_delete=models.CASCADE)


class ShopList(models.Model):
    user = models.OneToOneField(User, related_name='shoplist', on_delete=models.CASCADE, unique=True)
    recipes = models.ManyToManyField(Recipe, related_name='inshoplist')
