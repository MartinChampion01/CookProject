from typing import List, Dict
from django.core.exceptions import ValidationError
from ..models import Ingredient

class IngredientService:

    @staticmethod
    def create_ingredient_if_not_exists(ingredients: List[Dict[str, str]]):
        # Récupération des noms des ingrédients
        ingredient_names: List[str] = [ingredient['name'] for ingredient in ingredients]

        # Récupération des noms des ingrédients existants déjà en BDD
        existing_ingredients: List[Ingredient] = Ingredient.objects.filter(name__in=ingredient_names)
        existing_names: set[str] = set(ingredient.name for ingredient in existing_ingredients)

        # Création des ingrédients n'existant pas déjà en BDD
        ingredients_to_create: List[Ingredient] = []
        for name in ingredient_names:
            if name not in existing_names:
                ingredient = Ingredient(name=name)

            try:
                # Appel de clean() pour valider l'ingrédient avant l'ajout à la liste
                ingredient.clean()
                ingredients_to_create.append(ingredient)
            except ValidationError as e:
                # Gérer les erreurs de validation (vous pouvez les logger ou lever une exception)
                print(f"Erreur de validation pour l'ingrédient '{name}': {e}")

        Ingredient.objects.bulk_create(ingredients_to_create)