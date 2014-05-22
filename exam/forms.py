from django.forms.widgets import PasswordInput, TextInput
from captcha.fields import CaptchaField
from django.contrib.auth.forms import *

class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
