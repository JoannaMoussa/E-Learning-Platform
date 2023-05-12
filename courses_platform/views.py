from django.shortcuts import render
from django import forms
from PIL import Image
from .models import User, Course
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import secrets

RANDOM_STR = secrets.token_hex(8)


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
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'signup-form__input'}))
    confirm_password = forms.CharField(required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'signup-form__input'}))
    role = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'signup-form__input'}),
                             choices=User.ROLE_CHOICES)
    title = forms.CharField(max_length=120,
                            required=False,
                            widget=forms.TextInput(attrs={'class': 'signup-form__input hidden-element'}))
    about_me = forms.CharField(max_length=950,
                               required=True,
                               widget=forms.Textarea(attrs={'class': 'signup-form__input signup-form__input_textarea'}))


class SignInForm(forms.Form):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'signin-form__input'}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'signin-form__input'}))


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150,
                                 required=True,
                                 widget=forms.TextInput())
    last_name = forms.CharField(max_length=150,
                                required=True,
                                widget=forms.TextInput())
    username = forms.CharField(max_length=150,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(disabled=True,
                             widget=forms.EmailInput())
    title = forms.CharField(required=False,
                            max_length=120,
                            widget=forms.TextInput())
    about_me = forms.CharField(max_length=950,
                               required=True,
                               widget=forms.Textarea())


class CreateCourseForm(forms.Form):
    title = forms.CharField(required=True,
                            min_length=10,
                            max_length=80,
                            widget=forms.TextInput(attrs={'class': 'createcourse-form__input'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'createcourse-form__input createcourse-form__input-imgfield'}))
    category = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.CATEGORY_CHOICES)
    short_description = forms.CharField(required=True,
                                        min_length=50,
                                        max_length=200,
                                        widget=forms.Textarea(attrs={'class': 'createcourse-form__input createcourse-form__input-text-area'}))
    long_description = forms.CharField(required=True,
                                       min_length=200,
                                       max_length=2000,
                                       widget=forms.Textarea(attrs={'class': 'createcourse-form__input createcourse-form__input-text-area'}))
    duration = forms.IntegerField(required=True,
                                  min_value=2,
                                  max_value=24,
                                  widget=forms.NumberInput(attrs={'class': 'createcourse-form__input createcourse-form__input-sm'}))
    language = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.LANGUAGE_CHOICES)
    level = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={'class': 'createcourse-form__input'}),
        choices=Course.LEVEL_CHOICES)
    certificate = forms.BooleanField(required=False, widget=forms.CheckboxInput(
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
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "courses_platform/signin.html", {
            "signInForm": SignInForm()
        })


def index(request):
    return render(request, "courses_platform/index.html", {
        "authenticated_user": request.user
    })


def question_body_validator(question_body):
    return len(question_body) >= 10


@login_required(login_url='/signin')
def create_course(request):
    def response_with_error(msg):
        messages.error(
            request, msg)
        return render(request, "courses_platform/create_course.html", {
            "createCourseForm": filled_form,
            "quiz_data": zip(range(len(all_questions)), all_questions, all_options, all_correct_options),
            "get_request": False
        })

    current_user = request.user
    # make sure that only instructors can access that page
    if current_user.role != User.INSTRUCTOR:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        # get the values of CreateCourseForm() fileds
        filled_form = CreateCourseForm(request.POST, request.FILES)

        # get the values of the quiz questions fields
        all_questions = request.POST.getlist('question_body')
        all_options = request.POST.getlist('options')
        all_correct_options = request.POST.getlist('correct_option')

        if filled_form.is_valid():
            new_course = Course()
            new_course.instructor = current_user
            new_course.title = filled_form.cleaned_data["title"]
            new_course.image = filled_form.cleaned_data["image"]
            new_course.category = int(filled_form.cleaned_data["category"])
            new_course.short_description = filled_form.cleaned_data["short_description"]
            new_course.long_description = filled_form.cleaned_data["long_description"]
            new_course.duration = filled_form.cleaned_data["duration"]
            new_course.language = int(filled_form.cleaned_data["language"])
            new_course.level = int(filled_form.cleaned_data["level"])

            # and request.POST["prerequisite"].isnumeric():
            if request.POST["prerequisite"] != "":
                try:
                    course_id = int(request.POST["prerequisite"])
                except ValueError:
                    return response_with_error(
                        "The id of the prerequisite course is invalid")
                course_exists = Course.objects.filter(id=course_id).exists()
                if course_exists:
                    prerequisite_course = Course.objects.get(id=course_id)
                    # An instructor can only choose prerequisite courses from his courses
                    if prerequisite_course.instructor == current_user:
                        new_course.prerequisite = prerequisite_course
                    else:
                        return response_with_error(
                            "The id of the prerequisite course is invalid")

            new_course.certificate = filled_form.cleaned_data["certificate"]
            new_course.passing_grade = filled_form.cleaned_data["passing_grade"]
            new_course.save()

            # quiz section
            # extract all questions and check if they are valid
            all_questions = [question.strip() for question in all_questions]
            all_questions_validator_list = map(
                question_body_validator, all_questions)
            # if False in all_questions_validator_list:
            if not all(all_questions_validator_list):
                return response_with_error(
                    "The minimum length of the questions must be 10 characters")

            # extract all questions' options and check if they are valid
            if len(all_options) != len(all_questions):
                return response_with_error(
                    "You should specify options for every question")
            # when spliting the options, I should handle the case where the user
            # typed "\," to say that the comma is not meant to seperate options.
            # so first, in the original string coming from the request, I replaced all "\," with a
            # random string, to mask the comma from the split(",") method. Then I applied the split(",")
            # After that, in every element from the splitted list, i replaced the random string with a comma
            processed_all_options = []
            for options in all_options:
                options = options.replace("\\,", RANDOM_STR)
                options = options.split(",")
                options = [element.strip().replace(RANDOM_STR, ",")
                           for element in options]
                processed_all_options.append(options)
                print(processed_all_options)

            for options in processed_all_options:
                if len(options) <= 1:
                    return response_with_error(
                        "Make sure to specify more than 1 option for every question")
                for element in options:
                    if element == "":
                        return response_with_error(
                            "Make sure none of the options are empty.")

            # extract all correct options and check if they are valid
            if len(all_correct_options) != len(all_questions):
                return response_with_error(
                    "Make sure to specify a correct option for every question")
            # cast the index of the correct option to an integer
            try:
                processed_all_correct_options = [int(correct_option.strip()) - 1
                                                 for correct_option in all_correct_options]
            except ValueError:
                return response_with_error(
                    "Make sure the index of the correct option is valid")
            for i in range(len(processed_all_correct_options)):
                if not (0 <= processed_all_correct_options[i] < len(processed_all_options[i])):
                    return response_with_error(
                        "Make sure the index of the correct option is valid")

            # data to be written in the quiz file
            quiz_data = {
                "all_questions": all_questions,
                "all_options": processed_all_options,
                "all_correct_options": processed_all_correct_options,
            }
            filename = f"{current_user.username}_{new_course.id}.json"
            filepath = settings.QUIZES_ROOT / filename
            if not settings.QUIZES_ROOT.exists():
                settings.QUIZES_ROOT.mkdir()
            # write data
            json.dump(quiz_data, open(filepath, "w"))

            messages.success(request, "Your course was created successfully!")
            # TODO: redirect to instructor profile page
            return HttpResponseRedirect(reverse("index"))

        else:  # form is invalid
            return response_with_error(
                "The form is invalid. Make sure you followed all instructions")

    else:  # Get request
        return render(request, "courses_platform/create_course.html", {
            "createCourseForm": CreateCourseForm(),
            "get_request": True
        })


@login_required(login_url='/signin')
def quiz(request, course_id):
    # try to get the course
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "The course id is not valid")
        return HttpResponseRedirect(reverse("index"))

    current_user = request.user
    # Verify that current user is allowed to access or submit the quiz
    if current_user.role != User.STUDENT:
        messages.error(request, "You must be a student to take the quiz")
        # TODO: redirect to the course page instead of the index page
        return HttpResponseRedirect(reverse("index"))
    if course not in current_user.enrolled_courses.all():
        messages.error(
            request, "You must be enrolled in this course to take this quiz")
        # TODO: redirect to the course page instead of the index page
        return HttpResponseRedirect(reverse("index"))
    if current_user in course.passers.all():
        messages.warning(request, "You already passed this quiz")
        # TODO: redirect to the course page instead of the index page
        return HttpResponseRedirect(reverse("index"))

    # Open the course's quiz file
    quiz_filename = f"{course.instructor.username}_{course.id}.json"
    quiz_filepath = settings.QUIZES_ROOT / quiz_filename
    quiz_file = open(quiz_filepath)
    # save json string as python dictionary
    quiz_data = json.load(quiz_file)

    # Processing all_options
    # This is useful in order to put the value and id of the option input field in html
    quiz_data["all_options"] = [
        zip(range(1, len(options)+1), options) for options in quiz_data["all_options"]]

    if request.method == "GET":
        return render(request, "courses_platform/quiz.html", {
            "course": course,
            "quiz_data": zip(range(1, len(quiz_data["all_questions"]) + 1),
                             quiz_data["all_questions"],
                             quiz_data["all_options"])
        })

    if request.method == "POST":
        passed = False
        correct_answers = 0
        for i in range(len(quiz_data["all_correct_options"])):
            try:
                current_answer = int(request.POST[f"answer-{i+1}"])
            except (KeyError, ValueError):
                messages.error(
                    request, "An error occured, please resubmit the quiz")
                return render(request, "courses_platform/quiz.html", {
                    "course": course,
                    "quiz_data": zip(range(1, len(quiz_data["all_questions"]) + 1),
                                     quiz_data["all_questions"],
                                     quiz_data["all_options"])
                })
            if quiz_data["all_correct_options"][i] == current_answer - 1:
                correct_answers += 1
        grade = round(
            (correct_answers / len(quiz_data["all_correct_options"])) * 100)
        if grade >= course.passing_grade:
            passed = True
            course.passers.add(current_user)
        return render(request, "courses_platform/quiz_result.html", {
            "course": course,
            "passed": passed,
            "grade": grade
        })
