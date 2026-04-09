from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = Product.objects.filter(user=request.user)
    return render(request, 'home.html', {'user': request.user, 'products': products})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            return render(request, 'register.html', {'error': 'Senhas não conferem'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def add_product(request):
    if request.method == 'POST':
        Product.objects.create(
            user=request.user,
            name=request.POST['name'],
            quantity=request.POST['quantity']
        )
    return redirect('home')

def remove_product(request, id):
    Product.objects.get(id=id).delete()
    return redirect('home')
