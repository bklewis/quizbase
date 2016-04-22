from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def getScore(self):
        "Returns max score for quiz"
        questionList = Question.objects.filter(quiz=self.id)
        score = 0
        for q in questionList:
            answerList = Answer.objects.filter(question=q.id)
            vList = [a.value for a in answerList]
            twos = vList.count(2)
            score += twos
        return score


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    string = models.CharField(max_length=1000)


class Answer(models.Model):
    CORRECT = 2
    NOTWRONG = 1
    INCORRECT = 0
    VALUE_CHOICES = (
        (CORRECT, 'Correct'),
        (NOTWRONG, 'Not Wrong'),
        (INCORRECT, 'Incorrect'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    string = models.CharField(max_length=1000)
    value = models.IntegerField(choices=VALUE_CHOICES, default=INCORRECT)


class Quiz_attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_no = models.IntegerField()
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField()

    def getScore(self):
        "Returns score for quiz attempt"
        quiz = self.quiz
        questionList = Question.objects.filter(quiz=quiz.id)
        aaList = Answer_attempt.objects.filter(quiz_attempt=self.id)
        score = 0
        for q in questionList:
            vList = []
            answerList = Answer.objects.filter(question=q.id)
            for a in answerList:
                if aa.answer == a.id:
                    vList.append(a.value)
            twos = vList.count(2)
            ones = vList.count(1)
            zeros = vList.count(0)
            score += twos * (1 / (2 ** ones)) * (0 ** zeros)
        return score


class Answer_attempt(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE)
#	submit_time = models.DateTimeField(default=datetime.now, blank=True)
