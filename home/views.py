from .forms import LoginForm
from .forms import ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "As senhas não coincidem.")
                return redirect(reverse('home:change_password'))

            user = authenticate(
                request,
                username=request.user.username,
                password=old_password
            )
            if user is not None:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Senha alterada com sucesso.")
                return redirect(reverse('home:index'))
            else:
                messages.error(request, "Senha antiga inválida.")
                return redirect(reverse('home:change_password'))
    else:
        form = ChangePasswordForm()
    return render(
        request,
        'home/change_password.html',
        {'form': form, 'action': 'Alterar Senha'}
    )

def help_about(request):
        return render(request, 'home/help_about.html')

def help_entities(request):
        return render(request, 'home/help_entities.html')

def help_examples(request):
        return render(request, 'home/help_examples.html')

@login_not_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect(reverse('home:hlogin'))

@login_not_required
def hlogin(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("home:index"))
            else:
                form.add_error(None, "Usuário ou senha inválidos.")
    return render(request, "home/login.html", {"form": form})

@login_not_required
def hlogout(request):
    if request.user.is_authenticated:
        logout(request)
        # successfully logged out message
        messages.success(request, "Você fez o logout com sucesso.")
    else:
        messages.warning(request, "Você não está logado.")
    return redirect("home:login")
