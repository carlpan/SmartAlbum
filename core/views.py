from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from .forms import LoginForm
from album.views import album

# Create your views here.

def home(request):
    if request.user.is_authenticated():
        return album(request)
    else:
        return render(request, 'core/home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect(reverse('core:home'))
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect(reverse('core:home'))
