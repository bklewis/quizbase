from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from .models import Quiz

# Create your views here.

def index(request):
	return render(request, 'home.html')
	#return HttpResponse("Welcome to QuizBase")

def create(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'GET':
		quizList = Quiz.objects.order_by('name')
		#output = ', '.join([q.name for q in quizList])
		#return HttpResponse(output)
		#template = loader.get_template('create.html')
		context = {'quizList': quizList,}
		#return HttpResponse(template.render(context, request))
		return render(request, 'create.html', context)
		#return render_to_response(request, 'create.html', c)
		# https://docs.djangoproject.com/en/1.8/ref/csrf/#how-to-use-it

	elif request.method == 'POST':
		quiz = Quiz(name = request.POST['quizname'])
		quiz.save()
		return HttpResponse("post!")

def quizzes(request):
	quizList = Quiz.objects.order_by('name')
	#context = {'quizList': quizList,}
	#return render(request, 'create.html', context)
	output = ', '.join([q.name for q in quizList])
	return HttpResponse(output)

def login(request):
	return HttpResponse("login")


def creating(request):
	return HttpResponse("CREATING")
