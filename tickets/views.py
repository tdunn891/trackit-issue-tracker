from accounts.models import Profile
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.utils.safestring import mark_safe
from rest_framework import viewsets
from .forms import AddTicketForm, AddCommentForm, EditTicketForm
from .models import Ticket, Comment, HistoricalTicket
from .serializers import TicketSerializer


class RestView(viewsets.ModelViewSet):
    """Django REST API as data source for Dashboard page"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


@login_required()
def dashboard(request):
    """Renders Dashboard page with 6 charts"""
    return render(request, 'dashboard.html')


@login_required()
def view_tickets(request):
    """Renders Tickets page with data table of all tickets"""
    tickets = Ticket.objects.filter()
    return render(request, 'tickets.html', {'tickets': tickets})


@login_required()
def view_ticket(request, pk):
    """View single ticket details, change history and comments"""
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
                ticket_id=pk,
                comment_body=comment_body,
                user_id=request.user.id)
            comment.save()
            messages.info(request, "Comment submitted.")
            return redirect(view_ticket, pk)
    return render(request, 'view_ticket.html', {'ticket': ticket,
                                                'comments': comments,
                                                'form': form,
                                                'all_deltas': all_deltas})


@login_required()
def add_ticket(request, pk=None):
    """User Adds Ticket (Bug or Feature)"""
    """If user has BASIC account, check if user has reached 10 ticket
     submission limit in current month"""
    user = get_object_or_404(User, id=request.user.id)
    user_profile = get_object_or_404(Profile, user_id=request.user.id)
    if not user_profile.is_pro_user:
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        end_date = datetime.datetime(
            today.year + int(today.month / 12),
            ((today.month % 12) + 1), 1)
        tickets_submitted_this_month = Ticket.objects.filter(
            submitted_by_id=user,
            created_date__range=(start_date, end_date)).count()
        if tickets_submitted_this_month > 9:
            messages.warning(
                request, ("You have reached the 10 ticket monthly limit"
                          " - Go PRO for unlimited tickets."))
            return redirect('checkout')
        else:
            messages.info(
                request, mark_safe(
                    ("Note: You have submitted <b>" +
                     str(tickets_submitted_this_month) +
                     "</b> of <b>10</b> free tickets this month."
                     " <a href='/checkout/'>Go PRO</a> for unlimited."
                     )))
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None

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
    """Upvote a Ticket. Increments upvotes by 1."""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        # Increment upvotes by 1
        ticket.upvotes += 1
        ticket.save()
        messages.info(request, "Ticket Upvoted | " + str(ticket.id))
    return redirect(view_ticket, pk)


@login_required()
def edit_ticket(request, pk=None):
    """
    Edit a Ticket. Get ticket object and prefill Edit Ticket
    Form with existing values. Ticket will be updated on Submit.
    """
    # Get ticket
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        form = EditTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            if (ticket.status == 'Resolved' and
                    ticket.resolved_date is None):
                # If ticket status is set to resolved for the first time,
                # set resolved date to now
                ticket.resolved_date = datetime.datetime.now()
            ticket = form.save()
            messages.info(
                request, "Ticket Updated | " + str(ticket.id))
            return redirect(view_tickets)
    else:
        form = EditTicketForm(instance=ticket)
        return render(request, 'edit_ticket.html',
                      {'form': form, 'ticket': ticket})


@login_required()
def kanban(request):
    """Show tickets in KANBAN View with columns
    representing ticket status (PRO Feature)"""
    # Check if user is PRO user
    user = get_object_or_404(Profile, user_id=request.user.id)
    # If user is not a PRO user, show message and redirect to Checkout.
    if not user.is_pro_user:
        messages.warning(
            request, "Upgrade your account to unlock KANBAN View.")
        return redirect('checkout')
    else:
        tickets = Ticket.objects.filter()
        # Filter by each Ticket Status for subtotals in dashboard template.
        new_tickets = tickets.filter(
            status='New')
        in_progress_tickets = tickets.filter(
            status='In Progress')
        resolved_tickets = tickets.filter(
            status='Resolved')
        cancelled_tickets = tickets.filter(
            status='Cancelled')
        return render(request, 'kanban.html',
                      {'tickets': tickets,
                       'new_tickets': new_tickets,
                       'in_progress_tickets': in_progress_tickets,
                       'resolved_tickets': resolved_tickets,
                       'cancelled_tickets': cancelled_tickets,
                       })


@login_required()
def change_status(request, pk=None, new_status=None):
    """Quick Update ticket status from dropdown"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == 'POST'):
        ticket.status = new_status
        if ticket.status == 'Resolved':
            # If status is Resolved, set resolved date to now.
            ticket.resolved_date = datetime.datetime.now()
        ticket.save()
        messages.info(request, "Ticket Status Updated | " +
                      str(ticket.id) + " | " + ticket.status)
    return redirect(view_tickets)
