from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from accounts.forms import UserLoginForm, UserRegistrationForm

# Create your views here.


def index(request):
    """Render Index.html"""
    return render(request, 'index.html')


@login_required()
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(reverse('index'))


def login(request):
    """Return login page"""
    if request.user.is_authenticated:
        return redirect(reverse('tickets'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                messages.success(request, "You have successfully logged in.")
                auth.login(user=user, request=request)
                return redirect(reverse('tickets'))
            else:
                login_form.add_error(
                    None, "Your username or password is incorrect.")
    else:
        login_form = UserLoginForm()
    # login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})


def registration(request):
    """Render registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            user = registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register your account")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {
        "registration_form": registration_form})


@login_required()
def user_profile(request):
    """User's profile page"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"user": user})


@login_required()
def user_list(request):
    """Shows list of all users"""
    # users = User.objects.filter()
    sort_field = request.GET['sort_by'] if 'sort_by' in request.GET else 'id'
    users = User.objects.filter().order_by(sort_field)
    # Staff
    staff = User.objects.filter(is_staff=1).order_by(sort_field)
    # Submitters
    submitters = User.objects.filter(is_staff=0).order_by(sort_field)
    return render(request, 'user_list.html', {"users": users,
                                              "staff": staff,
                                              "submitters": submitters})
