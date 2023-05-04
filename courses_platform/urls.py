from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("createCourse", views.create_course, name="create_course")
]
