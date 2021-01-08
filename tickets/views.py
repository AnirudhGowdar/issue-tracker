from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from home.models import Ticket, TicketComment, TicketStatus
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
    return render(request, 'tickets/index.html', {'tickets': tickets})


@login_required(login_url='/accounts/login')
def details(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    comments = TicketComment.objects.filter(ticket=ticket).order_by('-created')
    user = request.user
    form = None
    if request.method == 'POST':
        form = forms.AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = user
            new_comment.ticket = ticket
            new_comment.save()
        return redirect('tickets:details', ticket_id=ticket_id)
    else:
        form = forms.AddCommentForm
    return render(
        request,
        'tickets/details.html',
        {
            'ticket': ticket,
            'user': user,
            'comments': comments,
            'form': form
        }
    )


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
        return HttpResponseForbidden()


@login_required(login_url='/accounts/login')
def addpriority(request):
    if request.user.is_superuser:
        form = None
        if request.method == 'POST':
            form = forms.AddTicketPriorityForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket Priority added successfully')
                return redirect('accounts:dashboard')
        elif request.method == 'GET':
            form = forms.AddTicketPriorityForm()
        return render(
            request=request,
            template_name='tickets/addpriority.html',
            context={'form': form}
        )
    else:
        return HttpResponseForbidden()


@login_required(login_url='/accounts/login')
def addtype(request):
    if request.user.is_superuser:
        form = None
        if request.method == 'POST':
            form = forms.AddTicketTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket Type added successfully')
                return redirect('accounts:dashboard')
        elif request.method == 'GET':
            form = forms.AddTicketTypeForm()
        return render(
            request=request,
            template_name='tickets/addtype.html',
            context={'form': form}
        )
    else:
        return HttpResponseForbidden()
