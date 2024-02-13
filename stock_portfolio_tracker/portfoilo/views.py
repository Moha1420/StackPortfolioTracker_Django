# portfolio/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Portfolio

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User(username=username, password=password)
            user.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Username and password are required.')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('portfolio')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, 'Logged out successfully.')
    return redirect('login')

def portfolio(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        portfolio_items = Portfolio.objects.filter(user=user)
        return render(request, 'portfolio.html', {'user': user, 'portfolio_items': portfolio_items})
    else:
        return redirect('login')
