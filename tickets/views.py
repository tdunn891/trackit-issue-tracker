from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from .models import Ticket, Comment, HistoricalTicket
from .forms import AddTicketForm, AddCommentForm, EditTicketForm
from rest_framework import viewsets
from .serializers import TicketSerializer
import datetime


# Django REST API
class RestView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

# Dashboard
@login_required()
def dashboard(request):
    return render(request, 'dashboard.html')

# View Tickets
@login_required()
def view_tickets(request):
    """Display All Tickets"""
    tickets = Ticket.objects.filter()
    return render(request, 'tickets.html', {'tickets': tickets})

# View Single Ticket
@login_required()
def view_ticket(request, pk):
    """Display single ticket details, change history and comments"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    # Change History
    historical_changes = HistoricalTicket.objects.filter(id=pk)
    all_deltas = []
    for i in range(historical_changes.count()-1):
        new_record = ticket.history.all()[i]
        old_record = ticket.history.all()[i+1]
        delta = new_record.diff_against(old_record)
        for change in delta.changes:
            if (change.field != 'upvotes'):
                test_change = {
                    'field': change.field,
                    'new_value': change.new,
                    'old_value': change.old,
                    'changed_by': new_record.history_user,
                    'date_changed': new_record.history_date
                }
                all_deltas.append(test_change)

    # Comments
    comments = Comment.objects.filter(ticket_id=pk)
    form = AddCommentForm(request.POST, request.FILES, instance=None)
    # On submit comment
    if (request.method == "POST"):
        if form.is_valid():
            comment_body = form.cleaned_data.get("comment_body")
            comment = Comment(
                ticket_id=pk, comment_body=comment_body, user_id=request.user.id)
            comment.save()
            messages.info(request, "Comment submitted.")
            return redirect(view_ticket, pk)
    return render(request, 'view_ticket.html', {'ticket': ticket,
                                                'comments': comments,
                                                'form': form,
                                                'all_deltas': all_deltas})


@login_required()
def add_ticket(request, pk=None):
    """Add Ticket"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    # On Submit
    if (request.method == "POST"):
        form = AddTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.submitted_by = request.user
            ticket.save()
            form.save_m2m()
            messages.success(
                request, "Your ticket has been submitted | " + str(ticket.id))
            return redirect(view_tickets)
    else:
        form = AddTicketForm(instance=ticket)
        return render(request, 'add_ticket.html', {'form': form})


@login_required()
def upvote(request, pk=None):
    """Upvote a Ticket"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        # Increment upvotes by 1
        ticket.upvotes += 1
        ticket.save()
        messages.info(request, "Ticket Upvoted | " + str(ticket.id))
    return redirect(view_ticket, pk)


@login_required()
def edit_ticket(request, pk=None):
    """Get and Edit a Ticket"""
    # Get ticket
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        form = EditTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            if ticket.status == 'Resolved' and ticket.resolved_date != None:
                # If ticket is set to resolved for the first time, set resolved date to now
                ticket.resolved_date = datetime.datetime.now()
            ticket = form.save()
            messages.info(
                request, "Ticket Updated | " + str(ticket.id))
            return redirect(view_tickets)
    else:
        form = EditTicketForm(instance=ticket)
        return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})


# Not currently used
@login_required()
def delete_ticket(request, pk=None):
    """Deletes a ticket"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.delete()
    return redirect(view_tickets)


@login_required()
def kanban(request):
    """Show KANBAN View"""
    sort_field = request.GET.get(
        'sort_by') if 'sort_by' in request.GET else '-id'
    tickets = Ticket.objects.filter()
    # New tickets count
    new_tickets_count = Ticket.objects.filter(
        status='New').count()
    # In Progress tickets count
    in_progress_tickets_count = Ticket.objects.filter(
        status='In Progress').count()
    # Resolved tickets count
    resolved_tickets_count = Ticket.objects.filter(
        status='Resolved').count()
    # Cancelled tickets count
    cancelled_tickets_count = Ticket.objects.filter(
        status='Cancelled').count()
    # My tickets count
    my_tickets_count = Ticket.objects.filter(
        submitted_by=request.user.id).count()
    return render(request, 'kanban.html', {'tickets': tickets,
                                           'new_tickets_count': new_tickets_count,
                                           'in_progress_tickets_count': in_progress_tickets_count,
                                           'resolved_tickets_count': resolved_tickets_count,
                                           'cancelled_tickets_count': cancelled_tickets_count,
                                           'my_tickets_count': my_tickets_count
                                           })


@login_required()
def change_status(request, pk=None, new_status=None):
    """Quick Update ticket status from dropdown"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == 'POST'):
        ticket.status = new_status
        if ticket.status == 'Resolved':
            # If existing status is Resolved, set resolved date to now.
            ticket.resolved_date = datetime.datetime.now()
        ticket.save()
        messages.info(request, "Ticket Status Updated | " +
                      str(ticket.id) + " | " + ticket.status)
    return redirect(view_tickets)
