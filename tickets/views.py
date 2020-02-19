from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Ticket
from .forms import AddTicketForm


# Create your views here.
def view_tickets(request):
    """Display All Tickets"""
    tickets = Ticket.objects.filter().order_by('-id')
    return render(request, 'tickets.html', {'tickets': tickets})
    # return HttpResponse('Hello from tickets app')


def view_ticket(request, pk):
    """Display single ticket"""
    ticket = Ticket.objects.filter(id=pk)[0]
    return render(request, 'view_ticket.html', {'ticket': ticket})


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
            return redirect(view_tickets)
    else:
        form = AddTicketForm(instance=ticket)
        return render(request, 'add_ticket.html', {'form': form})


def edit_ticket(request, pk=None):
    """Edits Ticket"""
    # gets ticket
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        form = AddTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # request.user should be recorded in an "updated by column"
            # modifieddate should also be recorded in an "modified column"
            ticket = form.save()
            return redirect(view_tickets)
    else:
        form = AddTicketForm(instance=ticket)
        return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})


def cancel_ticket(request, pk=None):
    """Sets Ticket Status to Cancelled"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.status = "Cancelled"
    ticket.priority = "N/A"
    # set priorty to NA?
    ticket.save()
    return redirect(view_tickets)
