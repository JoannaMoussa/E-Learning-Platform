from django.shortcuts import render
from django import forms
from django.core import validators
from PIL import Image
from .models import User, Course


# Creating Django forms
class SignUpForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=150,
                                 required=True,
                                 widget=forms.TextInput())
    last_name = forms.CharField(label="Last Name",
                                max_length=150,
                                required=True,
                                widget=forms.TextInput())
    username = forms.CharField(label="Username",
                               max_length=150,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(label="Email",
                             required=True,
                             widget=forms.EmailInput())
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password",
                                       widget=forms.PasswordInput())
    role = forms.ChoiceField(label="You are a",
                             widget=forms.RadioSelect,
                             choices=User.ROLE_CHOICES)
    title = forms.CharField(label="Title",
                            max_length=120,
                            widget=forms.TextInput())
    about_me = forms.CharField(label="About me",
                               max_length=950,
                               required=True,
                               widget=forms.Textarea())


class LogInForm(forms.Form):
    email = forms.EmailField(label="Email",
                             required=True,
                             widget=forms.EmailInput())
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput())


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=150,
                                 required=True,
                                 widget=forms.TextInput())
    last_name = forms.CharField(label="Last Name",
                                max_length=150,
                                required=True,
                                widget=forms.TextInput())
    username = forms.CharField(label="Username",
                               max_length=150,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(label="Email",
                             disabled=True,
                             widget=forms.EmailInput())
    title = forms.CharField(label="Title",
                            max_length=120,
                            widget=forms.TextInput())
    about_me = forms.CharField(label="About me",
                               max_length=950,
                               required=True,
                               widget=forms.Textarea())


class CreateCourseForm(forms.Form):
    title = forms.CharField(label="Title",
                            max_length=80,
                            required=True,
                            widget=forms.TextInput())
    image = forms.ImageField()
    category = forms.ChoiceField(label="Course Category",
                                 widget=forms.RadioSelect,
                                 choices=Course.CATEGORY_CHOICES)
    short_description = forms.CharField(label="Short Description",
                                        required=True,
                                        max_length=200,
                                        widget=forms.Textarea())
    long_description = forms.CharField(label="About this course",
                                       required=True,
                                       max_length=2000,
                                       widget=forms.Textarea())
    duration = forms.IntegerField(label="Course's Duration",
                                  required=True,
                                  min_value=2,
                                  max_value=24,
                                  widget=forms.NumberInput())
    language = forms.ChoiceField(label="Language",
                                 widget=forms.RadioSelect,
                                 choices=Course.LANGUAGE_CHOICES)
    level = forms.ChoiceField(label="Level",
                              widget=forms.RadioSelect,
                              choices=Course.LEVEL_CHOICES)
    certificate = forms.BooleanField(label="Certificate Upon Completion",
                                     widget=forms.CheckboxInput)
    passing_grade = forms.IntegerField(label="Passing Grade",
                                       required=True,
                                       min_value=50,
                                       max_value=100,
                                       widget=forms.NumberInput())
