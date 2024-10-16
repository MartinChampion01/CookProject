from typing import List, Dict
from django.core.exceptions import ValidationError
from ..models import Step

class StepService:

    @staticmethod
    def create_step_if_not_exist(steps: List[Dict[str, str]]):
        steps_descritpion: List[str] = [step['descrition'] for step in steps]

        existing_steps: List[Step] = Step.objects.filter(description__in=steps_descritpion)
        existing_descriptions: set[str] = set(step.description for step in existing_steps)

        steps_to_create: List[Step] = []
        for description in steps_descritpion:
            if description not in existing_descriptions:
                step = Step(description=description)

            try:
                # Appel de clean() pour valider l'étape avant l'ajout à la liste
                step.clean()
                steps_to_create.append(step)
            except ValidationError as e:
                # Gérer les erreurs de validation (vous pouvez les logger ou lever une exception)
                print(f"Erreur de validation pour l'étape '{description}': {e}")
        Step.objects.bulk_create(steps_to_create)