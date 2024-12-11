from django.contrib import admin
from django.urls import include, path

from . import views
from .views import (LoginView, LogoutView, RegistrationView, TaskCreateView,
                    TaskListView)

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
]
