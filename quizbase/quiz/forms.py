from django import forms

from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):
#	string = forms.CharField(widget=forms.TextArea, max_len=1000, label="question", help_text="Please enter question name")
#	quiz = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Question
		fields = ('string', 'quiz')
		widgets = {'string': forms.Textarea(),
				'quiz': forms.HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['string'].label = "Add a new question"

