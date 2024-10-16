from typing import List, Dict, Any
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ..models import Recipe
from letsCook.recipes.services import step_service, ingredient_service, recipe_ingredient_service, recipe_step_service

class RecipeService:

    @staticmethod
    @transaction.atomic
    def create_recipe_if_not_exists(recipe_infos: Dict[str, Any]) -> Recipe:

        recipe = Recipe.objects.filter(title=recipe_infos['title']).first()

        if recipe:
            # Si la recette existe, retourner l'objet existant
            return recipe
        
        # Créer l'objet recette sans l'enregistrer
        recipe = Recipe(
            title=recipe_infos['title'],
            description=recipe_infos['description'],
            cooking_time=recipe_infos['cooking_time'],
            servings=recipe_infos['servings'],
            category=recipe_infos['category'],
            diet=recipe_infos['diet']
        )

        try:
            # Appeler clean() pour valider l'objet avant de le sauvegarder
            recipe.clean()
            # Sauvegarder la recette
            recipe.save()
        except ValidationError as e:
            # Gérer les erreurs de validation
            raise serializers.ValidationError(e)

        ingredient_infos: List[Dict[str, str]] = recipe_infos['ingredients']
        steps_infos: List[Dict[str, str]] = recipe_infos['steps']

        ingredient_service.IngredientService.create_ingredient_if_not_exists(ingredient_infos)
        step_service.StepService.create_step_if_not_exist(steps_infos)

        recipe_ingredient_service.RecipeIngredientService.create_recipe_ingredient_relation(recipe, ingredient_infos)
        recipe_step_service.RecipeStepService.create_recipe_step_relation(recipe, steps_infos)

        return recipe         
        