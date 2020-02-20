from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Ticket, Comment
from .forms import AddTicketForm, AddCommentForm


# Create your views here.
def view_tickets(request):
    """Display All Tickets"""
    tickets = Ticket.objects.filter().order_by('-id')
    return render(request, 'tickets.html', {'tickets': tickets})
    # return HttpResponse('Hello from tickets app')


def view_ticket(request, pk):
    """Display single ticket"""
    ticket = Ticket.objects.filter(id=pk)[0]
    comments = Comment.objects.filter(ticket_id=pk)
    # If post (add comment button click)
    form = AddCommentForm(request.POST, request.FILES, instance=None)
    if (request.method == "POST"):
        if form.is_valid():
            comment_body = form.cleaned_data.get("comment_body")
            comment = Comment(
                ticket_id=pk, comment_body=comment_body, user_id=request.user.id)
            comment.save()
            return redirect(view_ticket, pk)
    return render(request, 'view_ticket.html', {'ticket': ticket, 'comments': comments, 'form': form})


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
    ticket.save()
    return redirect(view_tickets)


def delete_ticket(request, pk=None):
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.delete()
    return redirect(view_tickets)


# def add_comment(request):
#     """TESTAdd Ticket"""
#     print('test')
#     # On Submit
#     if (request.method == "POST"):
#         form = AddCommentForm(request.POST, request.FILES, instance=None)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             # ticket.submitted_by = request.user
#             comment.save()
#             form.save_m2m()
#             return redirect(view_tickets)
#     else:
#         form = AddCommentForm(instance=None)
#         return render(request, 'view_ticket.html', {'form': form})
