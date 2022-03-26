from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.forms import ModelForm


class Recipe(models.Model):

    title_text = models.CharField(max_length=200)
    ingredients_list = models.TextField()
    body_text = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now())
    edited_date = models.DateTimeField(default=datetime.now())
    parent_recipe = models.IntegerField() #reference parent recipe ID
    owner_id = models.IntegerField()  #user id from logged in user who posted
    #THINGS TO THINK ABOUT -
    #what should the picture(s) be
    #what happens when a recipe (particularly a parent recipe) is deleted
    #should a recipe be its own parent by default?

    def __str__(self):
        return self.title_text

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title_text', 'ingredients_list', 'body_text', 'owner_id', 'parent_recipe']