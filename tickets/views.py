from django.shortcuts import get_object_or_404, render, redirect
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
    print(tickets)
    return render(request, 'tickets/index.html', {'tickets': tickets})


def details(request, ticket_id):
    print(ticket_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    return render(request, 'tickets/details.html', {'ticket': ticket})


def edit(request, ticket_id):
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)

    form = forms.EditTicketForm(request.POST or None, instance=ticket)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Ticket Edited Successfully')
        # Save was successful, so redirect to another page
        return redirect('tickets:index')

    return render(request, 'tickets/edit.html', {
        'form': form
    })
