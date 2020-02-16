from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Ticket
from .forms import AddTicketForm


# Create your views here.
def view_tickets(request):
    """Display All Tickets"""
    tickets = Ticket.objects.filter()
    return render(request, 'tickets.html', {'tickets': tickets})
    # return HttpResponse('Hello from tickets app')

def add_ticket(request, pk=None):
    """Add Ticket"""
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if (request.method == "POST"):
        form = AddTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect(view_tickets)
            # return render(request, 'add_ticket.html')
    else:
        form = AddTicketForm(instance=ticket)
    return render(request, 'add_ticket.html', {'form': form})