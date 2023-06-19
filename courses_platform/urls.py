from django.urls import path
from . import views

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("createCourse", views.create_course, name="create_course"),
    path("courses/<int:course_id>/quiz", views.quiz, name="quiz"),
    path("allCourses", views.all_courses, name="all_courses"),
    path("courses/<int:course_id>", views.course_page, name="course_page"),
    path("enroll/<int:course_id>", views.course_enroll, name="course_enroll"),
    path("profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("profile/<int:user_id>/completedCourses",
         views.completed_courses, name="completed_courses"),
    path("profile/<int:user_id>/enrolledCourses",
         views.enrolled_courses, name="enrolled_courses"),
    path("editProfile",
         views.edit_profile, name="edit_profile"),

    # Paths for password reset
    path('password-reset/', PasswordResetView.as_view(
        template_name='courses_platform/password_reset.html',
        email_template_name='courses_platform/password_reset_email.html'), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='courses_platform/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='courses_platform/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='courses_platform/password_reset_complete.html'), name='password_reset_complete'),

    # API
    path("allCoursesApi", views.all_courses_api, name="all_courses_api")
]
