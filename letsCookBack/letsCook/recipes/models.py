from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator
from letsCook.recipes.enums import RecipeCategory, DietCategory

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100,
                            validators=[MaxLengthValidator(100),
                                        MinLengthValidator(1)])

    def __str__(self):
        return self.name

class Step(models.Model):
    description = models.TextField(validators=[MinLengthValidator(1)])

    def __str__(self):
        return self.description
    

class Recipe(models.Model):
    title = models.CharField(max_length=100,
                             validators=[MaxLengthValidator(100),
                                         MinLengthValidator(1)])
    description = models.TextField(validators=[MinLengthValidator(1)])
    cooking_time = models.PositiveBigIntegerField(help_text="Temps de cuisson en minutes", validators=[MinValueValidator(1)])
    servings = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    category = models.IntegerField(
        choices=RecipeCategory.choices,
        default=RecipeCategory.MAIN_COURSE
    )
    diet = models.IntegerField(
        choices=DietCategory.choices,
        default=DietCategory.MEAT
    )

    # Relation Many-to-Many avec Ingredient via RecipeIngredient (table intermédiaire)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    steps = models.ManyToManyField(Step, through='RecipeStep')

    def __str__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_recipes', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, help_text="Quantité avec unité de mesure si besoin", validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('recipe', 'ingredient')  # Empêche la duplication d'ingrédients pour une même recette
    
    def __str__(self):
        return f"{self.quantity} de {self.ingredient.name} pour {self.recipe.title}."
    
class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps_recipes', on_delete=models.CASCADE)
    step = models.ForeignKey(Step, related_name='recipe_steps', on_delete=models.CASCADE)
    order = models.PositiveBigIntegerField(help_text="position de l'étape dans la recette", validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('recipe', 'step')  # Empêche la duplication d'étapes pour une même recette
    
    def __str__(self):
        return f"Etape numéro {self.order} pour la recette : {self.recipe} : {self.step}."