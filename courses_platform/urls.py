from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("createCourse", views.create_course, name="create_course"),
    path("<int:course_id>/quiz", views.quiz, name="quiz"),
    path("allCourses", views.all_courses, name="all_courses")
]
