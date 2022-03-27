from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .views import Index


# Create your tests here.
class Index_tests(TestCase):

    # Setting up
    def setUp(self):
        self.rf = RequestFactory()

    # Testing that the website works
    def Main_page_basic_test(self):
        request = self.rf.get('/')
        request.user = User.objects.create(id=1, username="Tester")
        response = Index.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # Testing another user works
    def Main_page_another_basic_test(self):
        request = self.rf.get('/')
        request.user = User.objects.create(id=2, username="Jard")
        response = Index.as_view()(request)
        self.assertEqual(response.status_code, 200)
