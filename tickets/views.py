from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from .models import Ticket, Comment, HistoricalTicket
from .forms import AddTicketForm, AddCommentForm
from rest_framework import viewsets
from .serializers import TicketSerializer


# Create your views here.

# REST api
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
    """Display single ticket"""
    ticket = Ticket.objects.filter(id=pk)[0]
    comments = Comment.objects.filter(ticket_id=pk)
    historical_changes = HistoricalTicket.objects.filter(id=pk)
    all_deltas = []
    for x in range(historical_changes.count()-1):
        new_record = ticket.history.all()[x]
        old_record = ticket.history.all()[x+1]
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

    # * Display comment box
    form = AddCommentForm(request.POST, request.FILES, instance=None)
    # * On submit comment
    if (request.method == "POST"):
        if form.is_valid():
            comment_body = form.cleaned_data.get("comment_body")
            comment = Comment(
                ticket_id=pk, comment_body=comment_body, user_id=request.user.id)
            comment.save()
            return redirect(view_ticket, pk)
    return render(request, 'view_ticket.html', {'ticket': ticket, 'comments': comments, 'form': form, 'all_deltas': all_deltas})


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
            return redirect(view_tickets)
    else:
        form = AddTicketForm(instance=ticket)
        return render(request, 'add_ticket.html', {'form': form})


@login_required()
def upvote(request, pk=None):
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.upvotes += 1
    ticket.save()
    return redirect(view_ticket, pk)


@login_required()
def edit_ticket(request, pk=None):
    """Edits Ticket"""
    # gets ticket
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        form = AddTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # modifieddate should also be recorded in an "modified column"
            ticket = form.save()
            return redirect(view_tickets)
    else:
        form = AddTicketForm(instance=ticket)
        return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required()
def cancel_ticket(request, pk=None):
    """Sets Ticket Status to Cancelled"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.status = "Cancelled"
    ticket.priority = "N/A"
    ticket.save()
    return redirect(view_tickets)


@login_required()
def delete_ticket(request, pk=None):
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.delete()
    return redirect(view_tickets)


@login_required()
def kanban(request):
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
    return render(request, 'kanban.html', {'tickets': tickets,
                                           'new_tickets_count': new_tickets_count,
                                           'in_progress_tickets_count': in_progress_tickets_count,
                                           'resolved_tickets_count': resolved_tickets_count
                                           })


@login_required()
def change_status(request, pk=None, new_status=None):
    # get ticket
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    # change status
    print('New Status: ' + new_status)
    # ticket.status = 'In Progress'
    ticket.status = new_status
    ticket.save()
    return redirect(kanban)
