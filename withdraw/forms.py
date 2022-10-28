from django import forms

class WithdrawForm(forms.Form):
    jumlah = forms.DecimalField()
