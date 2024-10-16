from django.db import models

class RecipeCategory(models.IntegerChoices):
    STARTER = 1, 'Starter'
    MAIN_COURSE = 2, 'Main Course'
    DESSERT = 3, 'Dessert'
    COCKTAIL = 4, 'Cocktail'

class DietCategory(models.IntegerChoices):
    MEAT = 1, 'Meat based meal'
    VEGETARIAN = 2, 'Vegetarian'
    VEGAN = 3, 'Vegan'

