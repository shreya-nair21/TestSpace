from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signup_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return redirect('home')
  

  return render(request, 'accounts/signup.html')



def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      return redirect('home')
    
    else:
      return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
  return render(request, 'accounts/login.html')


def logout_user(request):
  logout(request)
  return redirect('login')



