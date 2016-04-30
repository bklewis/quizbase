"""All the Tests."""
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


class Login(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'test@email.com', 'password')
        self.admin.save()

    def test_user_creation(self):
        self.client.login(username=self.admin.username, password=self.admin.password)
        # self.assertEqual(self.client.user, self.admin)
        # self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.admin.is_staff, True)

    def test_page_protection(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')

    def test_login_view(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.assertRedirects(response, '/')


class CreateThings(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'test@email.com', 'password')
        self.admin.save()
        self.client.login(username=self.admin.username, password=self.admin.password)

    def test_login_view(self):
        response = self.client.post('/postquiz/', {'name': 'testquiz'})


class GetThings(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'test@email.com', 'password')
        self.admin.save()
        self.client.login(username=self.admin.username, password=self.admin.password)
        quiz = Quiz(name="testquiz")
        quiz.save()

    def test_quiz_input_and_output(self):
        quiz = Quiz.objects.create(name="quiz")
        getQuiz = Quiz.objects.get(id=quiz.id)
        self.assertEqual(quiz, getQuiz)
