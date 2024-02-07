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
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db.models.functions import Length
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

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
                                 widget=forms.TextInput(attrs={'class': 'edit-profile-form__input'}))
    last_name = forms.CharField(max_length=150,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'edit-profile-form__input'}))
    username = forms.CharField(disabled=True,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'edit-profile-form__input'}))
    email = forms.EmailField(disabled=True,
                             required=False,
                             widget=forms.EmailInput(attrs={'class': 'edit-profile-form__input'}))
    title = forms.CharField(required=False,
                            max_length=120,
                            widget=forms.TextInput(attrs={'class': 'edit-profile-form__input'}))
    about_me = forms.CharField(max_length=950,
                               required=True,
                               widget=forms.Textarea(attrs={'class': 'edit-profile-form__input edit-profile-form__input_textarea'}))


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
                    ### This is a temporary behavior to limit courses created when the website is public
                    messages.warning(request, "Creating instructors disabled in production.")
                    return render(request, "courses_platform/signup.html", {
                        "SignUpForm": filled_form
                    })
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
    courses = Course.objects.all()
    top_courses = sorted(
        courses, key=lambda course: course.enrolled_students.count(), reverse=True)[:6]
    return render(request, "courses_platform/index.html", {
        "top_courses": top_courses
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
        messages.error(request, "Only instructors can access that page")
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

            for options in processed_all_options:
                if len(options) <= 1:
                    return response_with_error(
                        "Make sure to specify more than 1 option for every question")
                for element in options:
                    if element == "":
                        return response_with_error(
                            "There is an empty option (An option list should not end with a coma)")

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

            new_course.save()
            messages.success(request, "Your course was created successfully!")
            return HttpResponseRedirect(reverse("user_profile", kwargs={"user_id": current_user.id}))

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
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "Invalid course id")
        return HttpResponseRedirect(reverse("index"))

    current_user = request.user
    # Verify that current user is allowed to access the quiz
    if current_user.role != User.STUDENT:
        messages.error(request, "You must be a student to take the quiz")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))
    if course not in current_user.enrolled_courses.all():
        messages.error(
            request, "You must be enrolled in this course to take this quiz")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))
    if current_user in course.passers.all():
        messages.warning(request, "You already passed this quiz")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))

    # Open the course's quiz file
    quiz_filename = f"{course.instructor.username}_{course.id}.json"
    quiz_filepath = settings.QUIZES_ROOT / quiz_filename
    if os.path.exists(quiz_filepath):
        quiz_file = open(quiz_filepath)
    else:
        messages.error(
            request, "Error loading quiz")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))
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


def all_courses(request):
    return render(request, "courses_platform/all_courses.html", {
        "Course": Course()
    })


@require_GET
def all_courses_api(request):
    # filter courses
    FILTER_OPTIONS = ["category", "duration", "language", "level"]
    filter_param = {}
    for option in FILTER_OPTIONS:
        if request.GET.get(option) is not None:
            if option == "duration":
                # Conditions are seperated with commas. e.g.: gte-4,lt-8
                duration_conditions = request.GET.get(option).split(",")
                for element in duration_conditions:
                    operator, value = element.split("-")
                    filter_param[f"{option}__{operator}"] = int(value)
            else:
                filter_param[option] = request.GET.get(option)
    filtered_courses = Course.objects.filter(**filter_param)

    # Sort courses
    sort_criteria = request.GET.get("sort")
    if sort_criteria not in ["title", "-title", "creation_date", "popularity"]:
        return JsonResponse({"error": "An error occured"}, status=400)

    if sort_criteria == "popularity":
        filtered_sorted_courses = sorted(
            filtered_courses, key=lambda course: course.enrolled_students.count(), reverse=True)
    else:
        filtered_sorted_courses = filtered_courses.order_by(sort_criteria)

    return JsonResponse([course.serialize() for course in filtered_sorted_courses], safe=False)


def course_page(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "Invalid course id")
        return HttpResponseRedirect(reverse("index"))

    enrolled_students = course.enrolled_students.order_by("last_name")
    same_category_courses = Course.objects.filter(
        category=course.category).exclude(id=course.id)[:3]
    return render(request, "courses_platform/course_page.html", {
        "course": course,
        "enrolled_students": enrolled_students,
        "same_category_courses": same_category_courses
    })


@login_required(login_url='/signin')
def course_enroll(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "Invalid course id")
        return HttpResponseRedirect(reverse("index"))

    if request.user.role == User.INSTRUCTOR:
        messages.error(request, "Only students can enroll")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))

    if request.user in course.enrolled_students.all():
        messages.error(request, "An error occured")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))

    course.enrolled_students.add(request.user)
    messages.success(request, "Enrolment Successfull")
    return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))


def user_profile(request, user_id):
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid user id")
        return HttpResponseRedirect(reverse("index"))

    if current_user.role == User.STUDENT:
        passed_courses = current_user.courses_passed.all().order_by("title")
        enrolled_not_passed_courses = []
        enrolled_courses = current_user.enrolled_courses.all().order_by("title")
        for course in enrolled_courses:
            if course not in current_user.courses_passed.all():
                enrolled_not_passed_courses.append(course)
        return render(request, "courses_platform/student_profile.html", {
            "current_user": current_user,
            "passed_courses": passed_courses,
            "enrolled_not_passed_courses": enrolled_not_passed_courses
        })
    elif current_user.role == User.INSTRUCTOR:
        courses_taught = current_user.courses_taught.all()
        total_nb_students_enrolled = 0
        for course in courses_taught:
            total_nb_students_enrolled += len(course.enrolled_students.all())
        return render(request, "courses_platform/instructor_profile.html", {
            "current_user": current_user,
            "total_nb_students_enrolled": total_nb_students_enrolled
        })
    else:
        messages.error(request, "An error occured")
        return HttpResponseRedirect(reverse("index"))


def completed_courses(request, user_id):
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid user id")
        return HttpResponseRedirect(reverse("index"))

    passed_courses = current_user.courses_passed.all().order_by("title")

    return render(request, "courses_platform/completed_courses.html", {
        "current_user": current_user,
        "passed_courses": passed_courses
    })


def enrolled_courses(request, user_id):
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid user id")
        return HttpResponseRedirect(reverse("index"))

    enrolled_not_passed_courses = []
    enrolled_courses = current_user.enrolled_courses.all().order_by("title")
    for course in enrolled_courses:
        if course not in current_user.courses_passed.all():
            enrolled_not_passed_courses.append(course)

    return render(request, "courses_platform/enrolled_courses.html", {
        "current_user": current_user,
        "enrolled_not_passed_courses": enrolled_not_passed_courses
    })


@login_required(login_url='/signin')
def edit_profile(request):
    if request.method == "GET":
        user_infos = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "title": request.user.instructor_title if request.user.role == request.user.INSTRUCTOR else None,
            "about_me": request.user.about
        }
        # Django disregards the disabled fields, so the only way to set their initial values is to use ".initial"
        filled_form = EditProfileForm(user_infos)
        filled_form.fields['email'].initial = request.user.email
        filled_form.fields['username'].initial = request.user.username

        return render(request, "courses_platform/edit_profile.html", {
            "EditProfileForm": filled_form
        })

    elif request.method == "POST":
        edits_data = EditProfileForm(request.POST)
        if edits_data.is_valid():
            if edits_data.cleaned_data["first_name"] != request.user.first_name:
                request.user.first_name = edits_data.cleaned_data["first_name"]
            if edits_data.cleaned_data["last_name"] != request.user.last_name:
                request.user.last_name = edits_data.cleaned_data["last_name"]
            if request.user.role == request.user.INSTRUCTOR:
                if edits_data.cleaned_data["title"] != request.user.instructor_title:
                    request.user.instructor_title = edits_data.cleaned_data["title"]
            if edits_data.cleaned_data["about_me"] != request.user.about:
                request.user.about = edits_data.cleaned_data["about_me"]
            request.user.save()

            messages.success(request, "You edited your profile successfully")
            return HttpResponseRedirect(reverse("user_profile", kwargs={"user_id": request.user.id}))


@login_required(login_url='/signin')
def get_certificate(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "Invalid course id")
        return HttpResponseRedirect(reverse("index"))

    if not course.certificate:
        messages.error(request, "This course does not provide a certificate")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))

    current_user = request.user

    if current_user not in course.passers.all():
        messages.error(request, "You did not pass this course")
        return HttpResponseRedirect(reverse("course_page", kwargs={"course_id": course_id}))

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    WIDTH, HEIGHT = 11 * inch, 8.5 * inch
    certificate = canvas.Canvas(buffer, pagesize=(WIDTH, HEIGHT))

    # Draw things on the PDF. Here's where the PDF generation happens.
    COLOR_LIGHT = (88/255, 91/255, 238/255)
    COLOR_DARK = (49/255, 46/255, 129/255)
    FONT = "Times-Roman"
    signature_height = 100
    signature_ratio = 1.2
    signature_width = signature_height * signature_ratio
    stamp_width_height = 150

    certificate.setTitle(
        f"{course.title.replace(' ', '_')}_certificate_{current_user.username}")

    def write_centered_text(font_size, rgb, y_coord, text):
        certificate.setFont(FONT, font_size)
        certificate.setFillColorRGB(*rgb)
        certificate.drawCentredString(WIDTH//2, y_coord, text)

    certificate.setStrokeColorRGB(*COLOR_DARK)
    certificate.setLineWidth(4)
    certificate.rect(10, 10, WIDTH-20, HEIGHT-20, stroke=1)

    certificate.drawImage(settings.MEDIA_ROOT / "certificate_images" / "certificate_stamp.png",
                          0, HEIGHT-stamp_width_height-15, width=stamp_width_height, height=stamp_width_height, mask="auto")
    write_centered_text(20, COLOR_LIGHT, HEIGHT*0.9, "CourseMedia")
    write_centered_text(30, COLOR_DARK, HEIGHT*0.8,
                        "Certificate of Completion")
    write_centered_text(20, COLOR_LIGHT, HEIGHT*0.7, "This is to certify that")
    write_centered_text(40, COLOR_DARK, HEIGHT*0.6,
                        f"{current_user.first_name} {current_user.last_name}")
    write_centered_text(20, COLOR_LIGHT, HEIGHT*0.53,
                        f"has successfully completed a {course.duration} weeks course on")
    write_centered_text(30, COLOR_DARK, HEIGHT*0.43,
                        f"{course.title}")
    write_centered_text(20, COLOR_LIGHT, HEIGHT*0.33,
                        f"Delivered by {course.instructor.first_name} {course.instructor.last_name} on CourseMedia platform")
    certificate.drawImage(settings.MEDIA_ROOT / "certificate_images" / "signature.png",
                          WIDTH * 0.45, HEIGHT*0.11, width=signature_width, height=signature_height, mask="auto")
    write_centered_text(20, COLOR_DARK, HEIGHT*0.09, "Joanna Moussa")
    write_centered_text(20, COLOR_DARK, HEIGHT*0.05, "Founder of CourseMedia")

    # Close the PDF object cleanly, and we're done.
    # showPage() causes the canvas to stop drawing on the current page
    # and any further operations will draw on a subsequent page
    # (if there are any further operations -- if not no new page is created)
    certificate.showPage()
    certificate.save()  # it generates the PDF file and closes the canvas

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer,
                        as_attachment=True,
                        filename=f"{course.title.replace(' ', '_')}_certificate_{current_user.username}.pdf")
