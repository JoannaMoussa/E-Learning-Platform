from django.contrib import admin
from .models import User, Course


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "role",
                    "instructor_title", "get_enrolled_courses")

    def get_enrolled_courses(self, obj):
        return "\n".join([enrolled_course.title for enrolled_course in obj.enrolled_courses.all()])


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "instructor", "title", "image", "category", "duration",
                    "language", "level", "prerequisite", "certificate",
                    "passing_grade", "get_passers", "creation_date")

    def get_passers(self, obj):
        return "\n".join([passer.username for passer in obj.passers.all()])


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
