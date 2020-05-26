from django import forms
from app.models import Question, User, Profile, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        if ' ' in password:
            raise forms.ValidationError('Password contains space.', code='space in password')

        return password

class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput)
    #avatar = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        if ' ' in password:
            raise forms.ValidationError('Password contains space.', code='space in password')

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')
        if ' ' in email:
            raise forms.ValidationError('Email contains space.', code='space in email')

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # TODO: checking size of avatar file
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeatPassword = cleaned_data.get('repeatPassword')

        if password != repeatPassword:
            raise forms.ValidationError('These passwords do not match.')

        #image = cleaned_data.get('avatar')
        #if image:
         #   if image.size > 4 * 1024 * 1024:
         #       raise forms.ValidationError("Image file too large ( > 4mb )")
        #else:
         #   raise forms.ValidationError("Couldn't read uploaded image")

    def save(self, commit=True):
        newUser = User(username=self.cleaned_data.get('username'),
                       email=self.cleaned_data.get('email'),
                       password=self.cleaned_data.get('password'))
        newProfile = Profile(user=newUser)
        if commit:
            newUser.save()
            newProfile.save()
        return newUser, newProfile


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, user, question, *args, **kwargs):
        self.user = user
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = Answer(text=self.cleaned_data.get('text'))
        answer.author = self.user
        answer.question = self.question
        if commit:
            answer.save()
        return answer


class SettingsForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    #avatar = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')
        if ' ' in email:
            raise forms.ValidationError('Email contains space.', code='space in email')

        return email

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        newUser = User(username=self.cleaned_data.get('username'),
                       email=self.cleaned_data.get('email'))
        newProfile = Profile(user=newUser)
        if commit:
            newUser.save()
            newProfile.save()
        return newUser, newProfile


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    #TODO: change user to author (mistake in DB tables)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question(title=self.cleaned_data.get('title'),
                            text=self.cleaned_data.get('text'))
        question.author = self.user
        if commit:
            question.save()

        question.tags.set(self.cleaned_data.get('tags'))
        if commit:
            question.save()
        return question
