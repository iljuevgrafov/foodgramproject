from django.forms import ModelForm, Textarea
from .models import Recipe
from django import forms

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'text', 'preparing_time', 'image')
        labels = {
            "text": "Текст",
            'image': 'Изображение',
            "preparing_time" : "Время приготовления",
            "text" : "Способ приготовления"
        }
        help_texts = {
            "title": "Введите здесь название своего рецепта",
            "group": "Выберете группу к которой относится пост",
            "preparing_time" : "Укажите время приготовления блюда",
            "text" : "Опишите способ приготовления"
        }