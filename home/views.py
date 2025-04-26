from .forms import LoginForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def home_index(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect('home_login')

def home_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_index")
            else:
                form.add_error(None, "Invalid username or password.")
    return render(request, "home/login.html", {"form": form})
