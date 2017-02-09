from django import forms


class UserForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()
