from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from home.models import Project, Ticket
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def create(request):
    if request.user.groups.filter(name='project_managers').exists():
        form = None
        if request.method == 'POST':
            form = forms.CreateProjectForm(request.POST)
            form.instance.manager = User.objects.get(id=request.user.id)
            if form.is_valid():
                form.save()
                messages.success(request, 'Project Created Successfully')
                return redirect('accounts:dashboard')
        elif request.method == 'GET':
            form = forms.CreateProjectForm()
    else:
        return HttpResponseForbidden()
    return render(
        request=request,
        template_name='projects/create.html',
        context={'form': form}
    )


@login_required(login_url='/accounts/login')
def index(request):
    tabledata = Project.objects.all()
    for d in tabledata:
        print(d.pk)
    return render(request, 'projects/index.html', {'tabledata': tabledata})


@login_required(login_url='/accounts/login')
def details(request, project_id):
    tickets = []
    user = request.user
    project = Project.objects.get(pk=project_id)
    tic = Ticket.objects.all()
    for ticket in tic:
        if ticket.project == project:
            tickets.append(ticket)
    return render(request, 'projects/details.html', {'project': project, 'user': user, 'tickets': tickets})


@login_required(login_url='/accounts/login')
def edit(request, project_id):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.EditProjectForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Project Edited Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'projects/edit.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def assign(request, project_id):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.AssignUsersForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Developers Added Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'projects/assign.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def remove(request, project_id):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.RemoveUsersForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Developers removed Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')
    return render(request, 'projects/remove.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user == project.manager or request.user.is_superuser:
        project.delete()
        return redirect('accounts:dashboard')
    else:
        return HttpResponseForbidden()
