from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^$', views.post_list, name='post_list'),
#	url(r'^create/', views.create, name='create'),
	url(r'^create/', views.create, name='create'),
	url(r'^quizzes/', views.quizzes, name='quizzes'),
	url(r'^postquiz/', views.postquiz, name='postquiz'),
	url(r'^login/', login, {'template_name': 'login.html'}),
	url(r'^logout/', logout),
	url(r'^base/', views.base, name='base'),
	url(r'^quizze/', views.QuizListView.as_view(), name='quiz-list'),
]
