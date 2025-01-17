from django.shortcuts import render , redirect
# django authentication  
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .forms import SignUpForm
from django.http import HttpResponse
import requests


def home(request):
    # check to see if logging in 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request , username = username , password = password)
        if user is not None :
            login(request , user)
            messages.success(request , "You Have Been Logged In")
            return redirect('home')
        else:
            messages.error(request , "There Was An Error Logging In ,Please Try Again...")
            return redirect('home')
    else:
        return render(request , 'home.html' , {})


    
def logout_user(request):
    logout(request)
    messages.success(request , "You Have Been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password = password)

            login(request , user)
            messages.success(request , "You Have Been Successfully Registered!")
            return redirect('home')
    
    else:
        form = SignUpForm()
    return render(request, 'register.html' , {'form':form})


# views.py
def proxy(request):
    url = request.GET.get('url', '')
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    return HttpResponse(status=400)
