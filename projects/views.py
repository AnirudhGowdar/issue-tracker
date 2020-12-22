from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from home.models import Project


def create(request):
    form = None
    if request.method == 'POST':
        form = forms.CreateProjectForm(request.POST)
        form.instance.manager = User.objects.get(id=request.user.id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Created Successfully')
            return redirect('projects:index')
    elif request.method == 'GET':
        form = forms.CreateProjectForm()
    return render(
        request=request,
        template_name='projects/create.html',
        context={'form': form}
    )


def index(request):
    tabledata = Project.objects.all()
    for d in tabledata:
        print(d.pk)
    return render(request, 'projects/index.html', {'tabledata': tabledata})


def details(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render(request, 'projects/details.html', {'project': project})


def edit(request, project_id):
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.EditProjectForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Project Edited Successfully')
        # Save was successful, so redirect to another page
        return redirect('projects:index')

    return render(request, 'projects/edit.html', {
        'form': form
    })


def assign(request, project_id):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.AssignUsersForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Developers Added Successfully')
        # Save was successful, so redirect to another page
        return redirect('projects:index')

    return render(request, 'projects/assign.html', {
        'form': form
    })


def remove(request, project_id):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)

    form = forms.RemoveUsersForm(request.POST or None, instance=project)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Developers removed Successfully')
        # Save was successful, so redirect to another page
        return redirect('projects:index')
    return render(request, 'projects/remove.html', {
        'form': form
    })
