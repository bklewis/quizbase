from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse, resolve
from .forms import *
from .models import *
from .views import *

# Create your tests here.

# Views Tests

print "HI"


class BasicTests(TestCase):

    def test_root_url_resolves_to_index_view(self):
        # response = self.client.get('/quizzes/', follow=True)
        # self.assertRedirects(response, '/login/')
        found = resolve('/')
        self.assertEqual(found.func, index)


# Inputting a quiz
# Taking a quiz
# Score
