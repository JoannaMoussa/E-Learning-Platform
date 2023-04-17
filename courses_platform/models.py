from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator


class User(AbstractUser):
    STUDENT = 1
    INSTRUCTOR = 2

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (INSTRUCTOR, "Instructor")
    ]

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    instructor_title = models.CharField(max_length=120, null=True, blank=True, validators=[
                                        MinLengthValidator(10), MaxLengthValidator(120)])
    about = models.TextField(max_length=950, validators=[
                             MinLengthValidator(40), MaxLengthValidator(950)])
    enrolled_courses = models.ManyToManyField(
        "Course", related_name="enrolled_students")


class Course(models.Model):
    ART_AND_CULTURE = 1
    COMMUNICATION = 2
    COMPUTER_SCIENCE = 3
    DESIGN = 4
    FOOD_AND_NUTRITION = 5
    LANGUAGE = 6
    MATH = 7
    SCIENCE = 8

    CATEGORY_CHOICES = [
        (ART_AND_CULTURE, "Art & Culture"),
        (COMMUNICATION, "Communication"),
        (COMPUTER_SCIENCE, "Computer Science"),
        (DESIGN, "Design"),
        (FOOD_AND_NUTRITION, "Food & Nutrition"),
        (LANGUAGE, "Language"),
        (MATH, "Math"),
        (SCIENCE, "Science"),
    ]

    ENGLISH = 1
    FRENCH = 2
    SPANISH = 3

    LANGUAGE_CHOICES = [
        (ENGLISH, "English"),
        (FRENCH, "French"),
        (SPANISH, "Spanish")
    ]

    instructor = models.ForeignKey(
        "User", on_delete=models.CASCADE)
    title = models.CharField(max_length=80, validators=[
                             MinLengthValidator(10), MaxLengthValidator(80)])
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    short_description = models.TextField(max_length=200, validators=[
                                         MinLengthValidator(50), MaxLengthValidator(200)])
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(24)])
    long_description = models.TextField(
        max_length=2000, validators=[MinLengthValidator(200), MaxLengthValidator(2000)])
    language = models.PositiveSmallIntegerField(choices=LANGUAGE_CHOICES)
    prerequisite = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True)
    certificate = models.BooleanField()
    passing_grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(100)])
    passers = models.ManyToManyField("User", related_name="courses_passed")
    creation_date = models.DateField(auto_now_add=True)
