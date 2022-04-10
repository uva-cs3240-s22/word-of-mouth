from datetime import datetime

from allauth.socialaccount.models import SocialApp, SocialLogin, SocialAccount
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase

# Create your tests here.
from main.views import IndexView
from main.views import RecipeCreateView
from main.models import Recipe


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
        self.assertEqual(response.context_data['avatar_url'], 'test.jpg')


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
        request = self.rf.post("/recipe/add", data={'title_text': "title", 'ingredients_list': "ingredients",
                                                    'body_text': "body"})
        request.user = User.objects.create(id=1, username="Tester")
        response = RecipeCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)


