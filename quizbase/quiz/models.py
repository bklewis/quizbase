from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def getScore(self):
        """ Returns max score for quiz """
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
    # COMPLETE = 2
    # INPROGRESS = 1
    # INCOMPLETE = 0
    # STATUS_CHOICES = (
    #     (COMPLETE, 'Correct'),
    #     (INPROGRESS, 'Not Wrong'),
    #     (INCOMPLETE, 'Incorrect'),
    # )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_no = models.IntegerField()
    # complete = models.BooleanField(default=True)
    # status = models.IntegerField(choices=STATUS_CHOICES, default=INPROGRESS)
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField()

    def getScore(self):
        "Returns score for quiz attempt"
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

    def as_table(self):
        output = '<table>'
        # for each field in model
        for field in self._meta.fields:
            # optionally skip any unwanted fields such as primary keys, etc
            # if field.auto_created:
            #    continue
            output += '<tr><th>%s</th><td>%s</td></tr>' % (
                field.name, getattr(self, field.name))
        output += '</table>'
        return output


class Answer_attempt(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE)
#   submit_time = models.DateTimeField(default=datetime.now, blank=True)


# class Results_Form(ModelForm):

 #   class Meta:
  #      model = Quiz_attempt
