from django.http import request
from django.http.response import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate, update_session_auth_hash
from . import forms
from django.contrib.auth.models import Group, User
from home.models import Project, Ticket, TicketType, TicketPriority
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
            y_tickets = []
            r_tickets = []
            tic = Ticket.objects.all()
            projects = Project.objects.all()
            for ticket in tic:
                if ticket.owner == request.user:
                    y_tickets.append(ticket)
            for ticket in tic:
                for s in projects:
                    if ticket.project.title == s.title and s.manager == request.user and ticket.ticket_status_id == 1:
                        r_tickets.append(ticket)
            project = []
            for s in projects:
                if s.manager == request.user:
                    project.append(s)
            return render(request, 'accounts/dashboards/dashboard_manager.html', {'y_tickets': y_tickets, 'r_tickets': r_tickets, 'project': project})
        elif request.user.groups.filter(name='developers').exists():
            y_tickets = []
            a_tickets = []
            tic = Ticket.objects.all()
            project = Project.objects.all()
            for ticket in tic:
                if ticket.owner == request.user:
                    y_tickets.append(ticket)
                if ticket.assigned_to == request.user:
                    a_tickets.append(ticket)
            return render(request, 'accounts/dashboards/dashboard_developer.html', {'y_tickets': y_tickets, 'a_tickets': a_tickets, 'project': project})
        elif request.user.is_superuser:
            tic_type = TicketType.objects.all()
            tic_priority = TicketPriority.objects.all()
            project = Project.objects.all()
            return render(request, 'accounts/dashboards/dashboard_admin.html', {'project': project, 'tic_type': tic_type, 'tic_priority': tic_priority})
        tickets = []
        tic = Ticket.objects.all()
        for ticket in tic:
            if ticket.owner == request.user:
                tickets.append(ticket)
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


@login_required(login_url='/accounts/login')
def users(request):
    if request.user.is_superuser:
        userdata = User.objects.all()
        groupdata = Group.objects.all()
        return render(request, 'accounts/users.html', {'userdata': userdata, 'groupdata': groupdata})
    else:
        return HttpResponseForbidden()


@login_required(login_url='/accounts/login')
def userrole(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = forms.ChangeUserGroupForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Role updated successfully')
        return redirect('accounts:users')
    return render(request, 'accounts/userrole.html', {
        'form': form
    })
