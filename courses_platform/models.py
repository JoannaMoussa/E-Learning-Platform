from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from PIL import Image
from io import BytesIO
from django.core.files import File
import time


class User(AbstractUser):
    REQUIRED_FIELDS = ["role", "about"]

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
        "Course", blank=True, related_name="enrolled_students")


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

    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3

    LEVEL_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced")
    ]

    instructor = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="courses_taught")
    title = models.CharField(max_length=80, validators=[
                             MinLengthValidator(10), MaxLengthValidator(80)])
    # upload_to() to specify a subdirectory of MEDIA_ROOT to use for uploaded files.
    image = models.ImageField(
        upload_to="courses_images/", null=True, blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    short_description = models.TextField(max_length=200, validators=[
                                         MinLengthValidator(50), MaxLengthValidator(200)])
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(24)])
    long_description = models.TextField(
        max_length=2000, validators=[MinLengthValidator(200), MaxLengthValidator(2000)])
    language = models.PositiveSmallIntegerField(choices=LANGUAGE_CHOICES)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    prerequisite = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True)
    certificate = models.BooleanField()
    passing_grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(100)])
    passers = models.ManyToManyField(
        "User", blank=True, related_name="courses_passed")
    creation_date = models.DateField(auto_now_add=True)

    # before saving the instance we’re reducing the image
    def save(self, *args, **kwargs):
        # Make sure to compress the image only if the course in being created, not on course update.
        # Otherwise, every time we update the course, the image will be compressed!
        if self.image and self.id is None:
            self.image = self.reduce_image_size(self.image)
        # The super() function is used to give access to methods and properties of a parent or sibling class.
        super().save(*args, **kwargs)

    def reduce_image_size(self, image):
        img = Image.open(image).convert('RGB')
        compressed_io = BytesIO()
        img.save(compressed_io, "jpeg", quality=75)
        new_image = File(
            compressed_io, name=f"{self.title[:10]}_{int(time.time())}.jpg")
        return new_image

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image.url if self.image else "/media/courses_images/default_img.jpg",
            "duration": self.duration,
            "language": self.get_language_display(),
            "level": self.get_level_display(),
            "creation_date": self.creation_date.strftime("%B %Y"),
            "enrolled_students": len(self.enrolled_students.all())
        }
