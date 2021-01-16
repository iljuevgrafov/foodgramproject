from rest_framework import serializers
from recipes.models import Ingredient

class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient