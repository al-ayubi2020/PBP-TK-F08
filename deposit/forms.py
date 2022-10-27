from django import forms

CHOICES =(
    ("Plastik", "PLASTIK"),
    ("Elektronik", "ELEKTRONIK")
)

class DepositForm(forms.Form):
    jenisSampah = forms.ChoiceField(choices = CHOICES)
    beratSampah = forms.DecimalField()
