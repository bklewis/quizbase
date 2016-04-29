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
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.http import Http404

from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy

import re
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
    qList = []
    for q in quizList:
        questions = Question.objects.filter(quiz=q.id)
        if questions:
            qList.append(q)
    context = {'quizList': qList, }
    return render(request, 'quizme.html', context)


@login_required(login_url='/login/')
def quizready(request, quizid):
    quiz = get_object_or_404(Quiz, id=quizid)
    questions = Question.objects.filter(quiz=quizid)
    numQuestions = len(questions)
    context = {'quiz': quiz,
               'numQuestions': numQuestions}
    return render(request, 'qready.html', context)


@login_required(login_url='/login/')
def postquizready(request, quizid):
    quiz = get_object_or_404(Quiz, id=quizid)
    attemptList = Quiz_attempt.objects.filter(quiz=quizid)
    attemptNo = len(attemptList) + 1
    quizAttempt = Quiz_attempt(quiz=quiz,
                               user=request.user,
                               attempt_no=attemptNo,
                               # start_time=datetime.now(),
                               # end_time=datetime.now()
                               complete=False)
    quizAttempt.save()
    score = quiz.getScore()
    question = quiz.question_set.all().order_by('id')[0]
    return HttpResponseRedirect(reverse(attempt, args=(quizAttempt.id, question.id,)))


@login_required(login_url='/login/')
def postquizattempt(request, qaid):
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    qa.complete = True
    # qa.end_time = datetime.now()
    qa.save()
    return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))


@login_required(login_url='/login/')
def finishquiz(request, qaid):
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    quiz = get_object_or_404(Quiz, id=qa.quiz.id)
    maxScore = quiz.getScore()
    yourScore = qa.getScore()
    context = {'yourScore': yourScore,
               'maxScore': maxScore,
               'quiz': quiz}
    return render(request, 'finish.html', context)


@login_required(login_url='/login/')
def attempt(request, qaid, questionid):
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    if qa.complete:
        return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))
    quiz = get_object_or_404(Quiz, id=qa.quiz.id)
    question = get_object_or_404(Question, id=questionid)
    answerList = Answer.objects.filter(question=questionid)

    aaList = Answer_attempt.objects.filter(quiz_attempt=qaid)
    takenQs = set()
    if not answerList:
        takenQs.add(int(questionid))

    for a in aaList:
        answer = get_object_or_404(Answer, id=a.answer.id)
        takenQ = get_object_or_404(Question, id=answer.question.id)
        takenQs.add(int(takenQ.id))

    if int(questionid) in takenQs:
        questionList = Question.objects.filter(quiz=quiz.id)
        nextQuestions = sorted([q.id for q in questionList if int(q.id) not in takenQs])
        nextQs = nextQuestions[:]
        for qid in nextQs:
            answerList = Answer.objects.filter(question=qid)
            if not answerList:
                nextQuestions.remove(qid)
        if nextQuestions:
            questionid = nextQuestions[0]
            question = get_object_or_404(Question, id=questionid)
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
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    if qa.complete:
        return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))
    question = get_object_or_404(Question, id=questionid)
    attemptForm = AttemptForm(question, request.POST)
    if attemptForm.is_valid():
        answers = attemptForm.cleaned_data['answers']
        for a in answers:
            answer = get_object_or_404(Answer, id=a.id)
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
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    quiz = get_object_or_404(Quiz, id=qa.quiz.id)
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
    quiz = get_object_or_404(Quiz, id=quizid)
    questionList = Question.objects.filter(quiz=quizid)
    context = {'questionList': questionList,
               'quiz': quiz,
               'questionForm': questionForm, }
    return render(request, 'questions.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def answers(request, quizid, questionid):
    quiz = get_object_or_404(Quiz, id=quizid)
    question = get_object_or_404(Question, id=questionid)
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
    quiz = get_object_or_404(Quiz, name=quizname)
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


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def deletequiz(request, quizid):
    quiz = get_object_or_404(Quiz, id=quizid)
    if request.method == 'POST':
        quiz.delete()
    return HttpResponseRedirect('/quizzes/')


@login_required(login_url='/login/')
def results(request):
    user = request.user
    if user.is_superuser:
        outputs = Quiz_attempt.objects.all()
    else:
        outputs = Quiz_attempt.objects.filter(user=user.id)
    return render_to_response('results.html', {'outputs': outputs})
