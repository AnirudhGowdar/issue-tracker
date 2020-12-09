from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from home.models import Project

def Create(request):
    form = None
    if request.method == 'POST':
        form = forms.CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Created Successfully')
            return redirect('index')
    elif request.method == 'GET':
        form = forms.CreateProjectForm()
    return render(
        request=request,
        template_name='projects/create.html',
        context={'form': form}
    )
def index(request):
    tabledata = Project.objects.all()
    return render(request, 'projects/index.html',{'tabledata' : tabledata})
