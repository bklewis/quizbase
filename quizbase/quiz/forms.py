from django import forms

from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('string', 'quiz')
		widgets = {'string': forms.Textarea(),
				'quiz': forms.HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['string'].label = "Add a new question"

class AnswerForm(forms.ModelForm):

	class Meta:
		model = Answer
		fields = ('string', 'question', 'value')
		widgets = {'string': forms.Textarea(),
			'value': forms.ChoiceField(choices=Answer.VALUE_CHOICES),
			'question': forms.HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['string'].label = "Answer Text"
		self.fields['value'].label = "Answer Value"
