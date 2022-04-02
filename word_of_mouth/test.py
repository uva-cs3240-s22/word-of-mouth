from django.test import TestCase


class DummyTestCase(TestCase):
    def test_dummy(self):
        x = 1
        self.assertEqual(x, 1)
        
class TrueCase(TestCase):
    def auth_test(self):
        test = True
        message = "Test value is not true"
        self.assertTrue(test, message)
