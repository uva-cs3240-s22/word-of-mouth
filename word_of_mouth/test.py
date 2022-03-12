from django.test import TestCase


class DummyTestCase(TestCase):
    def test_dummy(self):
        x = 1
        self.assertEqual(x, 1)
