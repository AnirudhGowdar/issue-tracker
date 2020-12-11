from django.shortcuts import render, redirect
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
    print(project_id)
    project = Project.objects.get(pk=project_id)
    return render(request, 'projects/details.html', {'project': project})
