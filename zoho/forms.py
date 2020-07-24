from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput,EmailInput,PasswordInput

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email Address'}))
    mob = forms.IntegerField(required=False,help_text='optional.',widget=forms.TextInput(attrs={'class': 'form-control','placeholder' : "Mobile Number"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'mob', 'password1', 'password2', )

        widgets = {
            'username': TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
            }
