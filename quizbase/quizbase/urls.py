"""App urls for Quizbase.  See all urls in quiz/urls.py."""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('quiz.urls')),
]
