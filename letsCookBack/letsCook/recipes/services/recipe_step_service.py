from typing import Any, List, Dict
from django.core.exceptions import ValidationError
from ..models import Step, Recipe, RecipeStep

class recipe_stepservice:

    @staticmethod
    def create_recipe_step_relation(recipe: Recipe, recipe_steps: List[Dict[str, Any]]):
        step_descriptions: List[str] = [step['description'] for step in recipe_steps]
        steps: List[Step] = Step.objects.filter(description__in=step_descriptions)

        recipe_step_objs: List[RecipeStep] = []
        for recipe_step in recipe_steps:
            step = next((st for st in steps if st.description == recipe_step['description']), None)
            if step:
                recipe_step_obj: RecipeStep = RecipeStep(
                    recipe = recipe,
                    step = step,
                    order = recipe_step['order']
                )

                try:
                # Appel de clean() pour valider l'étape avant l'ajout à la liste
                    recipe_step_obj.clean()
                    recipe_step_objs.append(recipe_step_obj)
                except ValidationError as e:
                # Gérer les erreurs de validation (vous pouvez les logger ou lever une exception)
                    print(f"Erreur de validation pour la relation entre '{recipe}' et l'ingrédient '{step}' : {e}")

        RecipeStep.objects.bulk_create(recipe_step_objs)