from django import forms
from app.models import Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question(**self.cleaned_data)
        profile = self.profile
        if commit:
            question.save()
        return question
