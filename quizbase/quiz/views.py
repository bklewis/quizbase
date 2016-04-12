from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils import timezone

from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from .models import Quiz, Question, Answer

#TODO: Deal with Quiz names with spaces and non-alpha characters

# Create your views here.

@login_required(login_url='/login/')
def index(request):
	return render(request, 'index.html')

def base(request):
	return render(request, 'base.html')

@login_required(login_url='/login/')
def create(request):
	if request.method == 'GET':
		quizList = Quiz.objects.order_by('name')
		context = {'quizList': quizList,}
		return render(request, 'create.html', context)

	elif request.method == 'POST':
		quiz = Quiz(name = request.POST['quizname'])
		quiz.save()
		return HttpResponse("post!")

@login_required(login_url='/login/')
def quizzes(request):
	quizList = Quiz.objects.order_by('name')
	context = {'quizList': quizList,}
	return render(request, 'quizzes.html', context)

def questions(request, quizid):
	quiz = Quiz.objects.get(id=quizid)
	questionList = Question.objects.filter(quiz=quiz.id)
	context = {'questionList': questionList,
			'quizName' : quiz.name,}
	return render(request, 'questions.html', context)

def postquiz(request):
	quizname = request.POST['quizname']
	quiz = Quiz(name=quizname)
	quiz.save()
	quiz = Quiz.objects.get(name=quizname)
	return HttpResponseRedirect('/quizzes/' + str(quiz.id) + '/')

def postquestion(request, quizname):
	quiz = Quiz.objects.get(name = quizname)
	question = Question(string=request.Post['questionstring'], quiz=quiz)
	question.save()
	return HttpResponseRedirect('/quizzes/') #I think I need ID!

#@login_required(login_url='/login/')
class QuizListView(ListView):
	model = Quiz
	def get_context_data(self, **kwargs):
		context = super(QuizListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context
