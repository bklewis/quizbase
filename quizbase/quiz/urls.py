from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^$', views.post_list, name='post_list'),
#	url(r'^create/', views.create, name='create'),
	url(r'^create/', views.create, name='create'),
	url(r'^quizzes/', views.quizzes, name='quizzes'),
]
