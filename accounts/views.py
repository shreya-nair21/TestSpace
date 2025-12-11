from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signup_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    
    # Simple validation
    if User.objects.filter(username=username).exists():
      return render(request, 'accounts/signup.html', {'error': 'Username already exists'})

    User.objects.create_user(username=username, password=password)
    # Redirect to login page after successful signup
    return redirect('login') 
  
  return render(request, 'accounts/signup.html')


def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    role = request.POST.get('role') # Get the role from the clicked button

    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      if role == 'teacher':
        return redirect('/admin/') # Redirect to Django Admin
      elif role == 'student':
        return redirect('home') # Redirect to Dashboard/Home
      else:
        # Fallback if no specific role button (shouldn't happen with current template)
        return redirect('home')
    
    else:
      return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
  if request.user.is_authenticated:
      return redirect('home')
      
  return render(request, 'accounts/login.html')


def logout_user(request):
  logout(request)
  return redirect('login')



