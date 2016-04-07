from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils import timezone

from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from .models import Quiz

# Create your views here.

@login_required(login_url='/login/')
def index(request):
	return render(request, 'home.html')
	#return HttpResponse("Welcome to QuizBase")

def base(request):
	return render(request, 'base.html')
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

@login_required(login_url='/login/')
def quizzes(request):
	quizList = Quiz.objects.order_by('name')
	context = {'quizList': quizList,}
	return render(request, 'quizzes.html', context)
	#output = ', '.join([q.name for q in quizList])
	#return HttpResponse(output)

#@login_required(login_url='/login/')
class QuizListView(ListView):
	model = Quiz
	def get_context_data(self, **kwargs):
		context = super(QuizListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

def creating(request):
	return HttpResponse("CREATING")
