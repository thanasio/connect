from django.core.urlresolvers import reverse
from django.test import Client, TestCase

__author__ = 'rogueleaderr'

"""
A file for system tests (i.e. tests that request full pages).

These will run much slower than unit tests, so we want to retain the option to not
run them every time we run the test suite.
"""

class HomepageSystemTest(TestCase):
    #fixtures = []

    def setUp(self):
        return

    def test_homepage(self):
        url = reverse("home")
        c = Client()
        req = c.get(url)
        self.assertEqual(req.status_code, 200)
        self.assertTemplateUsed(req, "homepage.html")
        self.assertIn("Kano Konnect", req.content)
