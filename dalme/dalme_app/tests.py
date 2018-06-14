from django.test import TestCase, Client
from django.urls import reverse

class HomepageTestCase(TestCase):
    def test_load_homepage(self):
        c = Client()
        response = c.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code,200)
