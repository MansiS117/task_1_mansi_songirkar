from django.shortcuts import render, redirect
from django.views import View
from . forms import RegistrationForm, TaskForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Task, User
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request,'index.html')


class RegistrationView(View):
    template_name = 'register.html'
    def get(self, request):
        form = RegistrationForm()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #prevents saving user to database
            user = form.save(commit = False)
            # fetches password and confirm_password from cleaned_data dictionary
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # checks if password and confirm_password matches or not
            if password == confirm_password:
                # hashes the password and then store to the database
                user.set_password(password)
                user.save()

                messages.success(request, "Registration Successful")
                return redirect('home')

            messages.error(request, "Password do not match")
            return render(request, self.template_name,{'form': form})


class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        
        messages.error(request, "Invalid login credentials")
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You are logged out")
        return redirect('home')


class TaskListView(View):
    template_name = 'index.html'
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(assigned_by = request.user)
            context = {
                'tasks' : tasks
            }
            return render(request, self.template_name, context)
        messages.error(request, "You need to log in first")
        return render(request, self.template_name)
    

class TaskCreateView(View):
    template_name = 'create_task.html'
    def get(self, request):
        form = TaskForm()
        return render(request, self.template_name, {"form" : form})
    
    def post(self, request):
        form = TaskForm(request.POST)
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        assigned_to = request.POST.get('assigned_to')
        priority = request.POST.get('priority')

        if form.is_valid():
            task = form.save(commit = False)
            assigned_by = request.user
            assigned_to = User.objects.get(id = assigned_to)
            task = Task(title = title, description = description, due_date = due_date, assigned_to = assigned_to, assigned_by = assigned_by, priority = priority)
            task.save()
            messages.success(request, "Task created sucessfully")
            return redirect('home')
        messages.error(request, "Try again")
        return render(request, self.template_name, {'form' : form})