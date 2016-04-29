from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Quiz(models.Model):
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
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    string = models.CharField(max_length=1000)

    def __str__(self):
        return self.string


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

    def __str__(self):
        return self.string


class Quiz_attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_no = models.IntegerField()
    complete = models.BooleanField(default=False)
    # start_time = models.DateTimeField(default=datetime.now, blank=True)
    # end_time = models.DateTimeField()

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
        output = '<tr>'
        for field in self._meta.fields[1:]:
            output += '<th>%s</th>' % (field.name)
        output += '<th>%s</th>' % ("Score")
        output += '</tr>'
        return output

    def as_table(self):
        """Return quiz attempt results as an html table row."""
        output = '<tr>'
        for field in self._meta.fields[1:]:
            output += '<td>%s</td>' % (getattr(self, field.name))
        output += '<td>%s</td>' % (str(self.getScore()) + '/' + str(self.quiz.getScore()))
        output += '</tr>'
        return output


class Answer_attempt(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE)
#   submit_time = models.DateTimeField(default=datetime.now, blank=True)
