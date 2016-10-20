from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "login_reg/index.html")

def register(request): #just taking the request object
    if request.method == 'POST':
        user = User.objects.register(request.POST)
        #user = a tuple, 2 options, (True, user) or (False, errors)
        if user[0]:
            request.session['user_id']= user[1].id
            request.session['first_name']=user[1].first_name
            return redirect('/success')
        #build flash messages here using user[1]
        for error in user[1]:
        #always going to be referring as user 1 because it's the first user in the list
            messages.error(request, error)
        return redirect('/')
def login(request):
    user = User.objects.login(request.POST)
    if user[0]:
        request.session['user_id'] = user[1].id
        request.session['first_name'] = user[1].first_name
        return redirect('/success')
        #flash messages
    for error in user[1]:
        messages.error(request, error)
    return redirect('/')

def success(request):
    return render(request, 'login_reg/success.html')

def logout(request):
    # Clears the current user out of session
    request.session.clear()
    return redirect('/')
