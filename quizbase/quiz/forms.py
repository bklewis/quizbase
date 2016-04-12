from django import forms

from .models import Quiz, Question, Answer

class PostQuestion(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('string')
