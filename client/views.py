from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserLoginForm, UserRegisterForm


def client(request):
    return render(request, 'init.html', {})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user =authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    args = {} 
    args['form'] = UserRegisterForm()
    return render(request, 'register.html', args)

def logout_view(request):
    logout(request)
    return redirect("/")