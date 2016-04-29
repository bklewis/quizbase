from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.forms import formset_factory
from django.db.models.functions import Lower
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime
import re

from .forms import QuestionForm, AnswerForm, AttemptForm

from .models import Quiz, Question, Answer, Quiz_attempt, Answer_attempt

# Create your views here.


def base(request):
    return render(request, 'base.html')


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def quizme(request):
    quizList = Quiz.objects.order_by(Lower('name'))
    context = {'quizList': quizList, }
    return render(request, 'quizme.html', context)


@login_required(login_url='/login/')
def quizready(request, quizid):
    quiz = Quiz.objects.get(id=quizid)
    questions = Question.objects.filter(quiz=quizid)
    numQuestions = len(questions)
    context = {'quiz': quiz,
               'numQuestions': numQuestions}
    return render(request, 'qready.html', context)


@login_required(login_url='/login/')
def postquizready(request, quizid):
    quiz = Quiz.objects.get(id=quizid)
    attemptList = Quiz_attempt.objects.filter(quiz=quizid)
    attemptNo = len(attemptList) + 1
    quizAttempt = Quiz_attempt(quiz=quiz,
                               user=request.user,
                               attempt_no=attemptNo,
                               start_time=datetime.now(),
                               end_time=datetime.now())
    quizAttempt.save()
    score = quiz.getScore()
    question = quiz.question_set.all().order_by('id')[0]
    return HttpResponseRedirect(reverse(attempt, args=(quizAttempt.id, question.id,)))


@login_required(login_url='/login/')
def postquizattempt(request, qaid):
    qa = Quiz_attempt.objects.get(id=qaid)
    qa.end_time = datetime.now()
    qa.save()
    return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))


@login_required(login_url='/login/')
def finishquiz(request, qaid):
    qa = Quiz_attempt.objects.get(id=qaid)
    quiz = Quiz.objects.get(id=qa.quiz.id)
    maxScore = quiz.getScore()
    yourScore = qa.getScore()
    return HttpResponse("You're done!  Your score is " + str(yourScore) + "/" + str(maxScore))


@login_required(login_url='/login/')
def attempt(request, qaid, questionid):
    qa = Quiz_attempt.objects.get(id=qaid)
    quiz = Quiz.objects.get(id=qa.quiz.id)
    question = Question.objects.get(id=questionid)

    aaList = Answer_attempt.objects.filter(quiz_attempt=qaid)

    takenQs = set()

    for a in aaList:
        answer = Answer.objects.get(id=a.answer.id)
        takenQ = Question.objects.get(id=answer.question.id)
        takenQs.add(int(takenQ.id))

    if int(questionid) in takenQs:
        questionList = Question.objects.filter(quiz=quiz.id)
        nextQuestions = sorted([q.id for q in questionList if int(q.id) not in takenQs])
        if nextQuestions:
            questionid = nextQuestions[0]
            question = Question.objects.get(id=questionid)
        else:
            return HttpResponseRedirect(reverse(postquizattempt, args=[qaid]))

    attemptForm = AttemptForm(question)
    context = {'question': question,
               'attemptForm': attemptForm,
               'qaid': qaid,
               'quiz': quiz}
    return render(request, 'attempt.html', context)


@login_required(login_url='/login/')
def postattempt(request, qaid, questionid):
    qa = Quiz_attempt.objects.get(id=qaid)
    question = Question.objects.get(id=questionid)
    attemptForm = AttemptForm(question, request.POST)
    if attemptForm.is_valid():
        answers = attemptForm.cleaned_data['answers']
        for a in answers:
            answer = Answer.objects.get(id=a.id)
            if answer not in [a.answer for a in Answer_attempt.objects.filter(quiz_attempt=qa)]:
                Answer_attempt(answer=answer, quiz_attempt=qa).save()
        questionList = Question.objects.filter(quiz=qa.quiz)
        nextQuestions = sorted([q.id for q in questionList if int(q.id) > int(questionid)])
        if nextQuestions:
            nextQuestion = nextQuestions[0]
            return HttpResponseRedirect(reverse(attempt, args=(qaid, nextQuestion,)))
        else:
            return HttpResponseRedirect(reverse(postquizattempt, args=[qaid]))
    else:
        return HttpResponse("You have to pick at least one answer! Press the back button and try again")


@login_required(login_url='/login/')
def quizattempt(request, qaid):
    qa = Quiz_attempt.objects.get(id=qaid)
    quiz = Quiz.objects.get(id=qa.quiz.id)
    questionList = Question.objects.filter(quiz=quiz.id)
    context = {'quiz': quiz,
               'questionList': questionList}
    return render(request, 'qa.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def quizzes(request):
    quizList = Quiz.objects.order_by(Lower('name'))
    context = {'quizList': quizList, }
    return render(request, 'quizzes.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def questions(request, quizid):
    questionForm = QuestionForm(initial={'quiz': quizid})
    quiz = Quiz.objects.get(id=quizid)
    questionList = Question.objects.filter(quiz=quizid)
    context = {'questionList': questionList,
               'quiz': quiz,
               'questionForm': questionForm, }
    return render(request, 'questions.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def answers(request, quizid, questionid):
    quiz = Quiz.objects.get(id=quizid)
    question = Question.objects.get(id=questionid)
    answerForm = AnswerForm(initial={'question': questionid})
    answerList = Answer.objects.filter(question=questionid)
    context = {'answerList': answerList,
               'quiz': quiz,
               'question': question,
               'answerForm': answerForm, }
    return render(request, 'answers.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def postquiz(request):
    quizname = request.POST['quizname']
    if not (re.search('[a-zA-Z0-9]', quizname)):
        return HttpResponseRedirect('/quizzes/')
    if quizname not in [quiz.name for quiz in Quiz.objects.all()]:
        quiz = Quiz(name=quizname)
        quiz.save()
    quiz = Quiz.objects.get(name=quizname)
    return HttpResponseRedirect('/quizzes/' + str(quiz.id) + '/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def postquestion(request, quizid):
    questionForm = QuestionForm(request.POST)
    if questionForm.is_valid():
        question = questionForm.save()
        return HttpResponseRedirect(reverse(answers, args=(quizid, question.id,)))
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def postanswer(request, quizid, questionid):
    answerForm = AnswerForm(request.POST)
    if answerForm.is_valid():
        answer = answerForm.save()
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/')
