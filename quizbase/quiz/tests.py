from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve

import unittest

from .forms import *
from .models import *
from .views import *

# Create your tests here.


class BasicTests(TestCase):

    def test_index_page(self):
        # response = self.client.get('/quizzes/', follow=True)
        # self.assertRedirects(response, '/login/')
        found = resolve('/')
        self.assertEqual(found.func, index)

    # def test_user(self):
    #     myUser = User.objects.create(name='admin')
    #     user = User.objects.get(name='admin')
    #     self.assertEqual(myUser, user)


class CreateQuiz(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'test@email.com', 'password')
        self.admin.save()
        # Quiz.objects.create(name="quiz")

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.client.login(username=self.admin.username, password=self.admin.password)
        self.assertEqual(self.admin.is_staff, True)
        response = self.client.get('')
        # self.assertEqual(200, response.status_code)


# Inputting a quiz
# Taking a quiz
# Score
