from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STUDENT = 1
    INSTRUCTOR = 2

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (INSTRUCTOR, "Instructor")
    ]
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES)
    professional_title = models.CharField(
        max_length=120, null=True, blank=True)
    about = models.TextField(max_length=950)
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

    instructor = models.ForeignKey(
        "User", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    # check imagefield
    photo = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=100)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    short_description = models.TextField(max_length=200)
    duration = models.PositiveSmallIntegerField()
    long_description = models.TextField()
    language = models.CharField()
    prerequisite = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)
    certificate = models.BooleanField()
    passing_grade = models.PositiveSmallIntegerField()
    passers = models.ManyToManyField("User", related_name="courses_passed")
    creation_date = models.DateField(auto_now_add=True)
