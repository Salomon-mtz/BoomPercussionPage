from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")


class NewPlayerForm(forms.ModelForm):

    level = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = Player
        fields = ("level", "country")