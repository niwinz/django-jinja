from django import forms

class TestForm(forms.Form):
    name = forms.CharField(max_length=2)
