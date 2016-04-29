from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [

    # Core URLs
    url(r'^$', views.index, name='index'),
    url(r'^login/', login, {'template_name': 'login.html'}),
    url(r'^logout/', logout, {'template_name': 'logout.html'}),
    url(r'^base/', views.base, name='base'),

    # Viewable URLs for taking a quiz
    url(r'^quizme/(?P<quizid>[0-9]+)/ready/$', views.quizready, name='quizready'),
    url(r'^quizme/(?P<qaid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.attempt, name='attempt'),
    url(r'^quizme/(?P<qaid>[0-9]+)/$', views.quizattempt, name='quizattempt'),
    url(r'^quizme/', views.quizme, name='quizme'),

    # POST URLs for taking a quiz
    url(r'^postquizready/(?P<quizid>[0-9]+)/$', views.postquizready, name='postquizready'),
    url(r'^postattempt/(?P<qaid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.postattempt, name='postattempt'),
    url(r'^postquizattept/(?P<qaid>[0-9]+)/$', views.postquizattempt, name='postquizattempt'),

    # URLs for finishing a quiz and seening results
    url(r'^finishquiz/(?P<qaid>[0-9]+)/$', views.finishquiz, name='finishquiz'),
    url(r'^results/$', views.results, name='results'),

    # Viewable URLs for creating quiz components
    url(r'^quizzes/(?P<quizid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.answers, name='answers'),
    url(r'^quizzes/(?P<quizid>[0-9]+)/$', views.questions, name='questions'),
    url(r'^quizzes/', views.quizzes, name='quizzes'),

    # POST URLs for creating quiz components
    url(r'^postquiz/', views.postquiz, name='postquiz'),
    url(r'^postquestion/(?P<quizid>[0-9]+)/$', views.postquestion, name='postquestion'),
    url(r'^postanswer/(?P<quizid>[0-9]+)/(?P<questionid>[0-9]+)/$', views.postanswer, name='postanswer'),

    # POST URLs for deleting quiz components
    url(r'^deletequiz/(?P<quizid>[0-9]+)/$', views.deletequiz, name='deletequiz'),
    url(r'^deletequestion/(?P<questionid>[0-9]+)/$', views.deletequestion, name='deletequestion'),
    url(r'^deleteanswer/(?P<answerid>[0-9]+)/$', views.deleteanswer, name='deleteanswer'),

]
