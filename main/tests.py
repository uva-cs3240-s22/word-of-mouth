from datetime import datetime

from allauth.socialaccount.models import SocialApp, SocialLogin, SocialAccount
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase

# Create your tests here.
from django.urls import reverse_lazy, reverse

from main.models import Recipe
from main.views import IndexView, favorite_add, RecipeCreateView
from main.views import IndexView
from main.views import RecipeCreateView, RecipeCommentFormView
from main.models import Recipe, Comment


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

    # Testing that an authenticated user will be able to get to the create recipe page
    def test_with_authenticated_user(self):
        request = self.rf.get("/recipe/add")
        request.user = User.objects.create(id=1, username="Tester")
        response = RecipeCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # Testing that an anonymous user is redirected when trying to go to the create recipe page
    def test_with_anon_user(self):
        request = self.rf.get("/recipe/add")
        request.user = AnonymousUser()
        response = RecipeCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)



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

    def test_fork_different_user_and_date(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")

        x.save()
        req = self.rf.get(reverse_lazy("new_recipe"), {"from": x.id})
        test_user = User.objects.create_user('google2', 'google2@g.com', '1234')
        req.user = test_user
        view: RecipeCreateView = RecipeCreateView()
        view.setup(req)
        initial = view.get_initial()

        req2 = self.rf.post(reverse_lazy("new_recipe"), data={'title_text':initial['title_text'],'ingredients_list':initial['ingredients_list'], 'body_text':initial['body_text']})
        req2.user=test_user
        response = RecipeCreateView.as_view()(req2)

        y = Recipe.objects.get(owner= test_user)

        self.assertNotEqual(y.owner, x.owner)
        self.assertNotEqual(y.posted_date, x.posted_date)
        self.assertEqual(y.body_text, x.body_text)


    def test_comment_anon_user(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()
        req = self.rf.post('/recipe/1', data={'message':'test comment'})
        req.user = AnonymousUser()
        response = RecipeCommentFormView.as_view()(req)
        self.assertEqual(response.status_code, 302)

    def test_comment_authenticated_user(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()

        req = self.rf.post(reverse('recipe_detail', kwargs={'pk':1},), data={'message':'test comment'})
        test_user = User.objects.create_user('google2', 'google2@g.com', '1234')
        test_user.save()
        req.user = test_user
        response = RecipeCommentFormView.as_view()(req, **{'pk': 1})
        self.assertEqual(response.status_code, 200)

    def test_comment_created(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()

        y = Comment.objects.create(owner=self.request.user, body= "test comment", recipe=x)
        y.save()

        self.assertTrue(y.recipe, x)
        self.assertTrue(y.body, "test comment")
        self.assertTrue(y.owner, self.request.user)

    def test_empty_comment_created(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")
        x.save()

        y = Comment.objects.create(owner=self.request.user, recipe=x)
        y.save()

        self.assertTrue(y.DoesNotExist)

    def test_fork_comments(self):
        x = Recipe.objects.create(owner=self.request.user, title_text="Test Recipe",
                                  ingredients_list="Ingredients! yum yum yum!", body_text="wowza!")

        x.save()
        req = self.rf.get(reverse_lazy("new_recipe"), {"from": x.id})
        req.user = self.user

        view: RecipeCreateView = RecipeCreateView()
        view.setup(req)

        recipe = get_object_or_404(Recipe, id=x.id)

        testComment = Comment.objects.create(owner=self.request.user, body="test", recipe=recipe)
        testComment2 = Comment.objects.create(owner=self.request.user, body="comment", recipe=recipe)
        testComment.save()
        testComment2.save()

        commentCount = 0

        for comment in recipe.comments.values().all():
            commentCount += 1

        self.assertTrue(commentCount == 2)



class TestRedirectsOnAnon(TestCase):
    def setUp(self) -> None:
        self.rf = RequestFactory()

    def test_create_recipe_302(self):
        request = self.rf.get(reverse_lazy("new_recipe"))
        request.user = AnonymousUser()
        response = RecipeCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_create_recipe_redirects_to_google(self):
        request = self.rf.get(reverse_lazy("new_recipe"))
        request.user = AnonymousUser()
        response = RecipeCreateView.as_view()(request)

        self.assertIn("login", response.url)
        self.assertIn("google", response.url)

    #def test_favorite_redirects_to_google(self):
     #   request = self.rf.get(reverse_lazy("favorite_add", kwargs={"id": 3}))
     #   request.user = AnonymousUser()
      #  response = favorite_add(request)
#
      #  self.assertIn("login", response.url)
      #  self.assertIn("google", response.url)
       # self.assertIn("next=/recipe/fav/", response.url)
