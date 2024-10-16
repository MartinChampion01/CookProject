from typing import Any, List, Dict
from django.core.exceptions import ValidationError
from ..models import Ingredient, Recipe, RecipeIngredient

class RecipeIngredientService:

    @staticmethod
    def create_recipe_ingredient_relation(recipe: Recipe, recipe_ingredients: List[Dict[str, Any]]):

        ingredient_names: List[str] = [recipe_ingredient['name'] for recipe_ingredient in recipe_ingredients]
        ingredients: List[Ingredient] = Ingredient.objects.filter(name__in=ingredient_names)

        recipe_ingredient_objs: List[RecipeIngredient] = []
        for recipe_ingredient in recipe_ingredients:

            # Parcours un générateur qui renvoie l'ingrédient renvoyé par la base correspondant à celui dans l'objet reçu du client
            ingredient: Ingredient = next((ing for ing in ingredients if ing.name == recipe_ingredient['name']), None)
            if ingredient:
                recipe_ingredient_obj: RecipeIngredient  = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=recipe_ingredient['quantity']
                )

                try:
                # Appel de clean() pour valider l'étape avant l'ajout à la liste
                    recipe_ingredient_obj.clean()
                    recipe_ingredient_objs.append(recipe_ingredient_obj)
                except ValidationError as e:
                # Gérer les erreurs de validation (vous pouvez les logger ou lever une exception)
                    print(f"Erreur de validation pour la relation entre '{recipe}' et l'ingrédient '{ingredient}' : {e}")

        RecipeIngredient.objects.bulk_create(recipe_ingredient_objs)