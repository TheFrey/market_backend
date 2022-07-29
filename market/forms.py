from django import forms
from django.contrib.auth.models import User
from .models import Comment, Category


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'rating')


class SearchForm(forms.Form):
    CHOICE = ((i.name, i.name) for i in Category.objects.all())
    query = forms.CharField()
    category = forms.ChoiceField(choices=CHOICE)
    price_up = forms.IntegerField(initial=1000)
    price_down = forms.IntegerField(initial=0)
