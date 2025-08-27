from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Profile
import random

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def recipes(request):
    return render(request, 'core/recipes.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

def login_view(request):
    error = None
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        # Try to get user by email if input contains '@'
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = username_or_email  # fallback
        else:
            username = username_or_email
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid credentials'
    return render(request, 'core/login.html', {'error': error})

def register(request):
    step = request.POST.get('step', '1')
    context = {'step': step}

    if request.method == 'POST':
        if step == '1':
            email = request.POST['email']
            code = random.randint(100000, 999999)
            request.session['register_code'] = str(code)
            request.session['register_email'] = email
            request.session['register_data'] = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'dob': request.POST['dob'],
            }
            send_mail(
                'Your FoodBuddy Verification Code',
                f'Your code is: {code}',
                'noreply@foodbuddy.com',
                [email],
            )
            context.update({'step': '2', 'email': email})
            return render(request, 'core/register.html', context)
        elif step == '2':
            code = request.POST['code']
            if code == request.session.get('register_code'):
                context.update({'step': '3', 'email': request.session.get('register_email')})
                return render(request, 'core/register.html', context)
            else:
                context.update({'step': '2', 'email': request.session.get('register_email'), 'error': 'Invalid code'})
                return render(request, 'core/register.html', context)
        elif step == '3':
            password = request.POST['password']
            email = request.session.get('register_email')
            data = request.session.get('register_data')
            if User.objects.filter(username=email).exists():
                context.update({'step': '1', 'error': 'Email already registered'})
                return render(request, 'core/register.html', context)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            Profile.objects.create(user=user, dob=data['dob'])
            # login(request, user)  # Remove or comment out this line
            return redirect('login')  # Redirect to login page after registration
    else:
        context['step'] = '1'
    return render(request, 'core/register.html', context)

def add_recipe(request):
    return render(request, 'core/add_recipe.html')

def check_username(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def logout_view(request):
    logout(request)
    return redirect('login')