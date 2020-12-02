from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from . import forms


def register(request):
    form = None
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    elif request.method == 'GET':
        form = forms.RegisterForm()
    return render(
        request=request,
        template_name='accounts/register.html',
        context={'form': form}
    )


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = forms.LoginForm()
    return render(
        request=request,
        template_name='accounts/login.html',
        context={"form": form}
    )


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    else:
        return render(request, 'accounts/error.html')
