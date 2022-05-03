from datetime import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.forms import modelform_factory
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase
# Create your tests here.
from django.urls import reverse_lazy

from main.models import Recipe
from main.views import IndexView, favorite_add, RecipeCreateView


class IndexTests(TestCase):

    # Setting up
    def setUp(self):
        self.rf = RequestFactory()
        self.request = self.rf.get('/')

    # Testing that the website works
    def test_user(self):
        self.request.user = User.objects.create(id=1, username="Tester")
        response = IndexView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    # Testing another user works
    def test_user_2(self):
        self.request.user = User.objects.create(id=2, username="Jard")
        response = IndexView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_with_anon_user(self):
        self.request.user = AnonymousUser()
        response = IndexView.as_view()(self.request)

        self.assertEqual(response.status_code, 200)

    def test_with_google_user(self):
        self.request.user = User.objects.create_user('google', 'google@g.com', '123')
        SocialAccount.objects.create(user=self.request.user, provider='google', uid=123, last_login=datetime.now(),
                                     date_joined=datetime.now(), extra_data={"picture": "test.jpg"})
        self.current_site = Site.objects.get_current()

        response: TemplateResponse = IndexView.as_view()(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['avatar_url'], 'test.jpg')



class RecipeTests(TestCase):
    # Setting up
    def setUp(self):
        self.user = User.objects.create_user('google', 'google@g.com', '123')
        self.rf = RequestFactory(defaults={"user": self.user})
        self.request = self.rf.get('/')
        self.request.user = self.user

    def test_create_recipe_without_picture(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()
        self.assertFalse(x.picture)

    def test_favorite_recipe(self):
        owner = self.request.user
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()
        self.request.META['HTTP_REFERER'] = 'anything'
        response = favorite_add(self.request, x.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(x in Recipe.objects.filter(favorites=self.request.user))
        self.assertEqual(owner.is_anonymous, False)

    def test_anon_favorite_recipe(self):
        owner = AnonymousUser()
        self.assertEqual(owner.is_anonymous, True)
        # owner must be of type user
        # Given that the user is anonymous, the following line fails
        # Recipe.objects.create(owner=self.request.user, title_text="Test Recipe", ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")

    def test_remove_favorite(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()
        self.request.META['HTTP_REFERER'] = 'anything'
        response = favorite_add(self.request, x.id)
        self.assertEqual(response.status_code, 302)
        response = favorite_add(self.request, x.id)  # run favorite_add view again to remove from favorites
        self.assertEqual(response.status_code, 302)
        self.assertFalse(x in Recipe.objects.filter(favorites=self.request.user))

    def test_fork_prepopulate(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")

        x.save()
        req = self.rf.get(reverse_lazy("new_recipe"), {"from": x.id})
        req.user = self.user

        view: RecipeCreateView = RecipeCreateView()
        view.setup(req)
        initial = view.get_initial()

        self.assertEqual(initial['title_text'], x.title_text)
        self.assertEqual(initial['ingredients_list'], x.ingredients_list)
        self.assertEqual(initial['body_text'], x.body_text)

        self.assertNotIn('parent_id', initial)

    def testDoNotShowIfDeleted(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Deleted Recipe",
                                      ingredients_list="Lots of ingredients", body_text="tasty meal!", deleted="true")
        x.save()
        recipes = []
        if x.deleted != "true":
            recipes.append(x)
        print(recipes)
        self.assertFalse(len(recipes) == 1)

    def testShowBasicRecipe(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Not Deleted Recipe",
                                  ingredients_list="Lots of ingredients part 2", body_text="tasty meal!", deleted="false")
        x.save()
        recipes = []
        if x.deleted != "true":
            recipes.append(x)
        print(recipes)
        self.assertTrue(len(recipes) == 1)

    def testShowEvenIfDeletedIsNotSet(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Not Deleted Recipe",
                                  ingredients_list="Lots of ingredients part 2", body_text="tasty meal!")
        x.save()
        recipes = []
        if x.deleted != "true":
            recipes.append(x)
        print(recipes)
        self.assertTrue(len(recipes) > 0)


class DefaultAvatarTests(TestCase):

    # Setting up
    def setUp(self):
        self.rf = RequestFactory()
        self.request = self.rf.get('/')

    # Default avatar test
    def avatar_is_default(self):
        response = IndexView.as_view()(self.request)
        self.assertContains(response, "bi bi-person-circle", html=True)


class CreateRecipeTests(TestCase):

    # Setting up
    def setUp(self):
        self.rf = RequestFactory()
        # self.request = self.rf.get('/')

    # Testing that empty form causes validation error
    def test_submitting_empty_form(self):
        request = self.rf.post("/recipe/add")
        request.user = User.objects.create(id=1, username="Tester")
        response = RecipeCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "/recipe/list", html=True)

    # Testing that request.user is assigned to recipe made
    def test_user_form(self):
        request = self.rf.post(reverse_lazy("new_recipe"), data={'title_text': "title", 'ingredients_list': "ingredients",
                                                    'body_text': "body", 'picture': ""})
        request.user = User.objects.create(id=1, username="Tester")
        response = RecipeCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.filter(title_text="title").first().owner, request.user)


