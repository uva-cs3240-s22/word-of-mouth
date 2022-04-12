from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    title_text = models.CharField(max_length=200)
    ingredients_list = models.TextField()
    body_text = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now())
    edited_date = models.DateTimeField(default=datetime.now())
    parent = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True,
                               related_name="children")  # reference parent recipe ID
    picture = models.ImageField(null=True, upload_to='photos')

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


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    body = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now)
    edited_date = models.DateTimeField(null=True)
    recipe = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Start typing...', 'rows': 2}),
        }