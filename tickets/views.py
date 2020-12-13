from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from home.models import Ticket, TicketStatus


def create(request):
    form = None
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST)
        form.instance.owner = User.objects.get(id=request.user.id)
        form.instance.ticket_status = TicketStatus.objects.get(name='New')
        form.instance.archived = False
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket has been opened')
            return redirect('tickets:index')
    elif request.method == 'GET':
        form = forms.CreateTicketForm()
    return render(
        request=request,
        template_name='tickets/create.html',
        context={'form': form}
    )


def index(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/index.html', {'tickets': tickets})
