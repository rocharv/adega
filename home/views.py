from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


def home_help(request):
        return render(request, 'home/help.html')

@login_not_required
def home_index(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect(reverse('home:home_login'))

@login_not_required
def home_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("home:home_index"))
            else:
                form.add_error(None, "Usuário ou senha inválidos.")
    return render(request, "home/login.html", {"form": form})

@login_not_required
def home_logout(request):
    if request.user.is_authenticated:
        logout(request)
        # successfully logged out message
        messages.success(request, "Você fez o logout com sucesso.")
    else:
        messages.warning(request, "Você não está logado.")
    return redirect("home:home_login")
