from django import forms
from django.forms import formset_factory

from .models import Quiz, Question, Answer, Quiz_attempt, Answer_attempt


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
                   'question': forms.HiddenInput(),
                   'value': forms.Select(choices=Answer.VALUE_CHOICES)}

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['string'].label = "Answer Text"
        self.fields['value'].label = "Answer Value"
        self.fields['value'].queryset = Answer.VALUE_CHOICES


class AttemptForm(forms.Form):
    answers = forms.ModelMultipleChoiceField(queryset=Answer.objects.none(), widget=forms.CheckboxSelectMultiple())
    # question = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, question, *args, **kwargs):
        super(AttemptForm, self).__init__(*args, **kwargs)
        self.question = question
        # question = self.fields['question'].initial
        self.fields['answers'].queryset = Answer.objects.filter(question=question)
        self.fields['answers'].label = ""

    # def save(self, commit=True):
    #    instance = super(AttemptForm, self).save(commit=False)
    #    for
