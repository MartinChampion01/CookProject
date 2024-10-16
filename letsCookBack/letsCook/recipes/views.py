from django.shortcuts import render
from rest_framework import viewsets
from letsCook.recipes.models import Recipe, Ingredient, Step
from letsCook.recipes.serializers import RecipeSerializer, IngredientSerializer, StepSerializer

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # Vous pouvez personnaliser les méthodes create, update, etc., ici si nécessaire

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer