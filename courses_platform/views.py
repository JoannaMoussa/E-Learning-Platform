from django.shortcuts import render
from django import forms
from PIL import Image
from .models import User, Course
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Creating Django forms


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=150,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'signup-form__input'}))
    last_name = forms.CharField(max_length=150,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'signup-form__input'}))
    username = forms.CharField(max_length=150,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'signup-form__input'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'signup-form__input'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'signup-form__input'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'signup-form__input'}))
    role = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'signup-form__input'}),
                             choices=User.ROLE_CHOICES)
    title = forms.CharField(max_length=120,
                            required=False,
                            widget=forms.TextInput(attrs={'class': 'signup-form__input hidden-element'}))
    about_me = forms.CharField(max_length=950,
                               required=True,
                               widget=forms.Textarea(attrs={'class': 'signup-form__input signup-form__input_textarea'}))


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'signin-form__input'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'signin-form__input'}))


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
    title = forms.CharField(max_length=80,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'createcourse-form__input'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'createcourse-form__input createcourse-form__input-imgfield'}))
    category = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.CATEGORY_CHOICES)
    short_description = forms.CharField(required=True,
                                        max_length=200,
                                        widget=forms.Textarea(attrs={'class': 'createcourse-form__input createcourse-form__input-text-area'}))
    long_description = forms.CharField(required=True,
                                       max_length=2000,
                                       widget=forms.Textarea(attrs={'class': 'createcourse-form__input createcourse-form__input-text-area'}))
    duration = forms.IntegerField(required=True,
                                  min_value=2,
                                  max_value=24,
                                  widget=forms.NumberInput(attrs={'class': 'createcourse-form__input createcourse-form__input-sm'}))
    language = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.LANGUAGE_CHOICES)
    level = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.LEVEL_CHOICES)
    certificate = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'createcourse-form__input-checkbox'}))
    passing_grade = forms.IntegerField(required=True,
                                       min_value=50,
                                       max_value=100,
                                       widget=forms.NumberInput(attrs={'class': 'createcourse-form__input createcourse-form__input-sm'}))


def signup(request):
    if request.method == "POST":
        filled_form = SignUpForm(request.POST)

        if filled_form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if password != confirm_password:
                messages.error(
                    request, "Password and Confirm Password do not match")
                filled_form.fields['password'].widget.attrs['class'] += ' signup-form__input-red-border'
                filled_form.fields['confirm_password'].widget.attrs['class'] += ' signup-form__input-red-border'
                return render(request, "courses_platform/signup.html", {
                    "SignUpForm": filled_form
                })

            # Attempt to create new user
            try:
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                role = int(request.POST["role"])
                about = request.POST["about_me"]
                instructor_title = None
                if role == User.INSTRUCTOR:
                    if not request.POST["title"]:
                        messages.error(
                            request, "You should specify your title as an instructor")
                        filled_form.fields['title'].widget.attrs['class'] = 'signup-form__input signup-form__input-red-border'
                        return render(request, "courses_platform/signup.html", {
                            "SignUpForm": filled_form
                        })
                    else:
                        instructor_title = request.POST["title"]
                user = User.objects.create_user(username, email, password,
                                                first_name=first_name, last_name=last_name,
                                                role=role, about=about, instructor_title=instructor_title)
            except IntegrityError:
                messages.error(
                    request, "Username already taken")
                filled_form.fields['username'].widget.attrs['class'] += ' signup-form__input-red-border'
                return render(request, "courses_platform/signup.html", {
                    "SignUpForm": filled_form
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:  # form is invalid
            messages.error(request, "Invalid form")
            return render(request, "courses_platform/signup.html", {
                "SignUpForm": filled_form
            })
    else:  # GET request
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "courses_platform/signup.html", {
            "SignUpForm": SignUpForm()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def signin(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password")
            return render(request, "courses_platform/signin.html", {
                "signInForm": SignInForm()
            })
    else:  # GET request
        return render(request, "courses_platform/signin.html", {
            "signInForm": SignInForm()
        })


def index(request):
    return render(request, "courses_platform/index.html", {
        "authenticated_user": request.user
    })


def create_course(request):
    return render(request, "courses_platform/create_course.html", {
        "createCourseForm": CreateCourseForm()
    })
