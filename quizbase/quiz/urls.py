from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^$', views.post_list, name='post_list'),

	url(r'^quizme/(?P<quizid>[0-9]+)/$', views.quizready, name='quizready'),
	url(r'^quizme/', views.quizme, name='quizme'),

	url(r'^quizzes/(?P<quizid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.answers, name='answers'),
	url(r'^quizzes/(?P<quizid>[0-9]+)/$', views.questions, name='questions'),
#	url(r'^quizzes/(?P<quizname>\w+)/$', views.questions, name='questions'),
	url(r'^quizzes/', views.quizzes, name='quizzes'),
	url(r'^postquiz/', views.postquiz, name='postquiz'),
	url(r'^postquestion/(?P<quizid>[0-9]+)/$', views.postquestion, name='postquestion'),
	url(r'^postanswer/(?P<quizid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.postanswer, name='postanswer'),
	url(r'^login/', login, {'template_name': 'login.html'}),
	url(r'^logout/', logout),
	url(r'^base/', views.base, name='base'),
	url(r'^quizze/', views.QuizListView.as_view(), name='quiz-list'),
]
