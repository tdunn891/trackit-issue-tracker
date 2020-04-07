from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from accounts.models import Profile
import stripe


stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            total = 9.90
            order_line_item = OrderLineItem(
                order=order,
                product="PRO",
                quantity=1
            )
            order_line_item.save()

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                # Set 'is_pro_user' to True
                user = get_object_or_404(Profile, user_id=request.user.id)
                user.is_pro_user = True
                user.date_turned_pro = timezone.now()
                user.save()
                messages.success(
                    request, "You have successfully paid. Enjoy PRO!")
                # request.session['cart'] = {}

                return redirect(reverse('profile'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(
                request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})
