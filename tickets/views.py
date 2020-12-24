from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from home.models import Ticket, TicketStatus
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def create(request):
    form = None
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST, request.FILES)
        form.instance.owner = User.objects.get(id=request.user.id)
        form.instance.ticket_status = TicketStatus.objects.get(name='New')
        form.instance.archived = False
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket has been opened')
            return redirect('accounts:dashboard')
    elif request.method == 'GET':
        form = forms.CreateTicketForm()
    return render(
        request=request,
        template_name='tickets/create.html',
        context={'form': form}
    )


@login_required(login_url='/accounts/login')
def index(request):
    tickets = Ticket.objects.all()
    print(tickets)
    return render(request, 'tickets/index.html', {'tickets': tickets})


@login_required(login_url='/accounts/login')
def details(request, ticket_id):
    print(ticket_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    user = request.user
    return render(request, 'tickets/details.html', {'ticket': ticket, 'user': user})


@login_required(login_url='/accounts/login')
def edit(request, ticket_id):
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)

    form = forms.EditTicketForm(request.POST or None, instance=ticket)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Ticket Edited Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'tickets/edit.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def assign(request, ticket_id):
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)

    ticket.ticket_status = TicketStatus.objects.get(name='Waiting for support')
    form = forms.AssignDeveloperForm(request.POST or None, instance=ticket)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Developer Assigned Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'tickets/assign.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
def delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.user == ticket.owner or request.user.is_superuser:
        ticket.delete()
        return redirect('accounts:dashboard')
    else:
        return render(request, 'home/error.html')


def addcomment(request, ticket_id):
    pass
