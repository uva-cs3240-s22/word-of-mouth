from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    title_text = models.CharField(max_length=200)
    ingredients_list = models.TextField()
    body_text = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now)
    edited_date = models.DateTimeField(default=datetime.now)
    parent = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True,
                               related_name="children")  # reference parent recipe ID
    picture = models.ImageField(null=True, upload_to='photos', blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    favorites = models.ManyToManyField(User, related_name="favorites")

    # THINGS TO THINK ABOUT -
    # what should the picture(s) be
    # what happens when a recipe (particularly a parent recipe) is deleted
    # should a recipe be its own parent by default?

    def __str__(self):
        return self.title_text
