from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from accounts.forms import UserLoginForm, UserRegistrationForm, EditProfileForm


def index(request):
    """Render Home Page"""
    return render(request, 'index.html')


@login_required()
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "Logged out.")
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
                messages.success(
                    request, "Logged in: " + user.username)
                auth.login(user=user, request=request)
                return redirect(reverse('tickets'))
            else:
                login_form.add_error(
                    None, "Your username or password is incorrect.")
    else:
        login_form = UserLoginForm()
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
    """Render User's profile page"""
    user = get_object_or_404(User, email=request.user.email)
    user_profile_1 = get_object_or_404(Profile, user_id=request.user.id)
    if (request.method == 'POST'):
        form = EditProfileForm(
            request.POST, request.FILES, instance=user_profile_1)
        if form.is_valid():
            user_profile_1.save()
            messages.success(request, "Profile image updated.")
            return redirect(user_profile)
    else:
        form = EditProfileForm(instance=user_profile_1)
    return render(request, 'profile.html', {"user": user, "form": form})


@login_required()
def user_list(request):
    """Shows list of all users"""
    users = User.objects.filter()
    staff = User.objects.filter(is_staff=1)
    submitters = User.objects.filter(is_staff=0)
    return render(request, 'user_list.html', {"users": users,
                                              "staff": staff,
                                              "submitters": submitters})


@login_required()
def update_first_name(request):
    """User Updates First Name"""
    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = request.POST
        if form['updated_first_name']:
            user.first_name = form['updated_first_name']
            messages.success(request, "First name updated.")
        else:
            user.first_name = ''
            messages.success(request, "First name cleared.")
        user.save()
    return redirect(user_profile)


@login_required()
def update_last_name(request):
    """User Updates Last Name"""
    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = request.POST
        if form['updated_last_name']:
            user.last_name = form['updated_last_name']
            messages.success(request, "Last name updated.")
        else:
            user.last_name = ''
            messages.success(request, "Last name cleared.")
        user.save()
    return redirect(user_profile)


@login_required()
def update_zoomid(request, pk):
    """User Updates Zoom ID"""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = request.POST
        if form['updated_zoomid']:
            user.profile.zoom_id = form['updated_zoomid']
            messages.success(request, "Zoom ID updated successfully.")
        else:
            user.profile.zoom_id = None
            messages.success(request, "Zoom ID cleared.")
        user.profile.save()
    return redirect(user_profile)


@login_required()
def grant_staff_access(request, pk):
    """Allows Code Institute assessors to be immediately granted Staff Access.
    This is to ensure Assessors can see the full feature set.
    In a non-assessment situation, clicking Request Staff Access link would
     send email to Admin, who could then set is_staff to True.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_staff:
            messages.info(
                request, "You already have staff access.")
        else:
            user.is_staff = True
            user.save()
            messages.success(
                request, ("You have been granted Staff Access as a CI Assessor."
                          "You can now edit all tickets."))
    return redirect(user_profile)
