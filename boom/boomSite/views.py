from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm
from .forms import NewPlayerForm
import json
from json import dumps, load, loads
from django.views.decorators.csrf import csrf_exempt
import ast #para diccionario
import sqlite3
from django.contrib.auth.models import User
from .models import Player
from .models import Global
from django.contrib.auth.decorators import login_required   


def index(request):
    template = loader.get_template('boomSite/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('boomSite/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def stats(request):
    
    mydb = sqlite3.connect("db.sqlite3")
    curr = mydb.cursor()
    
    query_leaderboard ='''SELECT username, globalScore, level
        FROM boomSite_global
        ORDER BY globalScore DESC'''
    rows1 = curr.execute(query_leaderboard)
    data_leaderboard = []
    
    counter = 0
    for x in rows1:
        counter += 1
        data_leaderboard.append([counter, x[0], x[2], x[1]])
        
    
    query_timeFinish ='''SELECT username, timeFinish
        FROM boomSite_global
        WHERE level = 4
        ORDER BY timeFinish ASC
        LIMIT 3'''
    
    rows2 = curr.execute(query_timeFinish)
    data_timeFinish = []
    
    for x in rows2:
        data_timeFinish.append([x[0], x[1]])
        
    
    h_var = 'Country'
    v_var = 'Players'
    query_countries ='''SELECT Country, COUNT(Country)
		FROM boomSite_player
		GROUP BY Country
	'''
    rows3 = curr.execute(query_countries)
    data = [[h_var, v_var]]
    
    for x in rows3:
        data.append([x[0], x[1]])

    modified_data = dumps(data)
    
    
 
 
    return render(request, 'boomSite/stats.html', {'values':data_leaderboard, 'values2': data_timeFinish, 'values3': modified_data})

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
        form = NewUserForm(request.POST, instance=request.user)
        player_form = NewPlayerForm(request.POST, instance=request.user.player)
        if form.is_valid() and player_form.is_valid():
            user = form.save()
            player_form.save()
            login(user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        return render(request, 'boomSite/signup.html', {})

    # template = loader.get_template('boomSite/signup.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def profile(request):
    return render(request,'boomSite/profile.html')
    # template = loader.get_template('boomSite/profile.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return redirect('index')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        var = request.body
        dicc = ast.literal_eval(var.decode('utf-8'))
        # revisar que ['user'] existe
        u = Player.objects.filter(username=dicc['username'])
        return HttpResponse(str(json.dumps(u[0].toJson())).encode('utf-8'))
    else:
        return HttpResponse("Please use POST")


def playing(request):
    mydb = sqlite3.connect("db.sqlite3")
    curr = mydb.cursor()
    if request.method == 'POST':
        p = request.body
        d = ast.literal_eval(p.decode('utf-8'))
        userSqlite = Global.objects.filter(username=d['level'])
        u2 = userSqlite[0]
        u2.level = u2
        u2.save()
        
        g = Global()
        
        