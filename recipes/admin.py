from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient, Tag, Favorite, Follow

# class RecipeIngridientInline(admin.StackedInline):
#     model = RecipeIngridient
#     extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "image", "text", "preparing_time")
    # inlines = (RecipeIngridientInline,)

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("ingredient","amount", "recipe")
    # inlines = (RecipeIngridientInline,)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    # inlines = (RecipeIngridientInline,)

class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)

# class BuingListAdmin(admin.ModelAdmin):
#     list_display = ("user", )

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")

# Register your models here.

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(BuingList, BuingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)