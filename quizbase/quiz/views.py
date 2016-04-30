"""All views for QuizBase."""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
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


@login_required(login_url='/login/')
def index(request):
    """Display the home page."""
    return render(request, 'index.html')


@login_required(login_url='/login/')
def quizme(request):
    """Display quizzes available for user to take."""
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
    """Post new quiz attempt if user is ready to start."""
    quiz = get_object_or_404(Quiz, id=quizid)
    questions = Question.objects.filter(quiz=quizid)
    numQuestions = len(questions)
    context = {'quiz': quiz,
               'numQuestions': numQuestions}
    return render(request, 'qready.html', context)


@login_required(login_url='/login/')
def postquizready(request, quizid):
    """Create new quiz attempt."""
    quiz = get_object_or_404(Quiz, id=quizid)
    current_user = request.user
    attemptList = Quiz_attempt.objects.filter(quiz=quizid, user=current_user.id)
    attemptNo = len(attemptList) + 1
    quizAttempt = Quiz_attempt(quiz=quiz,
                               user=current_user,
                               attempt_no=attemptNo,
                               complete=False)
    quizAttempt.save()
    score = quiz.getScore()
    question = quiz.question_set.all().order_by('id')[0]
    return HttpResponseRedirect(reverse(attempt, args=(quizAttempt.id, question.id,)))


@login_required(login_url='/login/')
def postquizattempt(request, qaid):
    """Mark quiz attempt as complete."""
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    qa.complete = True
    qa.save()
    return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))


@login_required(login_url='/login/')
def finishquiz(request, qaid):
    """Display user's final score for completed quiz attempt."""
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
    """Display question and answer form from a quiz."""
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    if qa.complete:
        return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))
    quiz = get_object_or_404(Quiz, id=qa.quiz.id)
    question = get_object_or_404(Question, id=questionid)
    answerList = Answer.objects.filter(question=questionid)

    # If the question has no answers, don't display it
    aaList = Answer_attempt.objects.filter(quiz_attempt=qaid)
    takenQs = set()
    if not answerList:
        takenQs.add(int(questionid))

    for a in aaList:
        answer = get_object_or_404(Answer, id=a.answer.id)
        takenQ = get_object_or_404(Question, id=answer.question.id)
        takenQs.add(int(takenQ.id))

    # If the user has answered the question, don't display it
    # (Does not cover back button case)
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
    """Post user's response to a quiz question."""
    qa = get_object_or_404(Quiz_attempt, id=qaid)

    # If the quiz is complete, do not allow user to post new response
    if qa.complete:
        return HttpResponseRedirect(reverse(finishquiz, args=[qaid]))
    question = get_object_or_404(Question, id=questionid)
    attemptForm = AttemptForm(question, request.POST)

    """The next question in the quiz should be the first
       chronologically that user has not answered."""
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
        return HttpResponse("Not quite... Please select at least one answer, and make sure there's no funny business going on.  Hit back and resubmit to try again!")


@login_required(login_url='/login/')
def quizattempt(request, qaid):
    """Get a quiz attempt."""
    qa = get_object_or_404(Quiz_attempt, id=qaid)
    quiz = get_object_or_404(Quiz, id=qa.quiz.id)
    questionList = Question.objects.filter(quiz=quiz.id)
    context = {'quiz': quiz,
               'questionList': questionList}
    return render(request, 'qa.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def quizzes(request):
    """Display all quizzes and allow user to create new quiz."""
    quizList = Quiz.objects.order_by(Lower('name'))
    context = {'quizList': quizList, }
    return render(request, 'quizzes.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def questions(request, quizid):
    """Display questions for a quiz and allow user to create new question."""
    questionForm = QuestionForm(initial={'quiz': quizid})
    quiz = get_object_or_404(Quiz, id=quizid)
    questionList = Question.objects.filter(quiz=quizid)
    context = {'questionList': questionList,
               'quiz': quiz,
               'questionForm': questionForm, }
    return render(request, 'questions.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def answers(request, quizid, questionid):
    """Display answers for a question and allow user to create new answer."""
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
    """Create a new quiz."""
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
    """Create a new question."""
    questionForm = QuestionForm(request.POST)
    if questionForm.is_valid():
        question = questionForm.save()
        return HttpResponseRedirect(reverse(answers, args=(quizid, question.id,)))
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def postanswer(request, quizid, questionid):
    """Create a new answer."""
    answerForm = AnswerForm(request.POST)
    if answerForm.is_valid():
        answer = answerForm.save()
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def deletequiz(request, quizid):
    """Delete a quiz."""
    quiz = get_object_or_404(Quiz, id=quizid)
    if request.method == 'POST':
        quiz.delete()
    return HttpResponseRedirect('/quizzes/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def deletequestion(request, questionid):
    """Delete a question."""
    question = get_object_or_404(Question, id=questionid)
    quizid = question.quiz.id
    if request.method == 'POST':
        question.delete()
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def deleteanswer(request, answerid):
    """Delete an answer."""
    answer = get_object_or_404(Answer, id=answerid)
    questionid = answer.question.id
    question = get_object_or_404(Question, id=questionid)
    quizid = question.quiz.id
    if request.method == 'POST':
        answer.delete()
    return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/')


@login_required(login_url='/login/')
def results(request):
    """Show results of all available taken quizzes."""
    user = request.user
    if user.is_superuser:
        outputs = Quiz_attempt.objects.all()
    else:
        outputs = Quiz_attempt.objects.filter(user=user.id)
    return render_to_response('results.html', {'outputs': outputs})
