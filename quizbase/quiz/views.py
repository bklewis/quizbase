from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from .models import Quiz

# Create your views here.

def index(request):
	return render(request, 'home.html')
	#return HttpResponse("Welcome to QuizBase")

@login_required(login_url='/login/')
def create(request):
	if request.method == 'GET':
		quizList = Quiz.objects.order_by('name')
		#output = ', '.join([q.name for q in quizList])
		#return HttpResponse(output)
		#template = loader.get_template('create.html')
		context = {'quizList': quizList,}
		#return HttpResponse(template.render(context, request))
		return render(request, 'create.html', context)
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
"""
def login(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		auth.login(request, user)
		#return HttpResponseRedirect("/account/loggedin")
		return HttpResponse("You are now logged in!")
	else:
		#return HttpResponseRedirect("/account/invalid")
		return HttpResponse("invalid account")
	#return HttpResponse("login")
"""

def creating(request):
	return HttpResponse("CREATING")
