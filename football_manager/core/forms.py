from django import forms
from .models import Player
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'team', 'goals', 'assists', 'matches_played']

# SignUp Form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login Form
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']