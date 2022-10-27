from django import forms
from django.contrib.auth.models import User

user = User.objects.all()

CHOICES_USER = user

CHOICES =(
    ("Plastik", "PLASTIK"),
    ("Elektronik", "ELEKTRONIK")
)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

class PrizeForm(forms.Form):
    nama = forms.CharField()
    poin = forms.DecimalField()
    stok = forms.DecimalField()
    desc = forms.CharField(widget=forms.Textarea)

class DepositForm(forms.Form):
    jenisSampah = forms.ChoiceField(choices = CHOICES)
    beratSampah = forms.DecimalField()