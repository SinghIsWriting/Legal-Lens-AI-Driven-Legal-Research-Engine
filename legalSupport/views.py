from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from legalSupport.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from .utils import send_welcome_email
from django.contrib.auth import views as auth_views

def register(request):
    """
    Handles user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template for user registration.
    """
    form = CreateUserForm()
    msgs = None

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account was created for {user} successfully!')
            send_welcome_email(user, email)  # Sending welcome email
            return redirect('login')
        else:
            print("Form is not valid")
            msgs = form.errors
            print(form.errors)
            form = CreateUserForm()

    context = {
        'form': form,
        'messages': msgs
    }
    return render(request, 'legalSupport/register.html', context)

def loginPage(request):
    """
    Handles user login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template for user login.
    """
    print(auth_views.PasswordResetConfirmView())
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'legalSupport/login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def password_reset_view(request):
    print(auth_views.PasswordResetForm())
    if request.method == 'POST':
        form = auth_views.PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')
    else:
        form = auth_views.PasswordResetForm()
        print(form)
    return render(request, 'password_reset_form.html', {'form': form})