from typing import List, Dict, Any
from rest_framework import serializers
from django.db.models.query import QuerySet
from letsCook.recipes.models import *
from letsCook.recipes.services import recipe_service
        
class IngredientSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField(min_length=1, required=True)

    class Meta:
        model: type = Ingredient
        fields: List[str] = ['url', 'name']

class StepSerializer(serializers.HyperlinkedModelSerializer):

    description = serializers.CharField(min_length=1, required=True)

    class Meta:
        model: type = Step
        fields: List[str] = ['url', 'description']

class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):

    quantity = serializers.IntegerField(min_value=1, required=True)
    ingredient: IngredientSerializer = serializers.HyperlinkedRelatedField(
        view_name = 'ingredient-detail',
        queryset = Ingredient.objects.all()
    )

    class Meta:
        model: type = RecipeIngredient
        fields: List[str] = ['ingredient', 'quantity']

class RecipeStepSerializer(serializers.HyperlinkedModelSerializer):

    order = serializers.IntegerField(min_value=1, required=True)
    step: StepSerializer = serializers.HyperlinkedRelatedField(
        view_name = 'step-detail',
        queryset = Step.objects.all()
    )

    class Meta:
        model: type = RecipeStep
        fields: List[str] = ['step', 'order']

class RecipeSerializer(serializers.HyperlinkedModelSerializer):

    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(min_length=1, required=True)
    cooking_time = serializers.IntegerField(min_value=1, required=True)
    servings = serializers.IntegerField(min_value=1, required=True)
    category = serializers.ChoiceField(choices=RecipeCategory.choices)
    diet = serializers.ChoiceField(choices=DietCategory.choices)
    ingredients: RecipeIngredientSerializer = RecipeIngredientSerializer(many=True, source='recipe_ingredients')
    steps: RecipeStepSerializer = StepSerializer(many=True, source='recipe_steps')

    class Meta:
        model: type = Recipe
        fields: List[str] = ['url', 'title', 'description', 'cooking_time',
                  'servings', 'category', 'diet', 'ingredients', 'steps']
        
    def create(self, validated_data: Dict[str, Any]) -> Recipe:
        return recipe_service.RecipeService.create_recipe_if_not_exists(validated_data)