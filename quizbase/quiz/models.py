"""All models for QuizBase."""

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Quiz(models.Model):
    """Quiz object with name."""

    name = models.CharField(max_length=255, unique=True)

    def getScore(self):
        """Return the max score for quiz."""
        questionList = Question.objects.filter(quiz=self.id)
        score = 0
        for q in questionList:
            answerList = Answer.objects.filter(question=q.id)
            vList = [a.value for a in answerList]
            twos = vList.count(2)
            score += twos
        return score

    def __str__(self):
        """Return the name of the quiz as a string."""
        return self.name


class Question(models.Model):
    """Question object with string and foriegn key quiz."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    string = models.CharField(max_length=1000)

    def __str__(self):
        """Return the question string."""
        return self.string


class Answer(models.Model):
    """Answer object with string, value, and foriegn key question."""

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

    def __str__(self):
        """Return the answer string."""
        return self.string


class Quiz_attempt(models.Model):
    """
    Quiz attempt with associated user and quiz.

    Quiz attempt has the quiz the user was trying to take.
    It also has the user taking it, the nth attempt,
    and whether or not the quiz was completed.
    """

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_no = models.IntegerField()
    complete = models.BooleanField(default=False)

    def getScore(self):
        """Return user's score for quiz attempt."""
        quiz = self.quiz
        questionList = Question.objects.filter(quiz=quiz.id)
        aaList = Answer_attempt.objects.filter(quiz_attempt=self.id)
        score = 0.0
        for q in questionList:
            vList = []
            answerList = Answer.objects.filter(question=q.id)
            for a in answerList:
                for aa in aaList:
                    if aa.answer.id == a.id:
                        vList.append(a.value)
            twos = vList.count(2)
            ones = vList.count(1)
            zeros = vList.count(0)
            score += twos * (1.0 / (2 ** ones)) * (0 ** zeros)
        return score

    def as_table_headers(self):
        """Return headers for html quiz attempt results table."""
        output = '<tr id="results">'
        for field in self._meta.fields[1:]:
            output += '<th id="results">%s</th>' % (field.name)
        output += '<th id="results">%s</th>' % ("Score")
        output += '</tr>'
        return output

    def as_table(self):
        """Return quiz attempt results as an html table row."""
        output = '<tr id="results">'
        for field in self._meta.fields[1:]:
            output += '<td id="results">%s</td>' % (getattr(self, field.name))
        output += '<td id="results">%s</td>' % (str(self.getScore()) + '/' + str(self.quiz.getScore()))
        output += '</tr>'
        return output


class Answer_attempt(models.Model):
    """
    Answer attempt with associated answer and quiz attempt.

    An answer attempt has the answer the user selected.
    It also has the quiz attempt with which the selection was associated.
    """

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE)
