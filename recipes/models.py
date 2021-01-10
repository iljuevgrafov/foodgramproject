from django.db import models
# from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingridient(models.Model):
    title = models.CharField(max_length=50,null=True, verbose_name='Название')
    dimension = models.CharField(max_length=10,null=True, verbose_name='Еденица измерения')

    def __str__(self):
        return self.title

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='static/images/recipes/', blank=True, null=True)
    text = models.TextField(null=True)
    ingridients = models.ManyToManyField(Ingridient, through='RecipeIngridient') 
    tag = models.ManyToManyField('Tag')
    preparing_time = models.PositiveSmallIntegerField(default=0, null=True)

    def __str__(self):
        return self.title

class RecipeIngridient(models.Model):
    ingridient = models.ForeignKey(Ingridient, on_delete = models.CASCADE, default = '0')
    amount = models.PositiveSmallIntegerField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE, default = '0')

    def __str__(self):
        return str(self.ingridient)
    
class Tag(models.Model):
    title = models.CharField(max_length= 100)

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

class BuingList(models.Model):
    user = models.ForeignKey(User, related_name='buinglists', on_delete=models.CASCADE)
    items = models.ManyToManyField(RecipeIngridient)

    

# Create your models here.
