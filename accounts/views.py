from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate, update_session_auth_hash
from . import forms
from django.contrib.auth.models import Group, User
from home.models import Project, Ticket
from django.contrib.auth.decorators import login_required


def register(request):
    form = None
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            end_user_group = Group.objects.get(name='end_users')
            user.groups.add(end_user_group)
            print(user.groups.all())
            messages.success(request, 'Account created successfully')
            return redirect('accounts:login')
    elif request.method == 'GET':
        form = forms.RegisterForm()
    return render(
        request=request,
        template_name='accounts/register.html',
        context={'form': form}
    )


def login(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('accounts:dashboard')
    elif request.method == 'POST':
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(
                    request, f"You are now logged in as {username}")
                return redirect('accounts:dashboard')
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
        return redirect('home:index')


@login_required(login_url='/accounts/login')
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='project_managers').exists():
            tickets = Ticket.objects.all()
            project = Project.objects.all()
            return render(request, 'accounts/dashboards/dashboard_manager.html', {'tickets': tickets, 'project': project})
        elif request.user.groups.filter(name='developers').exists():
            tickets = Ticket.objects.all()
            project = Project.objects.all()
            return render(request, 'accounts/dashboards/dashboard_developer.html', {'tickets': tickets, 'project': project})
        elif request.user.is_superuser:
            tickets = Ticket.objects.all()
            project = Project.objects.all()
            return render(request, 'accounts/dashboards/dashboard_admin.html', {'tickets': tickets, 'project': project})
        tickets = Ticket.objects.all()
        return render(request, 'accounts/dashboards/dashboard_end_user.html', {'tickets': tickets})
    else:
        messages.error(request, 'You need to login to access the dashboard')
        return redirect('accounts:login')


@login_required(login_url='/accounts/login')
def profile(request, user_id):
    userdata = User.objects.get(pk=user_id)
    return render(request, 'accounts/profile.html', {'userdata': userdata})


@login_required(login_url='/accounts/login')
def edit_profile(request, user_id):
    user = None
    if user_id:
        user = get_object_or_404(User, pk=user_id)

    form = forms.EditProfileForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Profile Updated Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def change_password(request):
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            auth.logout(request)
            return redirect('accounts:login')
    else:
        form = forms.ChangePasswordForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
