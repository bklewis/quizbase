from django.db import models
from datetime import datetime

# Create your models here.

class Quiz(models.Model):
	name = models.CharField(max_length=256)

class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	string = models.CharField(max_length=1000)
#	ord = models.IntegerField()

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	string = models.CharField(max_length=1000)
	correctness = models.IntegerField()

class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=500)
	permissions = models.IntegerField()
	password = models.CharField(max_length=100)

class Quiz_attempt(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	attempt_no = models.IntegerField()
	score = models.IntegerField()
	start_time = models.DateTimeField(default=datetime.now, blank=True)
	end_time = models.DateTimeField()

class Answer_attempt(models.Model):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE)
	submit_time = models.DateTimeField(default=datetime.now, blank=True)
