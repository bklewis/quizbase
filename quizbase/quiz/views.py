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

from datetime import datetime

from .forms import QuestionForm, AnswerForm

from .models import Quiz, Question, Answer, Quiz_attempt

# Create your views here.

@login_required(login_url='/login/')
def index(request):
	return render(request, 'index.html')

def base(request):
	return render(request, 'base.html')

@login_required(login_url='/login/')
def quizme(request):
	quizList = Quiz.objects.order_by('name')
	context = {'quizList': quizList,}
	return render(request, 'quizme.html', context)

@login_required(login_url='/login/')
def quizready(request, quizid):
	quiz = Quiz.objects.get(id=quizid)
	attemptList = Quiz_attempt.objects.filter(quiz=quizid)
	attemptNo = len(attemptList) + 1
	quizAttempt = Quiz_attempt(quiz=quiz, 
			user=request.user,
			attempt_no = attemptNo,
			score = -1,
			start_time = datetime.now(),
			end_time = datetime.now())
	quizAttempt.save()
	return HttpResponse(str(quizAttempt.id) + "CREATED")


@login_required(login_url='/login/')
def quizzes(request):
	quizList = Quiz.objects.order_by('name')
	context = {'quizList': quizList,}
	return render(request, 'quizzes.html', context)

def questions(request, quizid):
	questionForm = QuestionForm(initial={'quiz':quizid})
	quiz = Quiz.objects.get(id=quizid)
	questionList = Question.objects.filter(quiz=quizid)
	context = {'questionList': questionList,
			'quiz' : quiz,
			'questionForm': questionForm,}
	return render(request, 'questions.html', context)

def answers(request, quizid, questionid):
	quiz = Quiz.objects.get(id=quizid)
	question = Question.objects.get(id=questionid)
	answerForm = AnswerForm(initial={'question':questionid})
	answerList = Answer.objects.filter(question=questionid)
	context = {'answerList': answerList,
			'quiz' : quiz,
			'question': question,
			'answerForm': answerForm,}
	return render(request, 'answers.html', context)


#	questionForm = QuestionForm(initial={'quiz':quizid})
#	quiz = Quiz.objects.get(id=quizid)
#	questionList = Question.objects.filter(quiz=quizid)
#	context = {'questionList': questionList,
#			'quiz' : quiz,
#			'questionForm': questionForm,}
#	return render(request, 'questions.html', context)

def postquiz(request):
	quizname = request.POST['quizname']
	quiz = Quiz(name=quizname)
	quiz.save()
	quiz = Quiz.objects.get(name=quizname)
	return HttpResponseRedirect('/quizzes/' + str(quiz.id) + '/')

def postquestion(request, quizid): #, questionid):
	questionForm = QuestionForm(request.POST)
	if questionForm.is_valid():
		#question = Question(string=questionForm.cleaned_data['string'],
		#	quiz=quizid)
		question = questionForm.save()
		return HttpResponseRedirect(reverse(answers, args=(quizid, question.id,)))
	#quiz = Quiz.objects.get(name = quizname)
	#question = Question(string=request.Post['questionstring'], quiz=quiz)
	#question.save()
	return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/') #I think I need ID!

def postanswer(request, quizid, questionid):
	answerForm = AnswerForm(request.POST)
	if answerForm.is_valid():
		answer = answerForm.save()
		return HttpResponseRedirect('/quizzes/' + str(quizid) + '/' + str(questionid) + '/') #I think I need ID!
	else:
		return HttpResponse("This form is not valid")

class QuizListView(ListView):
	model = Quiz
	def get_context_data(self, **kwargs):
		context = super(QuizListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context
