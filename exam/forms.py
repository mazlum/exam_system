from django.forms.widgets import PasswordInput, TextInput
from captcha.fields import CaptchaField
from django.contrib.auth.forms import *
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))


class UserCreateForm(UserCreationForm):
    captcha = CaptchaField()
    username = forms.CharField(label="Username", help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.", widget=TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put Username'}))
    password1 = forms.CharField(label="Password", widget=PasswordInput(attrs={'class': 'form-control','placeHolder': 'Put Password'}))
    password2 = forms.CharField(label="Password Confirmation", help_text="Enter the same password as above, for verification.", widget=PasswordInput(attrs={'class': 'form-control', 'placeHolder': 'Put Password Again'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put Last Name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put E-mail'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Put Last Name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(id=self.instance.id).count():
            raise forms.ValidationError(u'Username must be unique.')
        return username


class ValidatingPasswordChangeForm(PasswordChangeForm):
    MIN_LENGTH = 4

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")

        # ... any other validation you want ...

        return password1