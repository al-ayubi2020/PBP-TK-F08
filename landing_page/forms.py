from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

class TestimoniForm(forms.Form):
    desc = forms.CharField(widget=forms.Textarea)