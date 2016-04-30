from django import forms
from django.forms import formset_factory

from .models import Quiz, Question, Answer, Quiz_attempt, Answer_attempt


class QuestionForm(forms.ModelForm):

    """Create a question associated with a quiz."""

    class Meta:
        model = Question
        fields = ('string', 'quiz')
        widgets = {'string': forms.TextInput(),
                   'quiz': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['string'].label = "Add a new question"


class AnswerForm(forms.ModelForm):

    """Create an answer associated with a question/quiz."""

    class Meta:
        model = Answer
        fields = ('string', 'question', 'value')
        widgets = {'string': forms.TextInput(),
                   'question': forms.HiddenInput(),
                   'value': forms.Select(choices=Answer.VALUE_CHOICES)}

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['string'].label = "Answer Text"
        self.fields['value'].label = "Answer Value"
        self.fields['value'].queryset = Answer.VALUE_CHOICES


class AttemptForm(forms.Form):

    """Allow a user to post their response to question."""

    answers = forms.ModelMultipleChoiceField(queryset=Answer.objects.none(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, question, *args, **kwargs):
        super(AttemptForm, self).__init__(*args, **kwargs)
        self.question = question
        self.fields['answers'].queryset = Answer.objects.filter(question=question)
        self.fields['answers'].label = ""
