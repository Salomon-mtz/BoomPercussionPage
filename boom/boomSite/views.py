from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm


def index(request):
    template = loader.get_template('boomSite/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('boomSite/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def stats(request):
    template = loader.get_template('boomSite/stats.html')
    context = {}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template('boomSite/contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=username, password=pwd)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ('Bad login'))
            return render(request, 'boomSite/signin.html', {})
            
    else:
        return render(request, 'boomSite/signin.html', {})
        
    # template = loader.get_template('boomSite/signin.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, 'boomSite/signup.html', {})

    # template = loader.get_template('boomSite/signup.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def profile(request):
    template = loader.get_template('boomSite/profile.html')
    context = {}
    return HttpResponse(template.render(context, request))

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return redirect('index')



