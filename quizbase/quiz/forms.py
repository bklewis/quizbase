from django import forms

from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('string', 'quiz')
		widgets = {'string': forms.Textarea(),
				'quiz': forms.HiddenInput()}
