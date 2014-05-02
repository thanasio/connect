from django.test import RequestFactory, SimpleTestCase

from views import home


__author__ = 'rogueleaderr'


class HomepageTest(SimpleTestCase):
    #fixtures = []

    def setUp(self):
        return

    def test_homepage(self):
        # create fake request
        request_factory = RequestFactory()
        request = request_factory.post('/fake-path', data={})
        # execute view code
        response = home(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Kano Konnect', response.content)