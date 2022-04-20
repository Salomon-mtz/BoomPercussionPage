from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player


# Create your forms here.

class NewUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ("name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewPlayerForm(forms.ModelForm):

    level = forms.IntegerField()

    class Meta:
        model = Player
        fields = ("level",)

    def save(self, commit=True):
        player = super(NewPlayerForm, self).save(commit=False)
        player.email = self.cleaned_data['email']
        if commit:
            player.save()
        return player