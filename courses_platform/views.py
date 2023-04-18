from django.shortcuts import render
from django import forms
from django.core import validators


# Creating a Django form for sign up
class SignUpForm(forms.Form):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor")
    ]

    first_name = forms.CharField(label="First Name",
                                 max_length=150,
                                 required=True)
    last_name = forms.CharField(label="Last Name",
                                max_length=150,
                                required=True)
    username = forms.CharField(label="Username",
                               max_length=150,
                               required=True)
    email = forms.EmailField(label="Email",
                             required=True,
                             validators=[validators.EmailValidator()])
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password",
                                       widget=forms.PasswordInput())
    role = forms.ChoiceField(label="You are a:",
                             widget=forms.RadioSelect, choices=ROLE_CHOICES)
    title = forms.CharField(label="Title",
                            max_length=120)
    about_me = forms.CharField(label="About me",
                               max_length=950,
                               required=True,
                               widget=forms.Textarea(attrs={'class': 'hello'}))


def index(request):
    return render(request, "courses_platform/index.html", {
        "SignUpForm": SignUpForm
    })
