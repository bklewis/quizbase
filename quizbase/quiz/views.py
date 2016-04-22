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

from datetime import datetime

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
    context = {'quiz': quiz, }
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
#   return HttpResponse(str(quizAttempt.id) + "CREATED, Score = " + str(score))
    return HttpResponseRedirect(reverse(attempt, args=(quizAttempt.id, question.id,)))


@login_required(login_url='/login/')
def attempt(request, qaid, questionid):
    qa = Quiz_attempt.objects.get(id=qaid)
    quiz = Quiz.objects.get(id=qa.quiz.id)
    question = Question.objects.get(id=questionid)
    #attemptForm = AttemptForm(initial={'question': question})
    attemptForm = AttemptForm(question)
    context = {'question': question,
               'attemptForm': attemptForm,
               'qaid': qaid, }
    return render(request, 'attempt.html', context)
    # return HttpResponse(question.string + ',' + quiz.name + ',' + str(qaid))


@login_required(login_url='/login/')
def postattempt(request, qaid, questionid):
    qa = Quiz_attempt.objects.get(id=qaid)
    question = Question.objects.get(id=questionid)
    attemptForm = AttemptForm(question, request.POST)
    if attemptForm.is_valid():
        answers = attemptForm.answers
        return HttpResponse("Hello" + str(type(answers)) + "Goodbye")

        for string in answerStrings:
            return HttpResponse("Hello" + str(type(string)) + "BLOOEY")
            answer = Answer.objects.get(string=string)
            Answer_attempt(answer=answer, quiz_attempt=qa).save()
        questionList = sorted([q for q in Question.objects.get(quiz=qa.quiz) if q.id > questionid])
        if questionList:
            nextQuestion = questionList[0]
            return HttpResponseRedirect(reverse(attempt, args=(qaid, nextQuestion.id,)))
        else:
            return HttpResponse("FIN")
    else:
        return HttpResponse("This form is not valid")


@login_required(login_url='/login/')
def quizattempt(request, qaid):
    qa = Quiz_attempt.objects.get(id=qaid)
    quiz = Quiz.objects.get(id=qa.quiz.id)
    questionList = Question.objects.filter(quiz=quiz.id)
    context = {'quiz': quiz,
               'questionList': questionList}
    return render(request, 'qa.html', context)
    #qadic = {}
    # for question in questionList:
    #   answerList = Answer.objects.filter(question=question.id)
    #   qadic[question.string] = answerList
    #QaFormset = formset_factory(QaForm)
    #qaFormset = QaFormset(initial=questionList)
    # context = {'quiz': quiz,
    #       'questionList': questionList,
    #       'qadic': qadic,
    #       'qaFormset': qaFormset}
    # return render(request, 'qa.html', context)
#   return HttpResponse("HEY!" + str(qaid))

# def postquizattempt(request, qaid):
#   qaFormset = QaFormset(request.POST)
#   if qaFormset.is_valid():
    # question = Question(string=questionForm.cleaned_data['string'],
    #   quiz=quizid)
#       qaForm = qaFormset.save()
#       return HttpResponse("WHA")


@login_required(login_url='/login/')
def quizzes(request):
    quizList = Quiz.objects.order_by(Lower('name'))
    context = {'quizList': quizList, }
    return render(request, 'quizzes.html', context)


@login_required(login_url='/login/')
def questions(request, quizid):
    questionForm = QuestionForm(initial={'quiz': quizid})
    quiz = Quiz.objects.get(id=quizid)
    questionList = Question.objects.filter(quiz=quizid)
    context = {'questionList': questionList,
               'quiz': quiz,
               'questionForm': questionForm, }
    return render(request, 'questions.html', context)


@login_required(login_url='/login/')
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


#   questionForm = QuestionForm(initial={'quiz':quizid})
#   quiz = Quiz.objects.get(id=quizid)
#   questionList = Question.objects.filter(quiz=quizid)
#   context = {'questionList': questionList,
#           'quiz' : quiz,
#           'questionForm': questionForm,}
#   return render(request, 'questions.html', context)

@login_required(login_url='/login/')
def postquiz(request):
    quizname = request.POST['quizname']
    quiz = Quiz(name=quizname)
    quiz.save()
    quiz = Quiz.objects.get(name=quizname)
    return HttpResponseRedirect('/quizzes/' + str(quiz.id) + '/')


@login_required(login_url='/login/')
def postquestion(request, quizid):  # , questionid):
    questionForm = QuestionForm(request.POST)
    if questionForm.is_valid():
            # question = Question(string=questionForm.cleaned_data['string'],
            #   quiz=quizid)
        question = questionForm.save()
        return HttpResponseRedirect(reverse(answers, args=(quizid, question.id,)))
    #quiz = Quiz.objects.get(name = quizname)
    #question = Question(string=request.Post['questionstring'], quiz=quiz)
    # question.save()
    # I think I need ID!
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/')


@login_required(login_url='/login/')
def postanswer(request, quizid, questionid):
    answerForm = AnswerForm(request.POST)
    if answerForm.is_valid():
        answer = answerForm.save()
        return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/')
    else:
        return HttpResponse("This form is not valid")


class QuizListView(ListView):
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
