from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render
from .models import Burger  # Не забудьте импортировать модель Burger


def chat(request):
    return render(request, 'chat.html')


def index(request):
    # Меню
    left_menu = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Quiz', 'url': '/quiz/'},

    ]
    right_menu = [
        {'name': 'Login', 'url': '/login/'},
        {'name': 'Sign up', 'url': '/register/'},
    ]

    # Получаем список бургеров
    burgers = Burger.objects.all().order_by('-created_at')
    print(f"Found {burgers.count()} burgers")  # Для отладки

    # Если нужно только 4 бургера, используем этот вариант
    featured_burgers = burgers[:4]

    # Контекст для передачи в шаблон
    context = {
        'left_menu': left_menu,
        'right_menu': right_menu,
        'burgers': burgers,  # Все бургеры
        'featured_burgers': featured_burgers,  # Первые 4 бургера
    }

    return render(request, 'index.html', context)


def quiz(request):
    return render(request, 'quiz.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')

        errors = {}

        if len(username) < 3:
            errors['username'] = 'The username must be at least 3 characters long!'
        elif User.objects.filter(username__iexact=username).exists():
            errors['username'] = 'This username is in use!'

        try:
            validate_email(email)
            if User.objects.filter(email__iexact=email).exists():
                errors['email'] = 'This email is in use!'
        except ValidationError:
            errors['email'] = 'Invalid email format!'

        if len(password) < 8:
            errors['password'] = 'The password must be at least 8 characters long!'
        elif password != confirm_password:
            errors['confirmPassword'] = 'Passwords do not match!'

        if not first_name:
            errors['first_name'] = 'Enter your First name!'
        if not last_name:
            errors['last_name'] = 'Enter your Last name!'

        if errors:
            for field, message in errors.items():
                messages.error(request, message)
            return render(request, 'register.html', {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            })


        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            messages.success(request, 'Registration completed successfully! Use your username and password to log in.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'System error: {str(e)}')
            return render(request, 'register.html', {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            })

    # GET-запрос - показываем пустую форму
    return render(request, 'register.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'index')  # Для перенаправления после входа
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {'username': username})

    return render(request, 'login.html')

