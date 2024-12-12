from django.contrib import admin
from django.urls import include, path

from . import views
from .views import (LoginView, LogoutView, RegistrationView, TaskCreateView,
                    TaskListView, TaskEditView, TaskDeleteView, MyTaskView, UpdateMyTaskView, TaskDetailView)

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path('edit/<int:task_id>/', TaskEditView.as_view(), name = 'edit_task'),
    path('delete/<int:task_id>/',TaskDeleteView.as_view(), name = 'delete_task'),
    path('mytask/', MyTaskView.as_view(), name = "my_task"),
    path('updatetask/<int:task_id>', UpdateMyTaskView.as_view(), name = 'update_mytask'),
    path('detail/<int:task_id>', TaskDetailView.as_view(), name = "task_detail"),
]
