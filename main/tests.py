from datetime import datetime

from allauth.socialaccount.models import SocialApp, SocialLogin, SocialAccount
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase

# Create your tests here.
from main.models import Recipe
from main.views import IndexView, favorite_add


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
        SocialAccount.objects.create(user=self.request.user, provider='google', uid=123, last_login=datetime.now(), date_joined=datetime.now(), extra_data={"picture": "test.jpg"})
        self.current_site = Site.objects.get_current()

        response: TemplateResponse = IndexView.as_view()(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['avatar_url'], 'test.jpg')


class RecipeTests(TestCase):
    # Setting up
    def setUp(self):
        self.rf = RequestFactory()
        self.request = self.rf.get('/')
        self.request.user = User.objects.create_user('google', 'google@g.com', '123')

    def test_create_recipe_without_picture(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe", ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()
        self.assertFalse(x.picture)

    def test_favorite_recipe(self):
        owner = self.request.user
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe", ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
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
        response = favorite_add(self.request, x.id) #run favorite_add view again to remove from favorites
        self.assertEqual(response.status_code, 302)
        self.assertFalse(x in Recipe.objects.filter(favorites=self.request.user))







